# backend/src/schemas/receipt.py

from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime

class ItemBase(BaseModel):
    product_name: str
    price: float = Field(ge=0)
    quantity: int = Field(ge=1, default=1)
    discount: str = "0.0"
    notes: str = "-"

class ItemCreate(ItemBase):
    pass

class ItemUpdate(ItemBase):
    pass

class ItemInDB(ItemBase):
    id: int
    receipt_id: int

    class Config:
        orm_mode = True

class ReceiptBase(BaseModel):
    store_name: str
    total_amount: float = Field(ge=0)
    currency_type: str = "JPY"
    payment_method: str = "-"
    payment_details: str = "-"
    store_type: str = "-"
    location: str = "-"
    number_of_people: int = Field(ge=0, default=0)
    notes: str = "-"
    receipt_status: str = "pending"
    receipt_image_path: str = "-"

class ReceiptCreate(ReceiptBase):
    time: Optional[datetime]
    items: List[ItemCreate] = []

class ReceiptUpdate(ReceiptBase):
    pass

class ReceiptInDB(ReceiptBase):
    id: int
    receipt_id: str
    created_at: datetime
    time: Optional[datetime]
    items: List[ItemInDB]

    class Config:
        orm_mode = True
