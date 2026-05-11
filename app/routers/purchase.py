
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from core.security import get_current_user
import models
import schemas

router = APIRouter(prefix="/purchases", tags=["Purchases"])

@router.post("/{book_id}", response_model=schemas.PurchaseResponse)
def buy_book(book_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.role != "customer":
        raise HTTPException(
            status_code=403,
            detail={"error_code": "BOOKSTORE_ROLE_FORBIDDEN", "message": "Only customers can buy books"}
        )

    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(
            status_code=404,
            detail={"error_code": "BOOKSTORE_BOOK_NOT_FOUND", "message": "Book not found"}
        )

    # Constraint C: snapshot the price
    purchase = models.Purchase(
        customer_id=current_user.id,
        book_id=book.id,
        price_paid=book.price
    )
    db.add(purchase)
    db.commit()
    db.refresh(purchase)

    return purchase




@router.get("/history", response_model=list[schemas.PurchaseResponse])
def get_purchase_history(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.role != "customer":
        raise HTTPException(
            status_code=403,
            detail={"error_code": "BOOKSTORE_ROLE_FORBIDDEN", "message": "Only customers can view purchase history"}
        )

    purchases = db.query(models.Purchase).filter(models.Purchase.customer_id == current_user.id).all()
    return purchases
