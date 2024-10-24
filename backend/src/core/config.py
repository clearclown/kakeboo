from pydantic_settings import BaseSettings
from pathlib import Path
from typing import Optional
from functools import lru_cache

class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    # GCP settings
    GCP_CREDENTIALS_PATH: str = "./src/google/gcpVision.json"

    # File paths with default values
    DATA_DIR: Path = Path("./../../data/pics")
    LOGS_DIR: Path = Path("./../../logs/")

    # Directory paths
    NOT_YET_DIR: Path = Path("./../../data/pics/01notYet")
    CURRENT_DIR: Path = Path("./../../data/pics/02current")
    TXT_DIR: Path = Path("./../../data/pics/03txt")
    MD_DIR: Path = Path("./../../data/pics/04md")
    DONE_DIR: Path = Path("./../../data/pics/05done")
    ERROR_DIR: Path = Path("./../../data/pics/99error")

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # 未知の環境変数を無視

    def validate_paths(self):
        """Validate and create necessary directories"""
        for path in [
            self.DATA_DIR, self.LOGS_DIR,
            self.NOT_YET_DIR, self.CURRENT_DIR,
            self.TXT_DIR, self.MD_DIR,
            self.DONE_DIR, self.ERROR_DIR
        ]:
            path.mkdir(parents=True, exist_ok=True)

@lru_cache()
def get_settings() -> Settings:
    """キャッシュされた設定を取得"""
    return Settings()

# シングルトンインスタンスの作成
settings = get_settings()
