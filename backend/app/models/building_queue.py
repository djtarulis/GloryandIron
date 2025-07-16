from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from ..db.session import Base

class BuildingQueue(Base):
    __tablename__ = "building_queues"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)
    building_id = Column(Integer, ForeignKey("buildings.id"), nullable=False)
    type = Column(String, nullable=False)  # e.g., "Barracks", "Factory"
    level = Column(Integer, default=1)
    quantity = Column(Integer, nullable=False)
    building_started_at = Column(DateTime, nullable=False)
    building_finishes_at = Column(DateTime, nullable=False)
    finished = Column(Integer, default=0)  # 0 = in progress, 1 = finished