from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from jose import jwt
from datetime import datetime, timedelta, timezone

from app.models.building_queue import BuildingQueue
from app.models.building_type import BuildingType
from app.db.session import get_db
from app.models.city import City
from app.models.building import Building
from app.models.unit import Unit
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
    
    # Prevent duplicate city coordinates
    existing_city = db.query(City).filter(City.x == x, City.y == y).first()
    if existing_city:
        raise HTTPException(status_code=400, detail="A city already exists at these coordinates.")

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

    # Set active_city_id to this city if it's the player's first city
    if is_first_city:
        player.active_city_id = city.id
        db.commit()
        db.refresh(player)

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
    if not player:
        raise HTTPException(status_code=401, detail="Invalid user")
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

    # Store previous resource totals
    prev_resources = {
        "steel": city.steel,
        "oil": city.oil,
        "rubber": city.rubber,
        "food": city.food,
        "gold": city.gold,
    }

    city.steel = min(city.steel + float(steel_rate * elapsed_hours), city.max_steel)
    city.oil = min(city.oil + float(oil_rate * elapsed_hours), city.max_oil)
    city.rubber = min(city.rubber + float(rubber_rate * elapsed_hours), city.max_rubber)
    city.food = min(city.food + float(food_rate * elapsed_hours), city.max_food)
    city.gold = min(city.gold + float(gold_rate * elapsed_hours), city.max_gold)
    city.last_collected_at = now

    db.commit()
    db.refresh(city)

    # Calculate collected amounts
    collected = {
        "steel": city.steel - prev_resources["steel"],
        "oil": city.oil - prev_resources["oil"],
        "rubber": city.rubber - prev_resources["rubber"],
        "food": city.food - prev_resources["food"],
        "gold": city.gold - prev_resources["gold"],
    }

    return {
        "msg": "Resources collected",
        "collected": collected,
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
    if not player:
        raise HTTPException(status_code=401, detail="Invalid user")
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
        "buildings": [
            {
                "type": b.type,
                "level": b.level,
                "construction_started_at": b.construction_started_at,
                "construction_finished_at": b.construction_finished_at
            } for b in city.buildings
        ],
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
    if not player:
        raise HTTPException(status_code=401, detail="Invalid user")
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
    if not player:
        raise HTTPException(status_code=401, detail="Invalid user")
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
    if not player:
        raise HTTPException(status_code=401, detail="Invalid user")
    city = db.query(City).filter(City.id == city_id, City.player_id == player.id).first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    building_type_obj = db.query(BuildingType).filter(BuildingType.name == building_type).first()
    if not building_type_obj:
        raise HTTPException(status_code=400, detail="Invalid building type")

    # Check if there's an existing building queue entry for this city and type that is not finished
    existing_queue = db.query(BuildingQueue).filter_by(
        city_id=city.id,
        type=building_type,
        finished=0
    ).first()
    if existing_queue:
        raise HTTPException(status_code=400, detail="Building is already in progress or in the queue.")

    # Check if building already exists
    building = db.query(Building).filter_by(city_id=city.id, type=building_type).first()
    now = datetime.now(timezone.utc)
    build_time = timedelta(minutes=5)  # Example: 5 minutes per level, adjust as needed

    # Handle cases where the building is already finished and at max level
    if building and building.level >= building_type_obj.max_level:
        raise HTTPException(status_code=400, detail="Building is already at max level.")

    if building:
        # Upgrade existing building
        building.level += 1
        building.construction_started_at = now
        building.construction_finished_at = now + build_time
        msg = f"{building_type} upgraded to level {building.level}."
        db.add(building)
        building_id = building.id
        queue_level = building.level
    else:
        # Create new building first
        new_building = Building(
            city_id=city.id,
            type=building_type,
            level=1,
            construction_started_at=now,
            construction_finished_at=now + build_time
        )
        db.add(new_building)
        db.commit()
        db.refresh(new_building)
        building_id = new_building.id
        queue_level = 1

    # Add building to the queue
    building_queue = BuildingQueue(
        city_id=city.id,
        building_id=building_id,
        type=building_type,
        level=queue_level,
        quantity=1,
        building_started_at=now,
        building_finishes_at=now + build_time,
        finished=0
    )
    db.add(building_queue)
    msg = f"{building_type} construction started."
    db.commit()
    db.refresh(building_queue)

    return {
        "msg": msg,
        "building": {
            "city_id": city.id,
            "building_id": building_id,
            "type": building_type,
            "level": queue_level,
            "construction_started_at": now,
            "construction_finished_at": now + build_time
        }
    }

@router.get("/city/{city_id}/garrison")
def get_city_garrison(
    city_id: int,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username = payload.get("sub")
    player_obj = get_player_by_username(db, username)
    if not player_obj:
        raise HTTPException(status_code=401, detail="Invalid user")
    city = db.query(City).filter(City.id == city_id, City.player_id == player_obj.id).first()
    if not city:
        raise HTTPException(status_code=403, detail="Not authorized to view this city garrison")

    # Only show units with quantity > 0
    garrison = db.query(Unit).filter(
        Unit.city_id == city_id,
        Unit.moving == 0,
        Unit.quantity > 0
    ).all()
    

    return {"city_id": city_id, "garrison": [
        {
            "unit_id": unit.id,
            "type": unit.type,
            "quantity": unit.quantity,
            "x": unit.x,
            "y": unit.y
        } for unit in garrison
    ]}

@router.post("/switch_active_city")
def switch_active_city(
    city_id: int,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    """
    Switch the user's active city. Stores the active city_id in the player's profile.
    """
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username = payload.get("sub")
    player = get_player_by_username(db, username)
    if not player:
        raise HTTPException(status_code=401, detail="Invalid user")

    city = db.query(City).filter(City.id == city_id, City.player_id == player.id).first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found or not owned by user")

    # Store the active city_id in the player profile (assumes 'active_city_id' column exists)
    player.active_city_id = city_id
    db.commit()
    db.refresh(player)

    return {"msg": f"Active city switched to '{city.name}'", "active_city_id": city_id}