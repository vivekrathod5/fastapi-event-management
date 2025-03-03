from fastapi import Depends
from app.config import DATABASE_URL
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from sqlalchemy import create_engine, MetaData


engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata = MetaData()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()
