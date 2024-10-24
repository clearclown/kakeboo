# backend/src/core/config.py

from pydantic_settings import BaseSettings
from pathlib import Path
from typing import Optional
import os

class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    # GCP settings
    GCP_CREDENTIALS_PATH: str = "./src/google/gcpVision.json"

    # File paths
    DATA_DIR: Path = Path("./data/pics")
    LOGS_DIR: Path = Path("./logs")

    # Directory paths
    NOT_YET_DIR: Path = DATA_DIR / "01notYet"
    CURRENT_DIR: Path = DATA_DIR / "02current"
    TXT_DIR: Path = DATA_DIR / "03txt"
    MD_DIR: Path = DATA_DIR / "04md"
    DONE_DIR: Path = DATA_DIR / "05done"
    ERROR_DIR: Path = DATA_DIR / "99error"

    class Config:
        env_file = ".env"

    def validate_paths(self):
        """Validate and create necessary directories"""
        for path in [
            self.DATA_DIR, self.LOGS_DIR,
            self.NOT_YET_DIR, self.CURRENT_DIR,
            self.TXT_DIR, self.MD_DIR,
            self.DONE_DIR, self.ERROR_DIR
        ]:
            if not path.exists():
                path.mkdir(parents=True, exist_ok=True)

settings = Settings()
