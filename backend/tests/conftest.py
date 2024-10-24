# conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pathlib import Path
import os
import json

from src.core.config import Settings
from src.core.database import Base
from src.main import app
from src.db.session import get_db

# Test database URL
TEST_DATABASE_URL = "postgresql://test_user:test_password@localhost:5432/test_db"

# Create test engine
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session(test_db):
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="module")
def test_client():
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

@pytest.fixture(scope="function")
def sample_image():
    image_path = Path("tests/test_data/sample_receipt.png")
    return {
        "path": str(image_path),
        "content": b"sample image content",
        "metadata": {"width": 800, "height": 600}
    }

@pytest.fixture(scope="function")
def mock_gcp_response():
    return {
        "text": "Sample Store\nTotal: 1000 JPY\nDate: 2024-01-01",
        "locale": "ja",
        "confidence": 0.95
    }

@pytest.fixture(scope="function")
def sample_receipt_data():
    return {
        "store_name": "Sample Store",
        "total_amount": 1000.0,
        "currency_type": "JPY",
        "payment_method": "CASH",
        "time": "2024-01-01T10:00:00",
        "items": [
            {"product_name": "Item 1", "price": 500.0, "quantity": 1},
            {"product_name": "Item 2", "price": 500.0, "quantity": 1}
        ]
    }
