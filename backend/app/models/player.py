from sqlalchemy import Column, String, Integer
from ..db.session import Base
from sqlalchemy.orm import relationship


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    cities = relationship("City", back_populates="player")