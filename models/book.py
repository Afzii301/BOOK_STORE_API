from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    description = Column(String, nullable=True)
    cover_url    = Column(String, nullable=True)
    author_id = Column(Integer,ForeignKey("users.id"), nullable=False)

    purchases = relationship("Purchase", back_populates="book")
    reviews = relationship("Review", back_populates="book")


