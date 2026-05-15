from pydantic import BaseModel, Field
from datetime import datetime

class ReviewCreate(BaseModel):
    rating: int = Field(..., ge=1, le=5) # Sirf 1 se 5 tak rating
    comment: str

class ReviewResponse(BaseModel):
    id: int
    user_id: int
    book_id: int
    rating: int
    comment: str
    created_at: datetime

    class Config:
        from_attributes = True