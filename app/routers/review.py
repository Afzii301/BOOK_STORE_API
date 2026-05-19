from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from models.review import Review as ReviewModel
from models.purchase import Purchase as PurchaseModel
from models.user import User as UserModel
from schemas.review import ReviewCreate, ReviewResponse
from core.security import get_current_user

router = APIRouter(prefix="/reviews", tags=["reviews"])

# --- 1. POST: Review a book (Customer Only + Purchase Check) ---
@router.post("/{book_id}", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
def review_book(
    book_id: int, 
    review: ReviewCreate, 
    db: Session = Depends(get_db), 
    current_user: UserModel = Depends(get_current_user)
):
    # Rule: Who -> Customer only
    if current_user.role.value != "customer":
        raise HTTPException(status_code=403, detail="Sirf customers hi review de saktay hain.")

    # Rule: Must have purchased it
    purchase = db.query(PurchaseModel).filter(
        PurchaseModel.customer_id == current_user.id,
        PurchaseModel.book_id == book_id
    ).first()
    
    if not purchase:
        raise HTTPException(status_code=400, detail="Review denay ke liye book khareedna lazmi hai.")

    # Duplicate Check: Ek user ek book par ek hi review de
    existing = db.query(ReviewModel).filter(
        ReviewModel.user_id == current_user.id,
        ReviewModel.book_id == book_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Aap pehle hi is book ka review de chukay hain.")

    db_review = ReviewModel(
        user_id=current_user.id,
        book_id=book_id,
        rating=review.rating,
        comment=review.comment
    )
    
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

# --- 2. GET: List reviews for a book (Public) ---
@router.get("/{book_id}", response_model=list[ReviewResponse])
def get_book_reviews(book_id: int, db: Session = Depends(get_db)):
    """Ye endpoint public hai, isme token ki zaroorat nahi"""
    return db.query(ReviewModel).filter(ReviewModel.book_id == book_id).all()