# tests/test_integration/test_data_persistence.py

import pytest
from datetime import datetime
from src.services.db_service import DBService
from src.core.logger import setup_logger

logger = setup_logger(__name__)

def test_receipt_with_items_persistence(db_service, sample_receipt_data):
    # 1. Create receipt with items
    receipt = db_service.create_receipt(sample_receipt_data)
    
    assert receipt is not None
    assert len(receipt.items) == len(sample_receipt_data["items"])
    
    # 2. Verify all items are persisted
    for i, item_data in enumerate(sample_receipt_data["items"]):
        assert receipt.items[i].product_name == item_data["product_name"]
        assert receipt.items[i].price == item_data["price"]
    
    # 3. Update an item
    updated_item_data = {
        "product_name": "Updated Item",
        "price": 750.0,
        "quantity": 1
    }
    db_service.update_item(receipt.items[0].id, updated_item_data)
    
    # 4. Verify update
    updated_receipt = db_service.get_receipt(receipt.receipt_id)
    assert updated_receipt.items[0].product_name == "Updated Item"
    assert updated_receipt.items[0].price == 750.0

def test_transaction_rollback(db_service, sample_receipt_data):
    try:
        with db_service.session.begin():
            # 1. Create receipt
            receipt = db_service.create_receipt(sample_receipt_data)
            
            # 2. Attempt invalid operation
            invalid_item = {
                "product_name": "Invalid Item",
                "price": -100.0,  # Invalid negative price
                "quantity": 1
            }
            db_service.create_item(receipt.receipt_id, invalid_item)
    except Exception:
        pass
    
    # Verify nothing was persisted due to rollback
    assert db_service.get_receipt(receipt.receipt_id) is None
