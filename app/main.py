from fastapi import FastAPI
from app.routers import auth, book
from app.database import SessionLocal, Base, engine
from models import User, Book, Purchase, Review
from schemas import UserCreate, BookCreate, PurchaseCreate, ReviewCreate
from dotenv import load_dotenv
from sqlalchemy import inspect, text
import os

load_dotenv(".env")

app = FastAPI(title="Book API")

Base.metadata.create_all(bind=engine)

inspector = inspect(engine)
if inspector.has_table("books"):
    columns = [col["name"] for col in inspector.get_columns("books")]
    if "description" not in columns:
        with engine.begin() as conn:
            conn.execute(text("ALTER TABLE books ADD COLUMN description VARCHAR"))


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.include_router(auth.router,prefix="")
app.include_router(book.router,prefix="")



