from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime, timezone

class Purchase(Base):
    __tablename__ = "purchases"

    id = Column(Integer, primary_key=True, index=True)
    # ondelete="CASCADE" ka matlab: User delete ho toh purchase bhi delete ho jaye
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    customer_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False)
    price_paid = Column(Float, nullable=False)
    purchased_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships using full paths to avoid Mapper errors
    customer = relationship("models.user.User", back_populates="purchases", foreign_keys=[customer_id])
    book = relationship("models.book.Book", back_populates="purchases")