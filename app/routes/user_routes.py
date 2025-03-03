from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import UserCreate
from app.utils.hashing import hash_password, verify_password
from app.auth import create_jwt_token, get_current_user
from app.exceptions import UserExistsException, InvalidCredentialsException

router = APIRouter()

@router.post("/signup/")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise UserExistsException()

    hashed_password = hash_password(user.password)
    new_user = User(username=user.username, password=hashed_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_jwt_token(str(new_user.id))
    return {"id": new_user.id, "username": new_user.username, "token": token}


@router.post("/login/")
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise InvalidCredentialsException()

    token = create_jwt_token(str(db_user.id))
    return {"id": db_user.id, "username": db_user.username, "token": token}


@router.get("/check/")
def protected_route(user: str = Depends(get_current_user)):
    return {"message": f"Hello {user}, you have access!"}
