from pydantic import BaseModel

class PurchaseCreate(BaseModel):
    user_id: int
    book_id: int

class PurchaseResponse(BaseModel):
    id: int
    user_id: int
    book_id: int
    purchase_date: str

    class Config:
        from_attributes = True
