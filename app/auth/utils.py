import os
from datetime import timedelta, datetime, timezone
from typing import Optional

from argon2 import PasswordHasher
from jose import jwt, JWTError

# env-configurable JWT settings
SECRET_KEY = os.getenv("JWT_SECRET_KEY")  # set this in your .env file or directly in the environment
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

pass_hasher = PasswordHasher()


def hash_password(password: str) -> str:
    return pass_hasher.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return pass_hasher.verify(hashed_password, plain_password)
    except Exception:
        return False


def create_access_token(data: dict, expire_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expire_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
