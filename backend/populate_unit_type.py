from app.models.unit_type import UnitType
from app.db.session import SessionLocal

db = SessionLocal()

rifleman = UnitType(
    name="Rifleman",
    base_training_time=180,  # seconds
    base_attack=10,
    base_defense=5,
    base_cost={"steel": 100, "food": 30},
    base_speed=1.0,
    base_carry_capacity=10,
    base_range=1,
    base_life=100,
    population_cost=1,
    upkeep_cost=1,
    unit_type="Infantry",
    description="Basic infantry unit"
)

db.add(rifleman)
db.commit()
db.close()
print("Unit types populated!")