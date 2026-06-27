from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.sql import func

# Import Base from the canonical SQLAlchemy module so every model shares the same metadata.
from app.core.database import Base


class Approval(Base):
    __tablename__ = "approvals"

    # One approval row links a request to the user who approved or rejected it.
    id = Column(Integer, primary_key=True, index=True)
    purchase_request_id = Column(Integer, ForeignKey("purchase_requests.id"), nullable=False)
    approver_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    outcome = Column(String, nullable=False)
    comments = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
