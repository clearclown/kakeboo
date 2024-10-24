# tests/test_api/test_receipt_routes.py
import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.core.logger import setup_logger

logger = setup_logger(__name__)

def test_create_receipt(test_client, sample_receipt_data):
    response = test_client.post("/receipts/", json=sample_receipt_data)
    assert response.status_code == 200
    data = response.json()
    assert data["store_name"] == sample_receipt_data["store_name"]
    assert data["total_amount"] == sample_receipt_data["total_amount"]

def test_get_receipt(test_client, sample_receipt_data):
    # First create a receipt
    create_response = test_client.post("/receipts/", json=sample_receipt_data)
    receipt_id = create_response.json()["receipt_id"]
    
    # Then retrieve it
    response = test_client.get(f"/receipts/{receipt_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["store_name"] == sample_receipt_data["store_name"]

def test_update_receipt(test_client, sample_receipt_data):
    # Create receipt
    create_response = test_client.post("/receipts/", json=sample_receipt_data)
    receipt_id = create_response.json()["receipt_id"]
    
    # Update data
    updated_data = {**sample_receipt_data, "total_amount": 2000.0}
    
    # Perform update
    response = test_client.put(f"/receipts/{receipt_id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["total_amount"] == 2000.0

def test_delete_receipt(test_client, sample_receipt_data):
    # Create receipt
    create_response = test_client.post("/receipts/", json=sample_receipt_data)
    receipt_id = create_response.json()["receipt_id"]
    
    # Delete receipt
    response = test_client.delete(f"/receipts/{receipt_id}")
    assert response.status_code == 200
    
    # Verify deletion
    get_response = test_client.get(f"/receipts/{receipt_id}")
    assert get_response.status_code == 404
