from pydantic import BaseModel
from typing import Literal
class UserCreate(BaseModel):
    name: str
    email: str
    password: str
class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role:Literal["customer", "author"]
    class Config:
        from_attributes = True