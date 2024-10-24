# [DEBUG] : Receiptモデルの定義
from sqlalchemy import Column, String, Float, Integer, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from uuid import uuid4
from .base import Base

class Receipt(Base):
    __tablename__ = 'receipts'

    # [DEBUG] : 各列の定義
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

    # [DEBUG] : Itemとのリレーションシップ
    items = relationship("Item", back_populates="receipt", cascade="all, delete-orphan")
