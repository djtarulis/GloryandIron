from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from jose import jwt
from datetime import datetime, timedelta, timezone
from app.models import player
from app.models.army import Army
from app.models.city import City
from app.models.unit import Unit
from app.db.session import get_db
from app.routes.auth import (
    get_player_by_username,
    oauth2_scheme,
    SECRET_KEY,
    ALGORITHM,
)

router = APIRouter(prefix="/army", tags=["army"])

@router.post("/create")
def create_army(
    origin_city_id: int = Body(...),
    units: dict = Body(...),  # e.g., {"Rifleman": 100, "Tank": 10}
    mission: str = Body("attack"),
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username = payload.get("sub")
    player = get_player_by_username(db, username)
    city = db.query(City).filter(City.id == origin_city_id, City.player_id == player.id).first()
    if not city:
        raise HTTPException(status_code=404, detail="Origin city not found or not owned by player")

    # Validate enough units in city
    for unit_type, qty in units.items():
        city_unit = db.query(Unit).filter_by(city_id=city.id, type=unit_type).first()
        if not city_unit or city_unit.quantity < qty:
            raise HTTPException(status_code=400, detail=f"Not enough {unit_type} in city")

    # Deduct units from city
    for unit_type, qty in units.items():
        city_unit = db.query(Unit).filter_by(city_id=city.id, type=unit_type).first()
        city_unit.quantity -= qty

    # Create Army record (stationary at city)
    army = Army(
        owner_id=player.id,
        origin_city_id=city.id,
        origin_x=city.x,
        origin_y=city.y,
        destination_x=None,
        destination_y=None,
        units=units,
        departure_time=None,
        arrival_time=None,
        status="idle",
        mission=mission
    )
    db.add(army)
    db.commit()
    db.refresh(army)

    return {
        "msg": "Army created and stationed at city",
        "army_id": army.id,
        "units": army.units,
        "origin": (city.x, city.y),
        "status": army.status,
        "mission": mission
    }

@router.post("/{army_id}/add_units")
def add_units_to_army(
    army_id: int,
    units: dict = Body(...),  # e.g., {"Rifleman": 50, "Tank": 5}
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username = payload.get("sub")
    army = db.query(Army).filter(Army.id == army_id).first()
    if not army:
        raise HTTPException(status_code=404, detail="Army not found")
    player_obj = get_player_by_username(db, username)
    if army.owner_id != player_obj.id:
        raise HTTPException(status_code=403, detail="Not authorized to modify this army")

    # Find the city where the army is currently stationed
    city = db.query(City).filter(City.id == army.origin_city_id, City.player_id == player_obj.id).first()
    if not city:
        raise HTTPException(status_code=404, detail="Army is not stationed in a valid city you own")

    # Check and subtract units from the garrison
    for unit_type, qty in units.items():
        city_unit = db.query(Unit).filter_by(city_id=city.id, type=unit_type, moving=0, x=city.x, y=city.y).first()
        if not city_unit or city_unit.quantity < qty:
            raise HTTPException(status_code=400, detail=f"Not enough {unit_type} in city garrison")
        city_unit.quantity -= qty
        if city_unit.quantity == 0:
            db.delete(city_unit)

    # Add units to the army
    current_units = dict(army.units or {})
    for unit_type, qty in units.items():
        current_units[unit_type] = current_units.get(unit_type, 0) + qty
    army.units = current_units

    db.commit()
    db.refresh(army)
    return {
        "msg": "Units added to army",
        "army_id": army.id,
        "units": army.units
    }

@router.post("/{army_id}/move")
def move_existing_army(
    army_id: int,
    destination_x: int = Body(...),
    destination_y: int = Body(...),
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username = payload.get("sub")
    army = db.query(Army).filter(Army.id == army_id).first()
    if not army:
        raise HTTPException(status_code=404, detail="Army not found")
    if army.owner_id != player.id:
        raise HTTPException(status_code=403, detail="Not authorized to move this army")
    if army.status != "idle":
        raise HTTPException(status_code=400, detail="Army is already moving or not idle")

    # Calculate travel time (simple example)
    origin_x, origin_y = army.origin_x, army.origin_y
    distance = abs(origin_x - destination_x) + abs(origin_y - destination_y)
    travel_time = timedelta(minutes=distance)
    departure = datetime.now(timezone.utc)
    arrival = departure + travel_time

    # Update army for movement
    army.destination_x = destination_x
    army.destination_y = destination_y
    army.departure_time = departure
    army.arrival_time = arrival
    army.status = "marching"

    db.commit()
    db.refresh(army)
    return {
        "msg": "Army is marching",
        "army_id": army.id,
        "units": army.units,
        "origin": (origin_x, origin_y),
        "destination": (destination_x, destination_y),
        "arrival_time": arrival,
        "status": army.status
    }

@router.post("/{army_id}/remove_units")
def remove_units_from_army(
    army_id: int,
    units: dict = Body(...),  # e.g., {"Rifleman": 10, "Tank": 2}
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username = payload.get("sub")
    player_obj = get_player_by_username(db, username)

    army = db.query(Army).filter(Army.id == army_id).first()
    if not army:
        raise HTTPException(status_code=404, detail="Army not found")
    if army.owner_id != player_obj.id:
        raise HTTPException(status_code=403, detail="Not authorized to modify this army")

    # Find the city where the army is currently stationed
    city = db.query(City).filter(City.id == army.origin_city_id, City.player_id == player_obj.id).first()
    if not city:
        raise HTTPException(status_code=404, detail="Army is not stationed in a valid city you own")

    # Remove units from army and add back to garrison
    current_units = dict(army.units or {})
    for unit_type, qty in units.items():
        if unit_type not in current_units or current_units[unit_type] < qty:
            raise HTTPException(status_code=400, detail=f"Not enough {unit_type} in army to remove")
        current_units[unit_type] -= qty
        if current_units[unit_type] <= 0:
            del current_units[unit_type]

        # Add back to garrison
        garrison_unit = db.query(Unit).filter_by(
            city_id=city.id,
            type=unit_type,
            moving=0,
            x=city.x,
            y=city.y
        ).first()
        if garrison_unit:
            garrison_unit.quantity += qty
        else:
            new_unit = Unit(
                city_id=city.id,
                type=unit_type,
                quantity=qty,
                x=city.x,
                y=city.y,
                moving=0
            )
            db.add(new_unit)

    army.units = current_units
    db.commit()
    db.refresh(army)
    return {
        "msg": "Units removed from army and returned to garrison",
        "army_id": army.id,
        "units": army.units
    }

@router.get("/{army_id}")
def view_army(
    army_id: int,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username = payload.get("sub")
    player_obj = get_player_by_username(db, username)

    army = db.query(Army).filter(Army.id == army_id).first()
    if not army:
        raise HTTPException(status_code=404, detail="Army not found")
    if army.owner_id != player_obj.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this army")

    # Army location: if marching, use destination; else, use origin
    if army.status == "marching" and army.destination_x is not None and army.destination_y is not None:
        location = {"x": army.destination_x, "y": army.destination_y}
    else:
        location = {"x": army.origin_x, "y": army.origin_y}

    # List all units and their quantities
    units_list = [
        {"type": unit_type, "quantity": qty}
        for unit_type, qty in (army.units or {}).items()
    ]

    return {
        "army_id": army.id,
        "units": units_list,
        "location": location,
        "status": army.status,
        "mission": army.mission
    }