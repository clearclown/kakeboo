# test_utils/test_validators.py
import pytest
from src.utils.validators import ReceiptValidator, ItemValidator
from src.core.logger import setup_logger

logger = setup_logger(__name__)

@pytest.fixture
def receipt_validator():
    return ReceiptValidator()

@pytest.fixture
def item_validator():
    return ItemValidator()

def test_validate_receipt_success(receipt_validator, sample_receipt_data):
    result = receipt_validator.validate(sample_receipt_data)
    assert result["valid"] is True
    assert result["errors"] == []

def test_validate_receipt_missing_required_fields(receipt_validator):
    invalid_data = {
        "store_name": "Sample Store"
        # Missing other required fields
    }
    result = receipt_validator.validate(invalid_data)
    assert result["valid"] is False
    assert len(result["errors"]) > 0

def test_validate_receipt_invalid_amount(receipt_validator):
    invalid_data = {
        **sample_receipt_data,
        "total_amount": -1000.0  # Negative amount
    }
    result = receipt_validator.validate(invalid_data)
    assert result["valid"] is False
    assert any("amount" in error for error in result["errors"])

def test_validate_item_success(item_validator):
    item_data = {
        "product_name": "Test Product",
        "price": 100.0,
        "quantity": 1
    }
    result = item_validator.validate(item_data)
    assert result["valid"] is True
    assert result["errors"] == []

def test_validate_item_invalid_price(item_validator):
    invalid_data = {
        "product_name": "Test Product",
        "price": -100.0,  # Negative price
        "quantity": 1
    }
    result = item_validator.validate(invalid_data)
    assert result["valid"] is False
    assert any("price" in error for error in result["errors"])
