from fastapi import FastAPI
from app.database import SessionLocal, Base, engine
from dotenv import load_dotenv
from sqlalchemy import inspect, text
from models import User, Book, Purchase, Review
from app.routers import auth, book, purchase, review
from schemas import UserCreate, BookCreate, PurchaseCreate, ReviewCreate
import os

load_dotenv(".env")

app = FastAPI(title="Book API")



inspector = inspect(engine)
if inspector.has_table("books"):
    columns = [col["name"] for col in inspector.get_columns("books")]
    if "description" not in columns:
        with engine.begin() as conn:
            conn.execute(text("ALTER TABLE books ADD COLUMN description VARCHAR"))

if inspector.has_table("reviews"):
    columns = [col["name"] for col in inspector.get_columns("reviews")]
    if "user_id" in columns and "customer_id" not in columns:
        with engine.begin() as conn:
            conn.execute(text("ALTER TABLE reviews RENAME COLUMN user_id TO customer_id"))

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.include_router(auth.router,prefix="")
app.include_router(book.router,prefix="")
app.include_router(purchase.router,prefix="")
app.include_router(review.router,prefix="")



Base.metadata.create_all(bind=engine)