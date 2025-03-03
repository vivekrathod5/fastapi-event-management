from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.routes import user_routes, event_routes, attendee_routes
from app.database import Base, engine
from app.exceptions import BaseAPIException
from app.database import get_db
# from apscheduler.schedulers.background import BackgroundScheduler
from app.utils.event_status_updater import update_event_status
from fastapi.testclient import TestClient





app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(user_routes.router, prefix="/user")
app.include_router(event_routes.router, prefix="/event")
app.include_router(attendee_routes.router, prefix="/attendees")

client = TestClient(app)

@app.exception_handler(BaseAPIException)
async def base_api_exception_handler(request: Request, exc: BaseAPIException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )



# Scheduler to update event status every 1 hour
# scheduler = BackgroundScheduler()
# scheduler.add_job(update_event_status, "interval", hours=1, args=[next(get_db())])
# scheduler.start()