from pydantic import BaseModel

class ReviewCreate(BaseModel):
    user_id: int
    book_id: int
    rating: float
    comment: str | None = None

class ReviewResponse(BaseModel):
    id: int
    user_id: int
    book_id: int
    rating: float
    comment: str | None = None

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
    }
