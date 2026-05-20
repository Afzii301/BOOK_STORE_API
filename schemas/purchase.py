from datetime import datetime

from pydantic import BaseModel
class bookDetailsInpurchase(BaseModel):
    id: int
    title: str
    price: float
    cover_url: str|None
    
    model_config = {
        "from_attributes": True,
    }

class PurchaseCreate(BaseModel):
    user_id: int
    book_id: int

class PurchaseResponse(BaseModel):
    id: int
    user_id: int
    customer_id: int
    book_id: int
    price_paid: float
    purchased_at: datetime  

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
    }
