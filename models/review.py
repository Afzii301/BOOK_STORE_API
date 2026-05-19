from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, inspect
from sqlalchemy.orm import relationship, synonym
from app.database import Base, engine
from datetime import datetime, timezone

inspector = inspect(engine)
review_col = "customer_id"
if inspector.has_table("reviews"):
    cols = [col["name"] for col in inspector.get_columns("reviews")]
    if "customer_id" not in cols and "user_id" in cols:
        review_col = "user_id"

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False)
    rating = Column(Integer, nullable=False)  # 1 to 5
    comment = Column(String, nullable=True)
   
    _customer_user_id = Column(review_col, Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    customer_id = synonym("_customer_user_id")
    user_id = synonym("_customer_user_id")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Relationships (Using string paths to avoid mapper errors)
    customer = relationship("models.user.User", back_populates="reviews", foreign_keys=[_customer_user_id])
    book = relationship("Book", back_populates="reviews", foreign_keys=[book_id])
    
    