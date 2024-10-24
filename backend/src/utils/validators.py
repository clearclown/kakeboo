# backend/src/utils/validators.py

from typing import Dict, Any
from datetime import datetime
from ..core.logger import setup_logger

logger = setup_logger(__name__)

class BaseValidator:
    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Base validation method"""
        raise NotImplementedError()

    def _validate_required_fields(self, data: Dict[str, Any], required_fields: list) -> list:
        """Validate required fields"""
        errors = []
        for field in required_fields:
            if field not in data or data[field] is None:
                errors.append(f"Missing required field: {field}")
        return errors

class ReceiptValidator(BaseValidator):
    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate receipt data"""
        errors = []

        # Required fields
        required_fields = ["store_name", "total_amount"]
        errors.extend(self._validate_required_fields(data, required_fields))

        # Validate total_amount
        if "total_amount" in data:
            if not isinstance(data["total_amount"], (int, float)):
                errors.append("total_amount must be a number")
            elif data["total_amount"] < 0:
                errors.append("total_amount cannot be negative")

        # Validate time
        if "time" in data:
            try:
                datetime.fromisoformat(data["time"])
            except ValueError:
                errors.append("Invalid time format. Use ISO format")

        return {
            "valid": len(errors) == 0,
            "errors": errors
        }

class ItemValidator(BaseValidator):
    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate item data"""
        errors = []

        # Required fields
        required_fields = ["product_name", "price"]
        errors.extend(self._validate_required_fields(data, required_fields))

        # Validate price
        if "price" in data:
            if not isinstance(data["price"], (int, float)):
                errors.append("price must be a number")
            elif data["price"] < 0:
                errors.append("price cannot be negative")

        # Validate quantity
        if "quantity" in data:
            if not isinstance(data["quantity"], int):
                errors.append("quantity must be an integer")
            elif data["quantity"] < 1:
                errors.append("quantity must be positive")

        return {
            "valid": len(errors) == 0,
            "errors": errors
        }
