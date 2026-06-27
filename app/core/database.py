import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Database URL comes from the environment when available, and falls back to SQLite for learning.
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./procurement.db")

# SQLite needs check_same_thread=False. Other databases do not.
engine_kwargs = {}
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}

engine = create_engine(SQLALCHEMY_DATABASE_URL, **engine_kwargs)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is the shared parent class for all SQLAlchemy models.
Base = declarative_base()


def get_db():
    # FastAPI route handlers can depend on this generator to get a DB session.
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()