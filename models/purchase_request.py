from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.sql import func

# Import Base from the shared database module so the ORM can register this table.
from app.core.database import Base


class PurchaseRequest(Base):
    __tablename__ = "purchase_requests"

    # This is the main workflow record: request details, routing, and lifecycle state.
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    quantity = Column(Integer, default=1, nullable=False)
    unit_price = Column(Float, nullable=True)
    total_price = Column(Float, nullable=True)
    status = Column(String, default="draft", nullable=False)
    requester_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=True)
    delivery_date = Column(Date, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    closed_at = Column(DateTime(timezone=True), nullable=True)
