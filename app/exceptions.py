import globals
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request, HTTPException

app = FastAPI()



class BaseAPIException(HTTPException):
    def __init__(self, status_code: int, message: str):
        super().__init__(status_code=status_code, detail=message)


class InvalidCredentialsException(BaseAPIException):
    def __init__(self):
        super().__init__(401, globals.INVALID_CREDENTIALS)

class UserExistsException(BaseAPIException):
    def __init__(self):
        super().__init__(400, globals.USERNAME_TAKEN)

class UserNotFoundException(BaseAPIException):
    def __init__(self):
        super().__init__(404, globals.USER_NOT_FOUND)

class EventNotFoundException(BaseAPIException):
    def __init__(self, event_id: int):
        super().__init__(404, globals.EVENT_NOT_FOUND)

class EventsNotFoundException(BaseAPIException):
    def __init__(self):
        super().__init__(400, globals.EVENTS_NOT_FOUND)

class AttendeeNotFoundException(BaseAPIException):
    def __init__(self, attendee_id: int):
        super().__init__(404, globals.ATTENDEE_NOT_FOUND)

class MaxAttendeeLimitReachedException(BaseAPIException):
    def __init__(self):
        super().__init__(400, globals.EVENT_IS_FULL_BOOKED)


class AttendeeExistsException(BaseAPIException):
    def __init__(self):
        super().__init__(400, globals.ATTENDEE_FOUND)

class InvalidInputException(BaseAPIException):
    def __init__(self, message=globals.INVALID_INPUT):
        super().__init__(400, message)


class AttendeeAlreadyCheckInException(BaseAPIException):
    def __init__(self):
        super().__init__(400, globals.ATTENDEE_ALREADY_CHECK_IN)

class AttendeesNotFoundException(BaseAPIException):
    def __init__(self):
        super().__init__(404, globals.ATTENDEES_NOT_FOUND)