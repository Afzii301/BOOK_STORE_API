from pydantic import BaseModel

class BookCreate(BaseModel):
    title: str
    author: str
    price: float
    description: str | None = None

class BookResponse(BaseModel):
    id: int
    title: str
    price: float
    description: str | None = None
    author_id:int

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
    }
