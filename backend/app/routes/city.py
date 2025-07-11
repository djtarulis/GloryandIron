from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from jose import jwt
from datetime import datetime, timedelta, timezone

from app.db.session import get_db
from app.models.city import City
from app.models.building import Building
from app.routes.auth import (
    get_player_by_username,
    oauth2_scheme,
    SECRET_KEY,
    ALGORITHM,
)

router = APIRouter(prefix="/city", tags=["city"])

# Create new city
@router.post("/create")
def create_city(
    name: str,
    x: int,
    y: int,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username = payload.get("sub")
    player = get_player_by_username(db, username)
    if not player:
        raise HTTPException(status_code=401, detail="Invalid user")
    
    # Check if this is the player's first city
    is_first_city = db.query(City).filter(City.player_id == player.id).count() == 0

    if is_first_city:
        # Default starting resources for the first city
        steel = 2000
        oil = 2000
        rubber = 1000
        food = 2000
        gold = 1000
    else:
        # Lower resources for additional cities
        steel = 500
        oil = 500
        rubber = 250
        food = 500
        gold = 250

    city = City(
        name=name,
        player_id=player.id,
        x=x,
        y=y,
        steel=steel,
        oil=oil,
        rubber=rubber,
        food=food,
        gold=gold,
        steel_rate=100.0,
        oil_rate=80.0,
        rubber_rate=60.0,
        food_rate=120.0,
        gold_rate=50.0
    )
    db.add(city)
    db.commit()
    db.refresh(city)

    warehouse = Building(
    city_id=city.id,
    type="Warehouse",
    level=1,
    construction_started_at=datetime.now(timezone.utc),
    construction_finished_at=datetime.now(timezone.utc)
    )
    db.add(warehouse)
    db.commit()
    return {"msg": "City created", "city_id": city.id}

# List cities for the current user
@router.get("/list")
def list_cities(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username = payload.get("sub")
    player = get_player_by_username(db, username)
    if not player:
        raise HTTPException(status_code=401, detail="Invalid user")
    return {"cities": [{"id": c.id, "user": c.player.username, "name": c.name, "x": c.x, "y": c.y} for c in player.cities]}

# Collect resources from a city
@router.post("/{city_id}/collect")
def collect_resources(
    city_id: int,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username = payload.get("sub")
    player = get_player_by_username(db, username)
    city = db.query(City).filter(City.id == city_id, City.player_id == player.id).first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    now = datetime.now(timezone.utc)
    elapsed_hours = (now - city.last_collected_at).total_seconds() / 3600

    # Example static rates
    steel_rate = 100.0  # per hour
    oil_rate = 80.0
    rubber_rate = 60.0
    food_rate = 120.0
    gold_rate = 50.0

    city.steel = min(city.steel + float(steel_rate * elapsed_hours), city.max_steel)
    city.oil = min(city.oil + float(oil_rate * elapsed_hours), city.max_oil)
    city.rubber = min(city.rubber + float(rubber_rate * elapsed_hours), city.max_rubber)
    city.food = min(city.food + float(food_rate * elapsed_hours), city.max_food)
    city.gold = min(city.gold + float(gold_rate * elapsed_hours), city.max_gold)
    city.last_collected_at = now

    db.commit()
    db.refresh(city)
    return {
        "msg": "Resources collected",
        "resources": {
            "steel": city.steel,
            "oil": city.oil,
            "rubber": city.rubber,
            "food": city.food,
            "gold": city.gold,
        }
    }

# Get city details
@router.get("/{city_id}/city_details")
def get_city_details(
    city_id: int,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username = payload.get("sub")
    player = get_player_by_username(db, username)
    city = db.query(City).filter(City.id == city_id, City.player_id == player.id).first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return {
        "id": city.id,
        "name": city.name,
        "x": city.x,
        "y": city.y,
        "resources": {
            "steel": city.steel,
            "oil": city.oil,
            "rubber": city.rubber,
            "food": city.food,
            "gold": city.gold,
        },
        "rates": {
            "steel_rate": city.steel_rate,
            "oil_rate": city.oil_rate,
            "rubber_rate": city.rubber_rate,
            "food_rate": city.food_rate,
            "gold_rate": city.gold_rate,
        },
        "storage_caps": {
            "steel": city.max_steel,
            "oil": city.max_oil,
            "rubber": city.max_rubber,
            "food": city.max_food,
            "gold": city.max_gold,
        },
        "last_collected_at": city.last_collected_at,
        "created_at": city.created_at,
        "population": getattr(city, "population", None)
    }

# Update city rates
@router.patch("/{city_id}/update_rates")
def update_city_rates(
    city_id: int,
    rates: dict = Body(...),
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username = payload.get("sub")
    player = get_player_by_username(db, username)
    city = db.query(City).filter(City.id == city_id, City.player_id == player.id).first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    # Update only provided rates
    for field in ["steel_rate", "oil_rate", "rubber_rate", "food_rate", "gold_rate"]:
        if field in rates:
            setattr(city, field, rates[field])

    db.commit()
    db.refresh(city)
    return {
        "msg": "City rates updated",
        "rates": {
            "steel_rate": city.steel_rate,
            "oil_rate": city.oil_rate,
            "rubber_rate": city.rubber_rate,
            "food_rate": city.food_rate,
            "gold_rate": city.gold_rate,
        }
    }

# Delete city
@router.delete("/{city_id}/delete")
def delete_city(
    city_id: int,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username = payload.get("sub")
    player = get_player_by_username(db, username)
    city = db.query(City).filter(City.id == city_id, City.player_id == player.id).first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    db.delete(city)
    db.commit()
    return {"msg": f"City '{city.name}' deleted successfully."}

# Build or upgrade a building in the city
@router.post("/{city_id}/build")
def construct_building(
    city_id: int,
    building_type: str = Body(..., embed=True),
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username = payload.get("sub")
    player = get_player_by_username(db, username)
    city = db.query(City).filter(City.id == city_id, City.player_id == player.id).first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    # Check if building already exists
    building = db.query(Building).filter_by(city_id=city.id, type=building_type).first()
    now = datetime.now(timezone.utc)
    build_time = timedelta(minutes=5)  # Example: 5 minutes per level, adjust as needed

    if building:
        # Upgrade existing building
        building.level += 1
        building.construction_started_at = now
        building.construction_finished_at = now + build_time
        msg = f"{building_type} upgraded to level {building.level}."
    else:
        # Create new building
        building = Building(
            city_id=city.id,
            type=building_type,
            level=1,
            construction_started_at=now,
            construction_finished_at=now + build_time
        )
        db.add(building)
        msg = f"{building_type} construction started."

    db.commit()
    db.refresh(building)
    return {
        "msg": msg,
        "building": {
            "type": building.type,
            "level": building.level,
            "construction_started_at": building.construction_started_at,
            "construction_finished_at": building.construction_finished_at
        }
    }