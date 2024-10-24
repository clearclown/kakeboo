# [DEBUG] : FastAPIアプリケーションの設定
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import receipt, item
from src.core.config import settings
from src.db.models.base import Base
from src.db.session import engine
from src.core.logger import setup_logger

# [DEBUG] : ロガーの設定
logger = setup_logger(__name__)

# [DEBUG] : データベーステーブルの作成
Base.metadata.create_all(bind=engine)

# [DEBUG] : FastAPIアプリケーションのインスタンス作成
app = FastAPI(
    title="Receipt OCR API",
    description="API for processing and managing receipts"
)

# [DEBUG] : CORSの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# [DEBUG] : ルーターのインクルード
app.include_router(receipt.router, prefix="/api/v1", tags=["receipts"])
app.include_router(item.router, prefix="/api/v1", tags=["items"])

@app.on_event("startup")
async def startup_event():
    """アプリケーションの初期化"""
    # [DEBUG] : アプリケーションの起動
    logger.info("Starting application")
    settings.validate_paths()

if __name__ == "__main__":
    import uvicorn
    # [DEBUG] : アプリケーションの起動
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
