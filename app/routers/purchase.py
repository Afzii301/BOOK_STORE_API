from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from core.security import get_current_user
from models.purchase import Purchase as PurchaseModel
from models.book import Book as BookModel
from models.user import User as UserModel, Role
from schemas.purchase import PurchaseResponse

router = APIRouter(prefix="/purchases", tags=["purchases"])

# --- GET: Purchase History (Customer Only) ---
@router.get("/history", response_model=list[PurchaseResponse])
def get_history(
    db: Session = Depends(get_db), 
    current_user: UserModel = Depends(get_current_user)
):
    if current_user.role != Role.customer:
        raise HTTPException(status_code=403, detail="Sirf customers history dekh saktay hain.")

    history = db.query(PurchaseModel).filter(PurchaseModel.user_id == current_user.id).all()
    return history

# --- POST: Buy a Book ---
@router.post("/{book_id}", response_model=PurchaseResponse)
def buy_book(
    book_id: int, 
    db: Session = Depends(get_db), 
    current_user: UserModel = Depends(get_current_user)
):
    # 1. Role Check
    if current_user.role != Role.customer:
        raise HTTPException(status_code=403, detail="Sirf customers hi khareed saktay hain.")

    # 2. Book Check
    book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book nahi mili.")

    # 3. Create Purchase
    new_purchase = PurchaseModel(
        user_id=current_user.id,
        customer_id=current_user.id,
        book_id=book.id,
        price_paid=book.price  # Snapshot price
    )

    try:
        db.add(new_purchase)
        db.commit()
        db.refresh(new_purchase)
        return new_purchase
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Purchase fail: {str(e)}")