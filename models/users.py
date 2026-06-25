#Here is the table for all users

requester (Lane 1: Creates the request)

manager (Lane 2: Approves normal requests)

procurement (Lane 3: Approves high-value requests)

admin (Lane 4-ish: Manages suppliers, system config)

# app/models/user.py
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from app.core.database import Base
import enum

# Step 1: Define the Enum for the role (like we just discussed!)
class UserRole(str, enum.Enum):
    REQUESTER = "requester"
    MANAGER = "manager"
    PROCUREMENT = "procurement"
    ADMIN = "admin"

# Step 2: Define the SQLAlchemy Class
class User(Base):
    __tablename__ = "users"
    
    # id: integer, primary key, auto-increment
    id = Column(Integer, primary_key=True, index=True)
    
    # name: string, cannot be null
    # HINT: Column(String, nullable=False)
    
    # email: string, unique, cannot be null
    # HINT: Column(String, unique=True, nullable=False, index=True)
    
    # role: use the Enum we just defined. Default to "requester".
    # HINT: Column(Enum(UserRole), default=UserRole.REQUESTER)
    
    # hashed_password: We need this for login! (We forgot it earlier).
    # HINT: Column(String, nullable=False)
    
    # created_at: Timestamp, automatically set when record is inserted.
    # HINT: Column(DateTime(timezone=True), server_default=func.now())
    
    # updated_at: Timestamp, automatically updated when record changes.
    # HINT: Column(DateTime(timezone=True), onupdate=func.now())
    
    pass  # <-- DELETE this line and fill in your columns!