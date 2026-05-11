from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from models.review import Review as ReviewModel
from models.user import User as UserModel
from models.book import Book as BookModel
from models.purchase import Purchase as PurchaseModel
from schemas.review import ReviewCreate, ReviewResponse
from core.security import get_current_user

router = APIRouter(
    prefix="/reviews",
    tags=["reviews"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/{book_id}", response_model=ReviewResponse)
def create_review(book_id: int, review: ReviewCreate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    if current_user.role.value != "customer":
        raise HTTPException(status_code=403, detail={
            "error_code": "BOOKSTORE_ROLE_FORBIDDEN",
            "message": "Only customers can leave reviews"
        })

    # Check if book exists
    book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail={
            "error_code": "BOOKSTORE_BOOK_NOT_FOUND",
            "message": "Book not found"
        })

    # Check if customer has purchased the book
    purchase = db.query(PurchaseModel).filter(
        PurchaseModel.customer_id == current_user.id,
        PurchaseModel.book_id == book_id
    ).first()
    if not purchase:
        raise HTTPException(status_code=400, detail={
            "error_code": "BOOKSTORE_PURCHASE_REQUIRED",
            "message": "You must purchase the book before reviewing it"
        })

    # Validate rating
    if not (1 <= review.rating <= 5):
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")

    # Check if already reviewed
    existing_review = db.query(ReviewModel).filter(
        ReviewModel.customer_id == current_user.id,
        ReviewModel.book_id == book_id
    ).first()
    if existing_review:
        raise HTTPException(status_code=400, detail="You have already reviewed this book")

    db_review = ReviewModel(
        customer_id=current_user.id,
        book_id=book_id,
        rating=review.rating,
        comment=review.comment,
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

@router.get("/{book_id}", response_model=list[ReviewResponse])
def get_reviews(book_id: int, db: Session = Depends(get_db)):
    # Check if book exists
    book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail={
            "error_code": "BOOKSTORE_BOOK_NOT_FOUND",
            "message": "Book not found"
        })

    return db.query(ReviewModel).filter(ReviewModel.book_id == book_id).all()