import datetime
from sqlalchemy import Column, ForeignKey, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from ..db.session import Base
from sqlalchemy.sql import func

class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, autoincrement=True)
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

    # Coordinates ----
    x = Column(Integer, nullable=False)
    y = Column(Integer, nullable=False)

    # Buildings ----
    buildings = relationship("Building", back_populates="city")
    
    ### WAREHOUSE PROPERTIES ----
    @property
    def warehouse_level(self):
        warehouse = next((b for b in self.buildings if b.type == "Warehouse"), None)
        return warehouse.level if warehouse else 0

    @property
    def max_steel(self):
        return 10000 + self.warehouse_level * 5000

    @property
    def max_oil(self):
        return 10000 + self.warehouse_level * 5000

    @property
    def max_rubber(self):
        return 10000 + self.warehouse_level * 5000

    @property
    def max_food(self):
        return 10000 + self.warehouse_level * 5000

    @property
    def max_gold(self):
        return 10000 + self.warehouse_level * 2000
    
    ### BARRACKS PROPERTIES ----
    @property
    def barracks_level(self):
        barracks = next((b for b in self.buildings if b.type == "Barracks"), None)
        return barracks.level if barracks else 0
    
    @property
    def max_capacity(self):
        return 2000 + self.barracks_level * 500
    
    @property
    def training_rate(self):
        return 1.0 + (self.barracks_level * 0.1)
    
    @property
    def unlocked_troop_types(self):
    # Example: unlocks new troop types at certain levels
        troop_unlocks = {
            1: ["Rifleman"],
            1: ["Medic"],
            1: ["Engineer"],
            1: ["Machine Gunner"],
            2: ["Scout"],
            2: ["Grenadier"],
            3: ["Automatic Rifleman"],
            2: ["Anti-Tank Gun"],
            4: ["Sniper"],
            3: ["Mortar"],
            4: ["Flamethrower"],
        }
        unlocked = set()
        for lvl, types in troop_unlocks.items():
            if self.barracks_level >= lvl:
                unlocked.update(types)
        return list(unlocked)

    @property
    def training_queue_size(self):
        # Example: base 1, +1 per 5 levels
        return 1 + (self.barracks_level // 5)
    
    # Units ----
    units = relationship("Unit", back_populates="city")

    # Timestamps ----
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_collected_at = Column(DateTime(timezone=True), server_default=func.now())

    # Defenses
    # defenses = relationship("Defense", back_populates="city")
    # TODO: Add defense relationships for each type of defense

    # Population ----
    population = Column(Integer, default=0)