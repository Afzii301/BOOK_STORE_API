from pydantic import BaseModel,EmailStr
from typing import Literal


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: Literal["customer", "author"]

class UserLogin(BaseModel):
    username: str
    password: str
    
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role:Literal["customer", "author"]
    
    class Config:
        from_attributes = True