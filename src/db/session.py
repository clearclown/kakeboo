# [DEBUG] : SQLAlchemyのエンジンとセッションを設定
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.core.config import settings
from src.db.models.base import Base

# [DEBUG] : データベースエンジンの作成
engine = create_engine(settings.DATABASE_URL)

# [DEBUG] : SessionLocalクラスの作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """[DEBUG] : データベースセッションの依存関係"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
