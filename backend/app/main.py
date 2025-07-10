from fastapi.middleware.cors import CORSMiddleware
from .db.session import engine, Base, get_db
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from jose import JWTError, jwt
from datetime import datetime, timedelta
from .models.player import Player
from .models.city import City

from app.routes.auth import (
    get_player_by_username,
    get_password_hash,
    authenticate_user,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    oauth2_scheme,
    SECRET_KEY,
    ALGORITHM,
)

app = FastAPI()

origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

router = APIRouter()

@router.post("/register")
def register(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_player_by_username(db, form_data.username)
    if user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(form_data.password)
    new_user = Player(username=form_data.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"msg": "User registered"}

@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me")
def read_users_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_player_by_username(db, username)
    if user is None:
        raise credentials_exception
    return {"username": user.username}

@router.post("/city/create")
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
    city = City(name=name, player_id=player.id, x=x, y=y)
    db.add(city)
    db.commit()
    db.refresh(city)
    return {"msg": "City created", "city_id": city.id}

@router.get("/cities")
def list_cities(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username = payload.get("sub")
    player = get_player_by_username(db, username)
    if not player:
        raise HTTPException(status_code=401, detail="Invalid user")
    return {"cities": [{"id": c.id, "name": c.name, "x": c.x, "y": c.y} for c in player.cities]}


@router.post("/city/{city_id}/collect")
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

    now = datetime.now(datetime.timezone.utc)
    elapsed_hours = (now - city.last_collected_at).total_seconds() / 3600

    # Example static rates
    steel_rate = 100.0  # per hour
    oil_rate = 80.0
    rubber_rate = 60.0
    food_rate = 120.0
    gold_rate = 50.0

    city.steel += float(steel_rate * elapsed_hours)
    city.oil += float(oil_rate * elapsed_hours)
    city.rubber += float(rubber_rate * elapsed_hours)
    city.food += float(food_rate * elapsed_hours)
    city.gold += float(gold_rate * elapsed_hours)
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


app.include_router(router)