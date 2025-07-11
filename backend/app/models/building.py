from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from app.db.session import Base
from sqlalchemy.orm import relationship
from datetime import datetime, timezone


class Building(Base):
    __tablename__ = "buildings"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("cities.id"))
    type = Column(String, index=True)  # e.g., "Headquarters", "Barracks"
    level = Column(Integer, default=1)
    construction_started_at = Column(DateTime(timezone=True), nullable=True)
    construction_finished_at = Column(DateTime(timezone=True), nullable=True)

    city = relationship("City", back_populates="buildings")