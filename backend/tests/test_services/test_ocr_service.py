# tests/test_services/test_ocr_service.py
import pytest
from unittest.mock import Mock, patch
from src.services.ocr_service import OCRService
from src.core.logger import setup_logger

logger = setup_logger(__name__)

@pytest.fixture
def ocr_service():
    return OCRService()

def test_process_image_success(ocr_service, sample_image, mock_gcp_response):
    with patch('src.services.ocr_service.vision.ImageAnnotatorClient') as mock_client:
        mock_client.return_value.text_detection.return_value.text_annotations = [
            Mock(description=mock_gcp_response["text"],
                 locale=mock_gcp_response["locale"])
        ]
        
        result = ocr_service.process_image(sample_image["path"])
        
        assert result["success"] is True
        assert result["text"] == mock_gcp_response["text"]
        assert result["locale"] == mock_gcp_response["locale"]

def test_process_image_no_text(ocr_service, sample_image):
    with patch('src.services.ocr_service.vision.ImageAnnotatorClient') as mock_client:
        mock_client.return_value.text_detection.return_value.text_annotations = []
        
        result = ocr_service.process_image(sample_image["path"])
        
        assert result["success"] is False
        assert "No text detected" in result["error"]

def test_process_image_api_error(ocr_service, sample_image):
    with patch('src.services.ocr_service.vision.ImageAnnotatorClient') as mock_client:
        mock_client.return_value.text_detection.side_effect = Exception("API Error")
        
        result = ocr_service.process_image(sample_image["path"])
        
        assert result["success"] is False
        assert "API Error" in result["error"]

def test_extract_text_with_valid_response(ocr_service, mock_gcp_response):
    text = ocr_service.extract_text(mock_gcp_response["text"])
    assert isinstance(text, str)
    assert "Sample Store" in text
    assert "1000 JPY" in text

def test_validate_results_success(ocr_service, mock_gcp_response):
    result = ocr_service.validate_results({
        "text": mock_gcp_response["text"],
        "locale": mock_gcp_response["locale"]
    })
    assert result is True

def test_validate_results_failure(ocr_service):
    result = ocr_service.validate_results({
        "text": "",
        "locale": None
    })
    assert result is False
