import os
import sys
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

# folder structure ye btata ha k main folder ke andar app folder hai jisme database.py file hai 
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from app.database import SessionLocal, Base, engine
from models import User, Book, Purchase, Review
from schemas import UserCreate, BookCreate, PurchaseCreate, ReviewCreate
from dotenv import load_dotenv

load_dotenv(os.path.join(ROOT_DIR, ".env"))

app = FastAPI(
    title="Book API",
    description="A simple API for managing books and users",
)

Base.metadata.create_all(bind=engine)
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()
        
        
        
        
        
        
