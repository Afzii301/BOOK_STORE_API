from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
import os
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__max_rounds=12
)



# -------------------------
# PASSWORD HASHING
# -------------------------

def _normalize_password(password) -> bytes:
    if isinstance(password, str):
        password = password.encode("utf-8")
    elif not isinstance(password, (bytes, bytearray)):
        password = str(password).encode("utf-8")
    return bytes(password)[:72]


def hash_password(password):
    return pwd_context.hash(_normalize_password(password))


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(_normalize_password(plain_password), hashed_password)


# -------------------------
# JWT TOKEN (optional but needed later)
# -------------------------
def create_access_token(data: dict, expires_delta: int = 30):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_delta)

    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)