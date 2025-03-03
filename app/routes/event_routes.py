import globals
from app.database import get_db
from sqlalchemy.orm import Session
from app.auth import get_current_user
from fastapi import APIRouter, Depends
from typing import List, Optional
from datetime import datetime
from app.models import Event, EventStatus
from app.schemas import EventCreate, EventUpdate, EventResponse
from app.exceptions import EventNotFoundException, InvalidInputException, EventsNotFoundException


router = APIRouter()


@router.post("/create/", response_model=EventResponse)
def create_event(event: EventCreate, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    if event.max_attendees <= 0:
        raise InvalidInputException(globals.MAX_ATTENDEES_MUST_BE_GREATER_THAN_0)

    new_event = Event(**event.dict())
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event


@router.put("/{event_id}/update/", response_model=EventResponse)
def update_event(event_id: int, event_update: EventUpdate, db: Session = Depends(get_db), user: str = Depends(get_current_user)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise EventNotFoundException(event_id)

    for key, value in event_update.dict(exclude_unset=True).items():
        setattr(event, key, value)
    
    db.commit()
    db.refresh(event)
    return event



@router.get("/{event_id}")
def get_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise EventNotFoundException(event_id)
    return event




@router.get("/", response_model=List[EventResponse])
def list_events(
    status: Optional[str] = None,
    location: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    search: str = None, 
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    query = db.query(Event)

    if status:
        query = query.filter(Event.status == status)
    if location:
        query = query.filter(Event.location.ilike(f"%{location}%"))
    if start_date:
        query = query.filter(Event.start_time >= start_date)
    if end_date:
        query = query.filter(Event.end_time <= end_date)

    if search:
        query = query.filter(Event.name.ilike(f"%{search}%"))

    events = query.offset(skip).limit(limit).all()
    if not events:
        raise EventsNotFoundException()
    return events