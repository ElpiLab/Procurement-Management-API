# Re-export the canonical SQLAlchemy objects for backwards compatibility.
# Models can import from app.core.database directly, but this keeps `from database import Base` working too.
from app.core.database import Base, SessionLocal, engine, get_db

