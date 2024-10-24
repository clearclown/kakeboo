# [DEBUG] : Itemモデルの定義
from sqlalchemy import Column, String, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship
from src.db.models.base import Base

class Item(Base):
    __tablename__ = 'items'

    # [DEBUG] : 各列の定義
    id = Column(Integer, primary_key=True)
    receipt_id = Column(Integer, ForeignKey('receipts.id'))
    product_name = Column(String(255), default="-")
    price = Column(Float, default=0.0)
    quantity = Column(Integer, default=1)
    discount = Column(String(255), default="0.0")
    notes = Column(String, default="-")

    # [DEBUG] : Receiptとのリレーションシップ
    receipt = relationship("Receipt", back_populates="items")
