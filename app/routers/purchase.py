from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from models.book import Book as BookModel
from models.purchase import Purchase as PurchaseModel
from models.user import User as UserModel
from schemas.purchase import PurchaseResponse
from core.security import get_current_user

router = APIRouter(prefix="/purchases", tags=["purchases"])

@router.get("/history", response_model=list[PurchaseResponse])
def get_purchase_history(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    if current_user.role.value != "customer":
        raise HTTPException(
            status_code=403,
            detail={
                "error_code": "BOOKSTORE_ROLE_FORBIDDEN",
                "message": "Only customers can view purchase history"
            }
        )

    purchases = db.query(PurchaseModel).filter(
        PurchaseModel.customer_id == current_user.id
    ).all()
    return purchases

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
        customer_id=current_user.id,
        book_id=book.id,
        price_paid=book.price
    )
    db.add(purchase)
    db.commit()
    db.refresh(purchase)

    return purchase
