from sqlalchemy import Column, ForeignKey, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from ..db.session import Base

class Unit(Base):
    __tablename__ = "units"

    id = Column(Integer, primary_key=True, index=True)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=True)  # Nullable
    type = Column(String, index=True)  # e.g., "Rifleman", "Tank"
    quantity = Column(Integer, default=0)

    # Location on the map
    x = Column(Integer, nullable=True)
    y = Column(Integer, nullable=True)

    # Movement tracking
    destination_x = Column(Integer, nullable=True)
    destination_y = Column(Integer, nullable=True)
    moving = Column(Integer, default=0)  # 0 = stationary, 1 = moving
    arrival_time = Column(DateTime, nullable=True)

    city = relationship("City", back_populates="units")

    def __repr__(self):
        return f"<Unit(type={self.type}, quantity={self.quantity}, x={self.x}, y={self.y})>"