import json
from app.models.unit_type import UnitType
from app.db.session import SessionLocal

with open("backend/populate_tables/unit_types.json", "r") as f:
    unit_types_data = json.load(f)

db = SessionLocal()
for unit_data in unit_types_data:
    unit = UnitType(**unit_data)
    db.add(unit)
db.commit()
db.close()
print("Unit types populated!")