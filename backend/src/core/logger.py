# backend/src/core/logger.py

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from datetime import datetime
import os

def setup_logger(name: str, log_dir: str = "./logs") -> logging.Logger:
    """Setup logger with file and console handlers"""

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Create logs directory if not exists
    Path(log_dir).mkdir(parents=True, exist_ok=True)

    # Create formatters
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_formatter = logging.Formatter(
        '%(levelname)s: %(message)s'
    )

    # File handler (with rotation)
    log_file = Path(log_dir) / f"{datetime.now().strftime('%Y%m%d')}.log"
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)

    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

def log_error(logger: logging.Logger, error: Exception, context: str = ""):
    """Log error with context"""
    logger.error(f"{context} - Error: {str(error)}", exc_info=True)

def log_info(logger: logging.Logger, message: str, context: str = ""):
    """Log info with context"""
    logger.info(f"{context} - {message}")
