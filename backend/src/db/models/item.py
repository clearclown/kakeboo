# backend/src/db/models/item.py

from sqlalchemy import Column, String, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship
from ..session import Base

class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    receipt_id = Column(Integer, ForeignKey('receipts.id'))
    product_name = Column(String(255), default="-")
    price = Column(Float, default=0.0)
    quantity = Column(Integer, default=1)
    discount = Column(String(255), default="0.0")
    notes = Column(String, default="-")

    # Relationships
    receipt = relationship("Receipt", back_populates="items")

    def to_dict(self):
        return {
            "id": self.id,
            "receipt_id": self.receipt_id,
            "product_name": self.product_name,
            "price": self.price,
            "quantity": self.quantity,
            "discount": self.discount,
            "notes": self.notes
        }
