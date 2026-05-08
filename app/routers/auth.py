from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from models.user import User, Role
from schemas.user import UserCreate
from core.security import hash_password

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)
from sqlalchemy.exc import IntegrityError

@router.post("/register", status_code=201)
def register(user: UserCreate, db: Session = Depends(get_db)):

    try:
        # Convert role string to enum
        try:
            role = Role(user.role.lower())
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail={
                    "error_code": "BOOKSTORE_INVALID_ROLE",
                    "message": "Role must be 'author' or 'customer'"
                }
            )
        
        new_user = User(
            username=user.username,
            email=user.email,
            password_hash=hash_password(user.password),
            role=role
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {"message": "User created successfully"}

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail={
                "error_code": "BOOKSTORE_USER_ALREADY_EXISTS",
                "message": "Username or email already exists"
            }
        )