# backend/src/services/file_service.py

import shutil
from pathlib import Path
from typing import List, Optional
from ..core.logger import setup_logger

logger = setup_logger(__name__)

class FileService:
    def __init__(self):
        pass

    def move_file(self, source: str, destination: str) -> bool:
        """Move file from source to destination"""
        try:
            source_path = Path(source)
            dest_path = Path(destination)

            if not source_path.exists():
                logger.error(f"Source file does not exist: {source}")
                return False

            # Create destination directory if it doesn't exist
            dest_path.parent.mkdir(parents=True, exist_ok=True)

            # Move file
            shutil.move(str(source_path), str(dest_path))
            logger.info(f"File moved from {source} to {destination}")
            return True

        except Exception as e:
            logger.error(f"Error moving file: {str(e)}", exc_info=True)
            return False

    def create_directory(self, path: str) -> bool:
        """Create directory if it doesn't exist"""
        try:
            Path(path).mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            logger.error(f"Error creating directory: {str(e)}", exc_info=True)
            return False

    def process_directory(self, source_dir: str, dest_dir: str) -> List[str]:
        """Process all files in source directory"""
        processed_files = []
        source_path = Path(source_dir)

        try:
            for file_path in source_path.glob('*'):
                if file_path.is_file():
                    dest_file = Path(dest_dir) / file_path.name
                    if self.move_file(str(file_path), str(dest_file)):
                        processed_files.append(str(file_path))
        except Exception as e:
            logger.error(f"Error processing directory: {str(e)}", exc_info=True)

        return processed_files
