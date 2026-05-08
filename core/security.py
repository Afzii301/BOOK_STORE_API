from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from models.user import User
import os
from dotenv import load_dotenv

# -------------------------
# LOAD ENV CONFIG
# -------------------------
load_dotenv(".env")

SECRET_KEY: str = os.getenv("SECRET_KEY", "default-secret-key")
ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__max_rounds=12
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# -------------------------

def _normalize_password(password) -> bytes:
    """Convert to bytes and truncate to 72 characters."""
    if isinstance(password, str):
        password = password.encode("utf-8")
    elif not isinstance(password, (bytes, bytearray)):
        password = str(password).encode("utf-8")
    return bytes(password)[:72]

def hash_password(password: str) -> str:
    return pwd_context.hash(_normalize_password(password))

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(_normalize_password(plain_password), hashed_password)

# -------------------------
# JWT TOKEN
# -------------------------

def create_access_token(data: dict, expires_delta: int = ACCESS_TOKEN_EXPIRE_MINUTES) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail={
                "error_code": "BOOKSTORE_AUTH_REQUIRED",
                "message": "Invalid authentication token"
            })
    except JWTError:
        raise HTTPException(status_code=401, detail={
            "error_code": "BOOKSTORE_AUTH_REQUIRED",
            "message": "Invalid authentication token"
        })

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=404, detail={
            "error_code": "BOOKSTORE_USER_NOT_FOUND",
            "message": "User not found"
        })
    return user
