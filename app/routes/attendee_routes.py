import globals
from app.database import get_db
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models import Attendee, Event
from fastapi import APIRouter, Depends
from app.auth import get_current_user
from app.schemas import AttendeeCreate, AttendeeResponse
from app.exceptions import (
    AttendeeNotFoundException, 
    MaxAttendeeLimitReachedException, 
    EventNotFoundException,
    AttendeeExistsException,
    AttendeeAlreadyCheckInException,
    AttendeesNotFoundException,
)


router = APIRouter()


@router.post("/{event_id}/register/")
def register_attendee(event_id: int, attendee: AttendeeCreate, db: Session = Depends(get_db)):

    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise EventNotFoundException(event_id)
    is_exists = db.query(Attendee).filter(
        Attendee.event_id == event_id, 
        Attendee.email == attendee.email
    ).first()
    if is_exists:
        raise AttendeeExistsException()
    count = db.query(Attendee).filter(Attendee.event_id == event_id).count()
    if count >= event.max_attendees:
        raise MaxAttendeeLimitReachedException()

    new_attendee = Attendee(**attendee.dict())
    db.add(new_attendee)
    db.commit()
    db.refresh(new_attendee)
    return new_attendee



@router.get("/{attendee_id}")
def get_attendee(attendee_id: int, db: Session = Depends(get_db)):
    attendee = db.query(Attendee).filter(Attendee.id == attendee_id).first()
    if not attendee:
        raise AttendeeNotFoundException(attendee_id)
    return attendee



@router.put("/{attendee_id}/check-in/")
def check_in_attendee(attendee_id: int, db: Session = Depends(get_db)):
    attendee = db.query(Attendee).filter(Attendee.id == attendee_id).first()
    if not attendee:
        raise AttendeeNotFoundException(attendee_id)

    if attendee.check_in_status:
        raise AttendeeAlreadyCheckInException()

    attendee.check_in_status = True
    db.commit()
    return {"message": f"Attendee {attendee_id} checked in successfully"}




@router.get("/{event_id}/attendees/", response_model=List[AttendeeResponse])
def list_attendees(
    event_id: int,
    checked_in: Optional[bool] = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db), 
    user: str = Depends(get_current_user)
):
    query = db.query(Attendee).filter(Attendee.event_id == event_id)

    if checked_in is not None:
        query = query.filter(Attendee.check_in_status == checked_in)

    attendees = query.offset(skip).limit(limit).all()
    if not attendees:
        raise AttendeesNotFoundException()
    return attendees