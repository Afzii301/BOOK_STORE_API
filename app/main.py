from fastapi import FastAPI
from app.routers import auth
from app.database import SessionLocal, Base, engine
from models import User, Book, Purchase, Review
from schemas import UserCreate, BookCreate, PurchaseCreate, ReviewCreate
from dotenv import load_dotenv
import os

load_dotenv(".env")

app = FastAPI(title="Book API")

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.include_router(auth.router,prefix="")



