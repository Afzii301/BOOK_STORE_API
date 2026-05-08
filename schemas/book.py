from pydantic import BaseModel

class BookCreate(BaseModel):
    title: str
    author: str
    price: float

class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    price: float

    class Config:
        from_attributes = True
