# =========================================================
# FILE: app/core/database.py
# =========================================================
# Purpose: Database connection setup.
# This file creates the "bridge" between your Python code
# and the actual database (SQLite file).
# =========================================================

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# =========================================================
# 1. DATABASE URL (Where the database lives)
# "sqlite:///./procurement.db" -> Creates a file in your project root.
# =========================================================
SQLALCHEMY_DATABASE_URL = "sqlite:///./procurement.db"

# =========================================================
# 2. ENGINE (The "motor" that connects to the database)
# connect_args={"check_same_thread": False} is required for SQLite.
# It allows multiple threads to access the database (needed for FastAPI).
# =========================================================
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# =========================================================
# 3. SESSION LOCAL (The "transaction manager")
# This creates a session object to talk to the database.
# Each API request will create its own session.
# =========================================================
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# =========================================================
# 4. BASE (The foundation for ALL models)
# All your SQLAlchemy classes (User, PurchaseRequest) will inherit from this.
# This ensures they are all linked to the same database.
# =========================================================
Base = declarative_base()