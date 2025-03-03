from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str


    class Config:
        from_attributes = True

# Event

class EventBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100, description="Event Name")
    description: Optional[str] = Field(None, max_length=500, description="Short description of the event")
    start_time: datetime = Field(..., description="Event Start Time (ISO 8601 Format)")
    end_time: datetime = Field(..., description="Event End Time (ISO 8601 Format)")
    location: str = Field(..., min_length=3, max_length=200, description="Event Location")
    max_attendees: int = Field(..., ge=1, description="Maximum number of attendees")

class EventCreate(EventBase):
    pass  # Same fields as EventBase for creating an event


class EventUpdate(EventBase):
    name: Optional[str] = Field(None, min_length=3, max_length=100, description="Updated event name")
    description: Optional[str] = Field(None, max_length=500, description="Updated event description")
    start_time: Optional[datetime] = Field(None, description="Updated event start time")
    end_time: Optional[datetime] = Field(None, description="Updated event end time")
    location: Optional[str] = Field(None, min_length=3, max_length=200, description="Updated event location")
    max_attendees: Optional[int] = Field(None, ge=1, description="Updated maximum number of attendees")


class EventResponse(EventBase):
    id: int 
    class Config:
        from_attributes = True 


# Attendee
class AttendeeBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str


class AttendeeCreate(AttendeeBase):
    event_id: int


class AttendeeResponse(AttendeeBase):
    id: int
    event_id: int
    check_in_status: bool = False

    class Config:
        from_attributes = True
