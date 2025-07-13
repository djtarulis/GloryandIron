import datetime
from sqlalchemy import Column, ForeignKey, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from ..db.session import Base
from sqlalchemy.sql import func

class Unit(Base):
    __tablename__ = "units"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("cities.id"))
    type = Column(String, index=True)  # e.g., "Infantry", "Tank"
    quantity = Column(Integer, default=0)

    unit = relationship("City", back_populates="units")