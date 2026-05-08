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

    class Config:
        from_attributes = True
