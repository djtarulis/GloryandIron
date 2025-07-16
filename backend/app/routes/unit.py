from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from jose import jwt
from app.models import player
from app.models.city import City
from app.models.unit import Unit
from app.models.unit_type import UnitType
from app.models.unit_training import UnitTraining
from app.db.session import get_db
from app.routes.auth import (
    get_player_by_username,
    oauth2_scheme,
    SECRET_KEY,
    ALGORITHM,
)

router = APIRouter(prefix="/unit", tags=["unit"])

@router.post("/train")
def create_unit(
    city_id: int,
    type: str,
    quantity: int,
    x: int = None,
    y: int = None,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username = payload.get("sub")
    player_obj = get_player_by_username(db, username)
    city = db.query(City).filter(City.id == city_id, City.player_id == player_obj.id).first()
    if not city:
        raise HTTPException(status_code=403, detail="Not authorized to train unit in this city")

    # Get unit type info from UnitType table
    unit_type_obj = db.query(UnitType).filter(UnitType.name == type).first()
    if not unit_type_obj:
        raise HTTPException(status_code=400, detail="Invalid unit type")

    # Default to city coordinates if not provided
    if x is None:
        x = city.x
    if y is None:
        y = city.y

    # Calculate training time (with efficiency bonus for batch training)
    base_time = unit_type_obj.base_training_time
    if quantity <= 1:
        total_time = base_time
    else:
        efficiency = min(0.3, 0.05 * (quantity - 1))  # up to 30% faster
        total_time = int(base_time * quantity * (1 - efficiency))

    now = datetime.now(timezone.utc)
    finish_time = now + timedelta(seconds=total_time)

    # Add training to queue
    training = UnitTraining(
        city_id=city_id,
        unit_type=type,
        quantity=quantity,
        training_started_at=now,
        training_finishes_at=finish_time,
        finished=0
    )
    db.add(training)
    db.commit()
    db.refresh(training)

    return {
        "msg": f"Training {quantity} {type}(s) started",
        "training_id": training.id,
        "city_id": city_id,
        "type": type,
        "quantity": quantity,
        "training_started_at": now,
        "training_finishes_at": finish_time,
        "duration_seconds": total_time
    }

# When training is finished, use this logic to add units to the garrison:
def add_units_to_garrison(city_id, type, quantity, x, y, db):
    unit = db.query(Unit).filter_by(
        city_id=city_id,
        type=type,
        moving=0,
        x=x,
        y=y
    ).first()
    if unit:
        unit.quantity += quantity
    else:
        unit = Unit(
            city_id=city_id,
            type=type,
            quantity=quantity,
            x=x,
            y=y,
            moving=0
        )
        db.add(unit)
    db.commit()
    db.refresh(unit)
    return unit

@router.post("/{unit_id}/move")
def move_unit(
    unit_id: int,
    destination_x: int,
    destination_y: int,
    quantity: int,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username = payload.get("sub")
    player_obj = get_player_by_username(db, username)

    unit = db.query(Unit).filter(Unit.id == unit_id).first()
    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")

    city = db.query(City).filter(City.id == unit.city_id).first()
    if not city or city.player_id != player_obj.id:
        raise HTTPException(status_code=403, detail="Not authorized to move this unit")
    if unit.moving:
        raise HTTPException(status_code=400, detail="Unit is already moving")
    if unit.quantity < quantity:
        raise HTTPException(status_code=400, detail="Not enough units to move")

    # Calculate travel time (simple example: 1 min per tile)
    # TODO: Factor in terrain, unit type, etc.
    distance = abs(unit.x - destination_x) + abs(unit.y - destination_y)
    travel_time = timedelta(minutes=distance)
    arrival = datetime.now(timezone.utc) + travel_time

    # Update unit for movement
    unit.moving = 1
    unit.destination_x = destination_x
    unit.destination_y = destination_y
    unit.arrival_time = arrival

    db.commit()
    return {"msg": "Unit is moving", "arrival_time": arrival}

@router.delete("/{unit_id}/delete")
def delete_unit(
    unit_id: int,
    quantity: int = 1,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username = payload.get("sub")
    player_obj = get_player_by_username(db, username)

    unit = db.query(Unit).filter(Unit.id == unit_id).first()
    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")

    # Only allow deletion if the player owns the city the unit is in
    city = db.query(City).filter(City.id == unit.city_id).first()
    if not city or city.player_id != player_obj.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this unit")

    if quantity >= unit.quantity:
        db.delete(unit)
        db.commit()
        return {"msg": f"All {unit.type} units deleted from garrison"}
    else:
        unit.quantity -= quantity
        db.commit()
        return {
            "msg": f"{quantity} {unit.type} units deleted from garrison",
            "unit_id": unit.id,
            "type": unit.type,
            "quantity": unit.quantity,
            "x": unit.x,
            "y": unit.y
        }