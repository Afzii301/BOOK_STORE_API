from pydantic import BaseModel

class BookCreate(BaseModel):
    title: str
    author: str
    price: float
    description: str | None = None

class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    price: float
    description: str | None = None

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
    }
