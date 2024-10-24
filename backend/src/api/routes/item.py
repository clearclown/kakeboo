# backend/src/api/routes/item.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from ...db.session import get_db
from ...services.db_service import DBService
from ...utils.validators import ItemValidator
from ...core.logger import setup_logger

router = APIRouter()
logger = setup_logger(__name__)

@router.post("/items/")
async def create_item(
    receipt_id: str,
    item_data: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """Create new item for a receipt"""
    # Validate item data
    validator = ItemValidator()
    validation_result = validator.validate(item_data)
    if not validation_result["valid"]:
        raise HTTPException(
            status_code=400,
            detail={"errors": validation_result["errors"]}
        )

    # Create item
    db_service = DBService(db)
    item = db_service.create_item(receipt_id, item_data)

    if not item:
        raise HTTPException(
            status_code=500,
            detail="Error creating item"
        )

    return item

@router.get("/items/{item_id}")
async def get_item(
    item_id: int,
    db: Session = Depends(get_db)
):
    """Get item by ID"""
    db_service = DBService(db)
    item = db_service.get_item(item_id)

    if not item:
        raise HTTPException(
            status_code=404,
            detail=f"Item {item_id} not found"
        )

    return item

@router.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item_data: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """Update item"""
    # Validate item data
    validator = ItemValidator()
    validation_result = validator.validate(item_data)
    if not validation_result["valid"]:
        raise HTTPException(
            status_code=400,
            detail={"errors": validation_result["errors"]}
        )

    # Update item
    db_service = DBService(db)
    item = db_service.update_item(item_id, item_data)

    if not item:
        raise HTTPException(
            status_code=404,
            detail=f"Item {item_id} not found"
        )

    return item

@router.delete("/items/{item_id}")
async def delete_item(
    item_id: int,
    db: Session = Depends(get_db)
):
    """Delete item"""
    db_service = DBService(db)
    success = db_service.delete_item(item_id)

    if not success:
        raise HTTPException(
            status_code=404,
            detail=f"Item {item_id} not found"
        )

    return {"message": "Item deleted successfully"}
