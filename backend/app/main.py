from fastapi.middleware.cors import CORSMiddleware
from .db.session import engine, Base
from fastapi import FastAPI, APIRouter
from app.routes.city import router as city_router
from app.routes.auth import router as auth_router

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


app.include_router(auth_router)
app.include_router(city_router)