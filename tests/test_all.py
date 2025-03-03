import sys
import os
import pytest
from app.database import get_db
from datetime import datetime, timedelta
from app.models import Event, Attendee, EventStatus
from app.utils.event_status_updater import update_event_status

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")


from main import client



def test_signup():
    response = client.post("/user/signup/", json={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 200
    assert response.json() == 200
    assert "id" in response.json()
    assert "token" in response.json()


def test_login():
    response = client.post("/user/login/", json={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 200
    assert response.json() == 200
    assert "token" in response.json()


def test_duplicate_user():
    client.post("/user/signup/", json={"username": "testuser", "password": "testpassword"})
    response = client.post("/user/signup/", json={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 400

def test_protected_route_without_token():
    response = client.get("/user/check/")
    assert response.status_code in [401, 403]

def test_protected_route_with_token():
    login_response = client.post("/user/login/", json={"username": "testuser", "password": "testpassword"})
    token = login_response.json().get("token")

    assert token is not None

    response = client.get("/user/check/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert "message" in response.json()





# Test event
def test_create_event():
    # Login to get a valid token
    login_response = client.post("/user/login/", json={"username": "testuser", "password": "testpassword"})
    token = login_response.json().get("token")
    assert token is not None

    # Create event with token
    response = client.post("/event/create/", json={
        "name": "Test Tech Conference",
        "description": "A conference for tech enthusiasts.",
        "start_time": "2024-08-10T10:00:00",
        "end_time": "2024-08-10T18:00:00",
        "location": "New York",
        "max_attendees": 100
    }, headers={"Authorization": f"Bearer {token}"})
    
    assert response.status_code == 200
    assert "id" in response.json()




# Test registration
@pytest.fixture
def setup_event():
    """Create an event with a max limit of 2 attendees."""
    db = next(get_db())
    event = Event(
        name="Test Event",
        description="A test event",
        start_time=datetime.strptime("2024-12-01T10:00:00", "%Y-%m-%dT%H:%M:%S"),
        end_time=datetime.strptime("2024-12-01T12:00:00", "%Y-%m-%dT%H:%M:%S"),
        location="Test Location",
        max_attendees=2
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


def test_registration_limit(setup_event):
    event_id = setup_event.id

    response1 = client.post(f"/attendees/{event_id}/register/", json={
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "phone_number": "1234567890",
        "event_id": event_id
    })
    response2 = client.post(f"/attendees/{event_id}/register/", json={
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane@example.com",
        "phone_number": "0987654321",
        "event_id": event_id
    })
    
    assert response1.status_code == 200
    assert response2.status_code == 200

    # Register a 3rd attendee (should be denied)
    response3 = client.post(f"/attendees/{event_id}/register/", json={
        "first_name": "Alice",
        "last_name": "Smith",
        "email": "alice@example.com",
        "phone_number": "1122334455",
        "event_id": event_id
    })
    
    assert response3.status_code == 400
    assert response3.json()["error"] == "Event is fully booked"



# Test checkin

def test_attendee_checkin(setup_event):
    event_id = setup_event.id

    # Register an attendee
    response = client.post(f"/attendees/{event_id}/register/", json={
        "first_name": "Test",
        "last_name": "User",
        "email": "test@example.com",
        "phone_number": "5555555555"
    })
    attendee_id = response.json().get("id")

    assert attendee_id is not None
    
    # First check-in (should succeed)
    checkin_response1 = client.put(f"/attendees/{attendee_id}/check-in/")
    assert checkin_response1.status_code == 200
    assert checkin_response1.json()["message"] == f"Attendee {attendee_id} checked in successfully"

    # Second check-in (should fail)
    checkin_response2 = client.put(f"/attendees/{attendee_id}/check-in/")
    assert checkin_response2.status_code == 400
    assert checkin_response2.json()["detail"] == "Attendee is already checked in"



# Test event status
def test_auto_event_status_update():
    """Test if events past their end time are marked as completed."""
    db = next(get_db())

    # Create a past event
    past_event = Event(
        name="Past Event",
        description="This event should be marked as completed",
        start_time=datetime.now() - timedelta(days=2),
        end_time=datetime.now() - timedelta(days=1),
        location="Test Location",
        max_attendees=50,
        status=EventStatus.scheduled  # Initially set as scheduled
    )
    db.add(past_event)
    db.refresh(past_event)
    db.commit()

    update_event_status(db)

    updated_event = db.query(Event).filter(Event.id == past_event.id).first()
    assert updated_event.status == EventStatus.completed
