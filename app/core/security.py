# app/core/security.py
# =========================================================
# Purpose: Password hashing & JWT token management.
# This is the "Engine Room" of authentication.
# =========================================================

from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext

# This module groups password hashing and JWT generation so routes/services stay focused on business logic.

# =========================================================
# 1. PASSWORD HASHING (The "Blender")
# =========================================================
# We use bcrypt to make passwords unreadable in the database.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Compare a plain password against a stored hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Convert a plain password into a secure hash for storage."""
    return pwd_context.hash(password)

# =========================================================
# 2. JWT TOKEN GENERATION (The "ID Card Issuer")
# =========================================================
# Replace this with an environment variable once you start configuring auth for real.
SECRET_KEY = "your-super-secret-key-change-this-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """Generate a JWT token containing user data."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt