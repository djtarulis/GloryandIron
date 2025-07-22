from sqlalchemy import Column, Integer, String, Float
from ..db.session import Base
from sqlalchemy.dialects.postgresql import JSONB

class BuildingType(Base):
    __tablename__ = "building_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)  # e.g., "Barracks", "Factory"
    description = Column(String, nullable=True)
    level = Column(Integer, default=1)
    cost = Column(JSONB, default=dict)  # Cost in resources (e.g., {"wood": 100, "stone": 50})
    build_time = Column(Float, nullable=False)  # Time in seconds to build
    max_level = Column(Integer, default=10)  # Maximum level for this building type
    resource_production = Column(JSONB, default=dict)  # Resource production per level, e.g. {"wood": 10, "stone": 5}
    population_capacity = Column(Integer, default=0)  # Population capacity provided by this building
    required_buildings = Column(JSONB, default=dict)  # Required buildings to unlock this type
    required_research = Column(String, default=None)  # Required research to unlock this building
    special_ability = Column(String, default=None)  # Special ability of the building (e.g., "Defense Boost")

    def __repr__(self):
        return (
            f"<BuildingType("
            f"id={self.id}, "
            f"name={self.name}, "
            f"description={self.description}, "
            f"level={self.level}, "
            f"cost={self.cost}, "
            f"build_time={self.build_time}, "
            f"max_level={self.max_level}, "
            f"resource_production={self.resource_production}, "
            f"population_capacity={self.population_capacity}, "
            f"required_buildings={self.required_buildings}, "
            f"required_research={self.required_research}, "
            f"special_ability={self.special_ability}"
            f")>"
        )