# backend/src/db/models/receipt.py

from sqlalchemy import Column, String, Float, Integer, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from uuid import uuid4
from src.db.models.base import Base

class Receipt(Base):
    __tablename__ = 'receipts'

    id = Column(Integer, primary_key=True)
    receipt_id = Column(String(255), unique=True, default=lambda: str(uuid4()))
    time = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())
    currency_type = Column(String(3), default="JPY")
    total_amount = Column(Float, default=0.0)
    payment_method = Column(String(255), default="-")
    payment_details = Column(String(255), default="-")
    store_name = Column(String(255), default="-")
    store_type = Column(String(255), default="-")
    store_other_info = Column(JSON)
    location = Column(String(255), default="-")
    number_of_people = Column(Integer, default=0)
    notes = Column(String, default="-")
    receipt_status = Column(String(255), default="pending")
    receipt_image_path = Column(String(255), default="-")

    # Relationships
    items = relationship("Item", back_populates="receipt", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "receipt_id": self.receipt_id,
            "time": self.time.isoformat() if self.time else None,
            "created_at": self.created_at.isoformat(),
            "currency_type": self.currency_type,
            "total_amount": self.total_amount,
            "payment_method": self.payment_method,
            "payment_details": self.payment_details,
            "store_name": self.store_name,
            "store_type": self.store_type,
            "store_other_info": self.store_other_info,
            "location": self.location,
            "number_of_people": self.number_of_people,
            "notes": self.notes,
            "receipt_status": self.receipt_status,
            "receipt_image_path": self.receipt_image_path,
            "items": [item.to_dict() for item in self.items]
        }
