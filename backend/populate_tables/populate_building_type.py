import json
from app.models.building_type import BuildingType
from app.db.session import SessionLocal

with open("populate_tables/building_types.json", "r") as f:
    building_types_data = json.load(f)

db = SessionLocal()
for building_data in building_types_data:
    building = BuildingType(**building_data)
    db.add(building)
db.commit()
db.close()
print("Building types populated!")