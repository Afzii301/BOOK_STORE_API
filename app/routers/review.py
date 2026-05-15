from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from models.review import Review as ReviewModel
from models.user import User as UserModel
from models.purchase import Purchase as PurchaseModel
from schemas.review import ReviewCreate, ReviewResponse
from core.security import get_current_user

router = APIRouter(prefix="/reviews", tags=["reviews"])

# 1. POST /reviews/{book_id} (Customer Only)
@router.post("/{book_id}", response_model=ReviewResponse)
def review_book(
    book_id: int, 
    review: ReviewCreate, 
    db: Session = Depends(get_db), 
    current_user: UserModel = Depends(get_current_user)
):
    # Role Check: Table ke mutabiq sirf Customer
    if current_user.role.value != "customer":
        raise HTTPException(status_code=403, detail="Only customers can review books")

    # Purchase Check: Table ke mutabiq purchase hona lazmi hai
    purchase = db.query(PurchaseModel).filter(
        PurchaseModel.customer_id == current_user.id,
        PurchaseModel.book_id == book_id
    ).first()
    
    if not purchase:
        raise HTTPException(status_code=400, detail="You must purchase the book before reviewing it")

    db_review = ReviewModel(
        customer_id=current_user.id,
        book_id=book_id,
        rating=review.rating,
        comment=review.comment
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

# 2. GET /reviews/{book_id} (Public - No Auth Required)
@router.get("/{book_id}", response_model=list[ReviewResponse])
def list_book_reviews(book_id: int, db: Session = Depends(get_db)):
    """Table ke mutabiq ye Public endpoint hai"""
    return db.query(ReviewModel).filter(ReviewModel.book_id == book_id).all()