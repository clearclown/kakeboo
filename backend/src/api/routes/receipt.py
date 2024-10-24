# backend/src/api/routes/receipt.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from ...db.session import get_db
from ...services.db_service import DBService
from ...services.ocr_service import OCRService
from ...utils.validators import ReceiptValidator
from ...core.logger import setup_logger

router = APIRouter()
logger = setup_logger(__name__)

@router.post("/receipts/")
async def create_receipt(
    receipt_data: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """Create new receipt"""
    # Validate receipt data
    validator = ReceiptValidator()
    validation_result = validator.validate(receipt_data)
    if not validation_result["valid"]:
        raise HTTPException(
            status_code=400,
            detail={"errors": validation_result["errors"]}
        )

    # Create receipt
    db_service = DBService(db)
    receipt = db_service.create_receipt(receipt_data)

    if not receipt:
        raise HTTPException(
            status_code=500,
            detail="Error creating receipt"
        )

    return receipt

@router.get("/receipts/{receipt_id}")
async def get_receipt(
    receipt_id: str,
    db: Session = Depends(get_db)
):
    """Get receipt by ID"""
    db_service = DBService(db)
    receipt = db_service.get_receipt(receipt_id)

    if not receipt:
        raise HTTPException(
            status_code=404,
            detail=f"Receipt {receipt_id} not found"
        )

    return receipt

@router.put("/receipts/{receipt_id}")
async def update_receipt(
    receipt_id: str,
    receipt_data: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """Update receipt"""
    # Validate receipt data
    validator = ReceiptValidator()
    validation_result = validator.validate(receipt_data)
    if not validation_result["valid"]:
        raise HTTPException(
            status_code=400,
            detail={"errors": validation_result["errors"]}
        )

    # Update receipt
    db_service = DBService(db)
    receipt = db_service.update_receipt(receipt_id, receipt_data)

    if not receipt:
        raise HTTPException(
            status_code=404,
            detail=f"Receipt {receipt_id} not found"
        )

    return receipt

@router.delete("/receipts/{receipt_id}")
async def delete_receipt(
    receipt_id: str,
    db: Session = Depends(get_db)
):
    """Delete receipt"""
    db_service = DBService(db)
    success = db_service.delete_receipt(receipt_id)

    if not success:
        raise HTTPException(
            status_code=404,
            detail=f"Receipt {receipt_id} not found"
        )

    return {"message": "Receipt deleted successfully"}

@router.post("/receipts/process-image")
async def process_receipt_image(
    image_path: str,
    db: Session = Depends(get_db)
):
    """Process receipt image with OCR and save data"""
    try:
        # Process image with OCR
        ocr_service = OCRService()
        ocr_result = ocr_service.process_image(image_path)

        if not ocr_result["success"]:
            raise HTTPException(
                status_code=400,
                detail=f"OCR processing failed: {ocr_result['error']}"
            )

        # Extract receipt data
        receipt_data = ocr_service.extract_receipt_data(ocr_result["text"])

        # Create receipt in database
        db_service = DBService(db)
        receipt = db_service.create_receipt(receipt_data)

        if not receipt:
            raise HTTPException(
                status_code=500,
                detail="Error creating receipt"
            )

        return receipt

    except Exception as e:
        logger.error(f"Error processing receipt image: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
