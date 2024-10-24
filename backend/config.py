# config.py
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    DATABASE_URL: str
    MYSQL_ROOT_PASSWORD: str
    MYSQL_DATABASE: str
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    GOOGLE_APPLICATION_CREDENTIALS: str = "path/to/your/credentials.json"

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
