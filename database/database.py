import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./procurement.db")

engine_kwargs = {}
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
	engine_kwargs["connect_args"] = {"check_same_thread": False}

engine = create_engine(SQLALCHEMY_DATABASE_URL, **engine_kwargs)

# =========================================================
# STEP 3: The TELEPHONE OPERATOR (Session)
# =========================================================
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# =========================================================
# STEP 4: The BLUEPRINT (Base for all tables)
# =========================================================
Base = declarative_base()