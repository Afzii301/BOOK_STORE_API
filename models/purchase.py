from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
from models.user import User as UserModel
from models.book import Book as BookModel



class Purchase(Base):
    __tablename__ = "purchases"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    customer_id = Column(Integer, ForeignKey("users.id"))
    book_id = Column(Integer, ForeignKey("books.id"))
    price_paid = Column(Float, nullable=False)
    purchased_at = Column(DateTime, default=datetime.utcnow)

    customer = relationship("User", back_populates="purchases", foreign_keys=[customer_id])
    user = relationship("User", foreign_keys=[user_id])
    book = relationship("Book", back_populates="purchases")
    