from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime, timezone

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False)
    rating = Column(Integer, nullable=False)  # 1 to 5
    comment = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    customer_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False) 
    
    
    # Relationships (Using string paths to avoid mapper errors)
    customer = relationship("models.user.User", back_populates="reviews",foreign_keys=[customer_id])
    book = relationship("Book",back_populates="reviews",foreign_keys=[book_id])