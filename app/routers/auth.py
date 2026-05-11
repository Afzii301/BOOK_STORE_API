from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from models.user import User, Role
from schemas.user import UserCreate, UserLogin
from core.security import create_access_token, hash_password, verify_password

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)
from sqlalchemy.exc import IntegrityError

@router.post("/register", status_code=201)
def register(user: UserCreate, db: Session = Depends(get_db)):

    try:
        
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
#   login endpoint
@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(
        User.username == user.username
    ).first()

    if not db_user:
        raise HTTPException(
            status_code=404,
            detail={
                "error_code": "BOOKSTORE_USER_NOT_FOUND",
                "message": "User not found"
            }
        )
    if not verify_password(user.password, db_user.password_hash):
        raise HTTPException(
            status_code=401,
            detail={
                "error_code": "BOOKSTORE_INVALID_CREDENTIALS",
                "message": "Wrong password"
            }
        )

    # token creat
    token = create_access_token({
        "user_id": db_user.id,
        "role": db_user.role.value
    })
    return {
        "access_token": token,
        "token_type": "bearer"
    }
    
    
    
@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        db.delete(user)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": "User deleted"}