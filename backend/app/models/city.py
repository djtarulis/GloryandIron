import datetime
from sqlalchemy import Column, ForeignKey, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from ..db.session import Base
from sqlalchemy.sql import func

class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    player_id = Column(Integer, ForeignKey("players.id"))
    player = relationship("Player", back_populates="cities")
    
    # Resources ----
    steel = Column(Integer, default=0)
    steel_rate = Column(Float, default=0.0)

    oil = Column(Integer, default=0)
    oil_rate = Column(Float, default=0.0)

    rubber = Column(Integer, default=0)
    rubber_rate = Column(Float, default=0.0)

    food = Column(Integer, default=0)
    food_rate = Column(Float, default=0.0)

    gold = Column(Integer, default=0)
    gold_rate = Column(Float, default=0.0)

    last_collected_at = Column(DateTime(timezone=True), server_default=func.now())
    now = datetime.utcnow()
    elapsed_hours = (now - last_collected_at).total_seconds() / 3600
    
    produced_steel = city.steel_rate * elapsed_hours
    produced_oil = city.oil_rate * elapsed_hours
    produced_rubber = city.rubber_rate * elapsed_hours
    produced_food = city.food_rate * elapsed_hours
    produced_gold = city.gold_rate * elapsed_hours

    # Coordinates ----
    x = Column(Integer, nullable=False)
    y = Column(Integer, nullable=False)

    # Buildings ----
    # buildings = relationship("Building", back_populates="city")
    #TODO: Add building relationships for each type of building

    # Troops ----
    # troops = relationship("Troop", back_populates="city")
    #TODO: Add troop relationships for each type of troop

    # Timestamps ----
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_collected_at = Column(DateTime(timezone=True), server_default=func.now())

    # Defenses
    # defenses = relationship("Defense", back_populates="city")
    # TODO: Add defense relationships for each type of defense

    # Population ----
    population = Column(Integer, default=0)