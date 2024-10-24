import pytest
import os
from pathlib import Path
from src.services.file_service import FileService
from src.core.logger import setup_logger

logger = setup_logger(__name__)

@pytest.fixture
def file_service():
    return FileService()

@pytest.fixture
def test_dirs(tmp_path):
    dirs = {
        "not_yet": tmp_path / "01notYet",
        "current": tmp_path / "02current",
        "txt": tmp_path / "03txt",
        "error": tmp_path / "99error"
    }
    for dir_path in dirs.values():
        dir_path.mkdir()
    return dirs

def test_move_file_success(file_service, test_dirs, sample_image):
    source_file = test_dirs["not_yet"] / "test.png"
    target_file = test_dirs["current"] / "test.png"
    
    # Create test file
    with open(source_file, "wb") as f:
        f.write(sample_image["content"])
    
    result = file_service.move_file(str(source_file), str(target_file))
    
    assert result is True
    assert not source_file.exists()
    assert target_file.exists()

def test_move_file_source_not_exists(file_service, test_dirs):
    source_file = test_dirs["not_yet"] / "nonexistent.png"
    target_file = test_dirs["current"] / "nonexistent.png"
    
    result = file_service.move_file(str(source_file), str(target_file))
    
    assert result is False

def test_create_directory_success(file_service, tmp_path):
    new_dir = tmp_path / "new_directory"
    
    result = file_service.create_directory(str(new_dir))
    
    assert result is True
    assert new_dir.exists()
    assert new_dir.is_dir()

def test_process_directory(file_service, test_dirs, sample_image):
    # Create test files
    test_files = ["test1.png", "test2.png"]
    for file_name in test_files:
        with open(test_dirs["not_yet"] / file_name, "wb") as f:
            f.write(sample_image["content"])
    
    processed_files = file_service.process_directory(
        str(test_dirs["not_yet"]),
        str(test_dirs["current"])
    )
    
    assert len(processed_files) == len(test_files)
    for file_name in test_files:
        assert not (test_dirs["not_yet"] / file_name).exists()
        assert (test_dirs["current"] / file_name).exists()
