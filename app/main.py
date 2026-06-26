# app/main.py
from pathlib import Path
import sys

from fastapi import FastAPI

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from database import Base, engine
from models import approval, purchase_request, supplier, users  # noqa: F401

# 1. Create the FastAPI web server
app = FastAPI(title="Procurement API", version="1.0")

# 2. This line sends the "CREATE TABLE" command to your PostgreSQL database
#    (It will create the 'users' table automatically!)
Base.metadata.create_all(bind=engine)

# 3. A simple test route to prove your API is alive
@app.get("/")
def root():
    return {"message": "Procurement API is running on PostgreSQL!"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)