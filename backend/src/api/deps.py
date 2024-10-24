# backend/src/api/deps.py

from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from ..db.session import get_db
from ..core.config import settings

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db_session() -> Generator[Session, None, None]:
    """Get database session"""
    try:
        db = next(get_db())
        yield db
    finally:
        db.close()

async def verify_token(token: str = Depends(oauth2_scheme)) -> str:
    """Verify authentication token"""
    # Implement your token verification logic here
    return token
