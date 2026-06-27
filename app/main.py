from pathlib import Path
import sys

from fastapi import FastAPI

# When you run this file directly, Python does not automatically add the repo root to imports.
# This makes `app` and `models` importable without needing to launch through uvicorn.
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# app.core.database is the single source of truth for engine/session/Base.
# Models import Base from there, and then create_all() can register every mapped table.
from app.core.database import Base, engine

# Import the model modules so their table classes are registered before create_all().
from models import approval, purchase_request, supplier, users  # noqa: F401


app = FastAPI(title="Procurement API", version="1.0")


# This creates the tables for every imported SQLAlchemy model.
Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "Procurement API is running!"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)