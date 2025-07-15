from sqlalchemy import Column, ForeignKey, String, Integer
from ..db.session import Base
from sqlalchemy.orm import relationship


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    active_city_id = Column(Integer, ForeignKey("cities.id"), nullable=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    cities = relationship("City", back_populates="player", foreign_keys="[City.player_id]")