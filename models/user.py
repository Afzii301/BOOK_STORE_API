from sqlalchemy import Column, Integer, String
from app.database import Base
import enum

class role(str, enum.Enum):
    admin = "author"
    user = "customer"



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String(100),unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String, nullable=False)