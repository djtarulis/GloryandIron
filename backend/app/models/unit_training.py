from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from ..db.session import Base

class UnitTraining(Base):
    __tablename__ = "unit_training"

    id = Column(Integer, primary_key=True, autoincrement=True)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)
    unit_type = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    training_started_at = Column(DateTime, nullable=False)
    training_finishes_at = Column(DateTime, nullable=False)
    finished = Column(Integer, default=0)  # 0 = in progress, 1 = finished