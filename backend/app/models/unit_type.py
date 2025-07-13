from sqlalchemy import Column, Integer, String, Float
from ..db.session import Base
from sqlalchemy.dialects.postgresql import JSONB


class UnitType(Base):
    __tablename__ = "unit_types"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)  # e.g., "Rifleman"
    base_training_time = Column(Float, nullable=False)   # seconds per unit
    base_attack = Column(Integer, default=0)  # Base attack value
    base_defense = Column(Integer, default=0)  # Base defense value
    base_cost = Column(JSONB, default=dict)  # Base cost in resources, e.g. {"steel": 100, "oil": 50, "food": 30}
    base_speed = Column(Float, default=1.0)  # Speed of the unit (could be in tiles per second)
    base_carry_capacity = Column(Integer, default=0)  # Carry capacity for resources
    base_range = Column(Integer, default=1)  # Range of the unit (for ranged units)
    base_life = Column(Integer, default=100)  # Hit points or life of the unit
    population_cost = Column(Integer, default=1)  # Population cost for the unit
    upkeep_cost = Column(Integer, default=0)  # Upkeep cost per unit (
    unit_type = Column(String, default="")  # e.g., Infantry, Tank, Artillery
    description = Column(String, default="")  # Description of the unit type
    unlock_requirements = Column(String, default=None)  # JSON or string for required buildings/research
    required_building = Column(String, default=None)  # Required building to train this unit
    required_research = Column(String, default=None)  # Required research to unlock this unit
    special_ability = Column(String, default=None)  # Special ability of the unit (e.g., "Stealth", "Healing")
    

    def __repr__(self):
        return (
            f"<UnitType("
            f"id={self.id}, "
            f"name={self.name}, "
            f"base_training_time={self.base_training_time}, "
            f"base_attack={self.base_attack}, "
            f"base_defense={self.base_defense}, "
            f"base_cost={self.base_cost}, "
            f"base_speed={self.base_speed}, "
            f"base_carry_capacity={self.base_carry_capacity}, "
            f"base_range={self.base_range}, "
            f"base_life={self.base_life}, "
            f"population_cost={self.population_cost}, "
            f"upkeep_cost={self.upkeep_cost}, "
            f"unit_type={self.unit_type}, "
            f"description={self.description}, "
            f"unlock_requirements={self.unlock_requirements}, "
            f"required_building={self.required_building}, "
            f"required_research={self.required_research}, "
            f"special_ability={self.special_ability}"
            f")>"
        )