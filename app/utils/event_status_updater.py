from sqlalchemy.orm import Session
from datetime import datetime
from app.models import Event, EventStatus

def update_event_status(db: Session):
    now = datetime.utcnow()
    events = db.query(Event).filter(Event.end_time < now, Event.status != EventStatus.completed).all()

    for event in events:
        event.status = EventStatus.completed
        db.commit()

    return {"message": "Event statuses updated successfully"}
