import shutil
import os
from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile,File
from sqlalchemy.orm import Session
from app.database import get_db
from app.database import SessionLocal
from sqlalchemy.orm import Session
from core.security import get_current_user
from models.book import Book as BookModel
from models.user import Role
from schemas.book import BookCreate, BookResponse
router = APIRouter(
    prefix="/books",
    tags=["books"]
)

def get_db():    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@router.post("/", response_model=BookResponse)
async def create_book(
    title: str = Form(...),
    price: float = Form(...),
    description: str = Form(None),
    cover_image: UploadFile = File(None),  # Optional cover
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # 1. Authorization Check
    if current_user.role != Role.author:
        raise HTTPException(status_code=403, detail="Sirf Authors hi books create kar saktay hain.")

    # 2. File Save Karne ka Logic
    saved_path = None
    if cover_image:
        upload_folder = "static/covers"
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        
        # File ka unique naam (taake conflict na ho)
        file_extension = cover_image.filename.split(".")[-1]
        file_name = f"book_{title.replace(' ', '_')}.{file_extension}"
        saved_path = os.path.join(upload_folder, file_name)

        with open(saved_path, "wb") as buffer:
            shutil.copyfileobj(cover_image.file, buffer)

    # 3. Database mein Entry
    db_book = BookModel(
        title=title,
        price=price,
        description=description,
        cover_url=saved_path,  # Database mein path save hoga
        author_id=current_user.id
    )
    
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
@router.get("/", response_model=list[BookResponse])
def get_books(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return db.query(BookModel).all()


@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.put("/{book_id}", response_model=BookResponse)
def update_book(book_id: int, updated_book: BookCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if current_user.role != Role.author:
            raise HTTPException(status_code=403, detail="Sirf Authors hi books update kr  sakta hain.")


    book.title = updated_book.title
    book.author = updated_book.author
    book.price = updated_book.price
    book.description = updated_book.description

    db.commit()
    db.refresh(book)
    return book


@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if current_user.role != Role.author:
            raise HTTPException(status_code=403, detail="Sirf Authors hi books Delete kr  sakta hain.")

    db.delete(book)
    db.commit()
    return {"message": "Book deleted successfully"}