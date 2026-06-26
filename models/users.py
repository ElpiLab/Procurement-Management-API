# app/models/user.py
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from database import Base
import enum

# =========================================================
# 1. ENUM (Used ONLY by Python to prevent typos)
# =========================================================
class UserRole(str, enum.Enum):
    REQUESTER = "requester"      # Lane 1
    MANAGER = "manager"          # Lane 2
    PROCUREMENT = "procurement"  # Lane 3
    ADMIN = "admin"              # System Admin

# =========================================================
# 2. SINGLE USER MODEL (Removed the duplicate Requester class)
# =========================================================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    
    # Store the role as a STRING in the DB. 
    # We use the Enum in Python to restrict it.
    role = Column(String, default=UserRole.REQUESTER.value, nullable=False) 
    
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())