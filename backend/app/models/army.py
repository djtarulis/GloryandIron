from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from ..db.session import Base
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.dialects.postgresql import JSONB

class Army(Base):
    __tablename__ = "armies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey("players.id"))
    origin_city_id = Column(Integer, ForeignKey("cities.id"))
    origin_x = Column(Integer)
    origin_y = Column(Integer)
    destination_x = Column(Integer)
    destination_y = Column(Integer)
    units = Column(MutableDict.as_mutable(JSONB), default=dict)   # For tracking changes to units dict in army 
    departure_time = Column(DateTime)
    arrival_time = Column(DateTime)
    status = Column(String, default="marching")  # marching, arrived, returning, etc.
    mission = Column(String, default="attack")   # attack, reinforce, scout, etc.
    battle_result = Column(JSON, nullable=True)  # Store battle outcome if needed

    owner = relationship("Player")
    origin_city = relationship("City")