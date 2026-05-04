from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.database import Base, engine
import models
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
@app.get("/")
def read_root():
    return {"Hello": "World"}




Base.metadata.create_all(bind=engine)
print("✅ Tables created successfully")