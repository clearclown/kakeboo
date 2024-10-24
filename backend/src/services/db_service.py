# backend/src/services/db_service.py

from typing import Dict, Any, Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from ..db.models.receipt import Receipt
from ..db.models.item import Item
from ..core.logger import setup_logger

logger = setup_logger(__name__)

class DBService:
    def __init__(self, session: Session):
        self.session = session

    def create_receipt(self, receipt_data: Dict[str, Any]) -> Optional[Receipt]:
        """Create new receipt with items"""
        try:
            # Create receipt
            receipt = Receipt(
                store_name=receipt_data["store_name"],
                total_amount=receipt_data["total_amount"],
                currency_type=receipt_data.get("currency_type", "JPY"),
                payment_method=receipt_data.get("payment_method", "-"),
                store_type=receipt_data.get("store_type", "-"),
                time=receipt_data.get("time"),
                location=receipt_data.get("location", "-"),
                notes=receipt_data.get("notes", "-")
            )
            self.session.add(receipt)

            # Create items
            for item_data in receipt_data.get("items", []):
                item = Item(
                    receipt=receipt,
                    product_name=item_data["product_name"],
                    price=item_data["price"],
                    quantity=item_data.get("quantity", 1),
                    discount=item_data.get("discount", "0.0"),
                    notes=item_data.get("notes", "-")
                )
                self.session.add(item)

            self.session.commit()
            return receipt

        except Exception as e:
            logger.error(f"Error creating receipt: {str(e)}", exc_info=True)
            self.session.rollback()
            return None

    def get_receipt(self, receipt_id: str) -> Optional[Receipt]:
        """Get receipt by ID"""
        try:
            return self.session.query(Receipt).filter(
                Receipt.receipt_id == receipt_id
            ).first()
        except Exception as e:
            logger.error(f"Error getting receipt: {str(e)}", exc_info=True)
            return None

    def update_receipt(self, receipt_id: str, receipt_data: Dict[str, Any]) -> Optional[Receipt]:
        """Update receipt"""
        try:
            receipt = self.get_receipt(receipt_id)
            if not receipt:
                return None

            # Update receipt fields
            for key, value in receipt_data.items():
                if hasattr(receipt, key):
                    setattr(receipt, key, value)

            self.session.commit()
            return receipt

        except Exception as e:
            logger.error(f"Error updating receipt: {str(e)}", exc_info=True)
            self.session.rollback()
            return None

    def delete_receipt(self, receipt_id: str) -> bool:
        """Delete receipt"""
        try:
            receipt = self.get_receipt(receipt_id)
            if receipt:
                self.session.delete(receipt)
                self.session.commit()
                return True
            return False

        except Exception as e:
            logger.error(f"Error deleting receipt: {str(e)}", exc_info=True)
            self.session.rollback()
            return False
