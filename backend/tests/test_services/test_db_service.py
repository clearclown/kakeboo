# tests/test_services/test_db_service.py
import pytest
from datetime import datetime
from src.services.db_service import DBService
from src.core.logger import setup_logger
from src.db.models.receipt import Receipt
from src.db.models.item import Item

logger = setup_logger(__name__)

@pytest.fixture
def db_service(db_session):
    return DBService(db_session)

def test_create_receipt(db_service, sample_receipt_data):
    receipt = db_service.create_receipt(sample_receipt_data)
    
    assert receipt.store_name == sample_receipt_data["store_name"]
    assert receipt.total_amount == sample_receipt_data["total_amount"]
    assert receipt.currency_type == sample_receipt_data["currency_type"]
    assert len(receipt.items) == len(sample_receipt_data["items"])

def test_get_receipt(db_service, sample_receipt_data):
    # First create a receipt
    created_receipt = db_service.create_receipt(sample_receipt_data)
    
    # Then retrieve it
    retrieved_receipt = db_service.get_receipt(created_receipt.receipt_id)
    
    assert retrieved_receipt is not None
    assert retrieved_receipt.store_name == sample_receipt_data["store_name"]
    assert retrieved_receipt.total_amount == sample_receipt_data["total_amount"]

def test_update_receipt(db_service, sample_receipt_data):
    # Create initial receipt
    receipt = db_service.create_receipt(sample_receipt_data)
    
    # Update data
    updated_data = sample_receipt_data.copy()
    updated_data["total_amount"] = 2000.0
    
    # Perform update
    updated_receipt = db_service.update_receipt(receipt.receipt_id, updated_data)
    
    assert updated_receipt.total_amount == 2000.0
    assert updated_receipt.store_name == sample_receipt_data["store_name"]

def test_delete_receipt(db_service, sample_receipt_data):
    # Create receipt
    receipt = db_service.create_receipt(sample_receipt_data)
    
    # Delete receipt
    result = db_service.delete_receipt(receipt.receipt_id)
    
    assert result is True
    assert db_service.get_receipt(receipt.receipt_id) is None
