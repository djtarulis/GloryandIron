from apscheduler.schedulers.background import BackgroundScheduler
from app.db.session import SessionLocal
from app.models.unit_training import UnitTraining
from app.models.unit import Unit
from datetime import datetime, timezone
import time

def process_unit_training():
    db = SessionLocal()
    now = datetime.now(timezone.utc)
    trainings = db.query(UnitTraining).filter(
        UnitTraining.training_finishes_at <= now,
        UnitTraining.finished == 0
    ).all()
    for training in trainings:
        # Add units to garrison
        unit = db.query(Unit).filter_by(
            city_id=training.city_id,
            type=training.unit_type,
            moving=0
        ).first()
        if unit:
            unit.quantity += training.quantity
        else:
            unit = Unit(
                city_id=training.city_id,
                type=training.unit_type,
                quantity=training.quantity,
                moving=0
            )
            db.add(unit)
        training.finished = 1
        db.commit()
    db.close()

if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    scheduler.add_job(process_unit_training, "interval", seconds=2)  # Check every 2 seconds
    scheduler.start()
    print("Unit training worker started. Press Ctrl+C to exit.")
    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()