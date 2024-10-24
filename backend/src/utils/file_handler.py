# backend/src/utils/file_handler.py

import json
from pathlib import Path
from typing import Dict, Any, Optional
from ..core.logger import setup_logger

logger = setup_logger(__name__)

class FileHandler:
    @staticmethod
    def read_file(file_path: str) -> Optional[str]:
        """Read file content"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Error reading file: {str(e)}", exc_info=True)
            return None

    @staticmethod
    def write_file(file_path: str, content: str) -> bool:
        """Write content to file"""
        try:
            Path(file_path).parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            logger.error(f"Error writing file: {str(e)}", exc_info=True)
            return False

    @staticmethod
    def read_json(file_path: str) -> Optional[Dict[str, Any]]:
        """Read JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error reading JSON: {str(e)}", exc_info=True)
            return None

    @staticmethod
    def write_json(file_path: str, data: Dict[str, Any]) -> bool:
        """Write data to JSON file"""
        try:
            Path(file_path).parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            logger.error(f"Error writing JSON: {str(e)}", exc_info=True)
            return False

    @staticmethod
    def validate_file(file_path: str, allowed_extensions: set = None) -> bool:
        """Validate file existence and extension"""
        try:
            path = Path(file_path)
            if not path.exists():
                return False
            if allowed_extensions and path.suffix.lower() not in allowed_extensions:
                return False
            return True
        except Exception as e:
            logger.error(f"Error validating file: {str(e)}", exc_info=True)
            return False
