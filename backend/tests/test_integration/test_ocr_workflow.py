# tests/test_integration/test_ocr_workflow.py

import pytest
from pathlib import Path
from src.services.ocr_service import OCRService
from src.services.file_service import FileService
from src.services.db_service import DBService
from src.core.logger import setup_logger

logger = setup_logger(__name__)

@pytest.fixture
def workflow_services(db_session):
    return {
        "ocr": OCRService(),
        "file": FileService(),
        "db": DBService(db_session)
    }

def test_complete_receipt_processing_workflow(
    workflow_services,
    test_dirs,
    sample_image,
    mock_gcp_response
):
    # Setup test image
    source_file = test_dirs["not_yet"] / "test_receipt.png"
    with open(source_file, "wb") as f:
        f.write(sample_image["content"])
    
    # 1. Move file to processing directory
    workflow_services["file"].move_file(
        str(source_file),
        str(test_dirs["current"] / "test_receipt.png")
    )
    
    # 2. Process image with OCR
    with patch('src.services.ocr_service.vision.ImageAnnotatorClient') as mock_client:
        mock_client.return_value.text_detection.return_value.text_annotations = [
            Mock(description=mock_gcp_response["text"],
                 locale=mock_gcp_response["locale"])
        ]
        ocr_result = workflow_services["ocr"].process_image(
            str(test_dirs["current"] / "test_receipt.png")
        )
    
    assert ocr_result["success"] is True
    
    # 3. Extract receipt data
    receipt_data = workflow_services["ocr"].extract_receipt_data(ocr_result["text"])
    
    # 4. Save to database
    receipt = workflow_services["db"].create_receipt(receipt_data)
    
    assert receipt is not None
    assert receipt.store_name == "Sample Store"
    assert receipt.total_amount == 1000.0

def test_error_handling_in_workflow(
    workflow_services,
    test_dirs,
    sample_image
):
    # Setup test image with invalid content
    source_file = test_dirs["not_yet"] / "invalid_receipt.png"
    with open(source_file, "wb") as f:
        f.write(b"invalid image content")
    
    # 1. Move file to processing directory
    workflow_services["file"].move_file(
        str(source_file),
        str(test_dirs["current"] / "invalid_receipt.png")
    )
    
    # 2. Process image with OCR (should fail)
    ocr_result = workflow_services["ocr"].process_image(
        str(test_dirs["current"] / "invalid_receipt.png")
    )
    
    assert ocr_result["success"] is False
    
    # 3. Verify file is moved to error directory
    workflow_services["file"].move_file(
        str(test_dirs["current"] / "invalid_receipt.png"),
        str(test_dirs["error"] / "invalid_receipt.png")
    )
    
    assert (test_dirs["error"] / "invalid_receipt.png").exists()
