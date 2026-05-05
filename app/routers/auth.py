from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import DATABASE_URL, get_db
from dotenv import load_dotenv
from models.user import User 
from schemas.user import UserCreate

router = APIRouter(prefix="/auth", tags=["auth"])

# REGISTER
@router.get("/auth")
def test():
    return {"message": "Hello, World!"}