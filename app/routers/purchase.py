from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from models.book import Book as BookModel
from models.purchase import Purchase as PurchaseModel
from models.user import User as UserModel
from schemas.purchase import PurchaseCreate, PurchaseResponse
from core.security import get_current_user
from sqlalchemy.exc import IntegrityError
router = APIRouter(prefix="/purchases", tags=["purchases"])

@router.post("/")
def create_purchase(purchase_in: PurchaseCreate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    # Pehle check karein ke kya user waqayi exist karta hai
    user = db.query(UserModel).filter(UserModel.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Aapka user account delete ho chuka hai ya maujood nahi hai.")

    try:
        new_purchase = PurchaseModel(
            user_id=current_user.id,
            customer_id=current_user.id,
            book_id=purchase_in.book_id,
            price_paid=1000, # ya book.price
            purchased_at=datetime.now(timezone.utc)
        )
        db.add(new_purchase)
        db.commit()
        return new_purchase
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Database error: User ID ya Book ID valid nahi hai.")
    
    
@router.post("/{book_id}", response_model=PurchaseResponse)
def buy_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    if current_user.role.value != "customer":
        raise HTTPException(
            status_code=403,
            detail={
                "error_code": "BOOKSTORE_ROLE_FORBIDDEN",
                "message": "Only customers can buy books"
            }
        )

    book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if not book:
        raise HTTPException(
            status_code=404,
            detail={
                "error_code": "BOOKSTORE_BOOK_NOT_FOUND",
                "message": "Book not found"
            }
        )

    # Constraint C: snapshot the current price at purchase time
    purchase = PurchaseModel(
        user_id=current_user.id,
        customer_id=current_user.id,
        book_id=book.id,
        price_paid=book.price,
        purchased_at=datetime.now(timezone.utc)
    )
    db.add(purchase)
    db.commit()
    db.refresh(purchase)

    return purchase
