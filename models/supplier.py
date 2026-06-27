from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.sql import func

# Supplier is another table that purchase requests point to through supplier_id.
from app.core.database import Base


class Supplier(Base):
    __tablename__ = "suppliers"

    # Supplier records hold vendor identity and contact details.
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    contact_person = Column(String, nullable=True)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
