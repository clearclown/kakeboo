from fastapi import FastAPI, BackgroundTasks
from src.core.config import settings
from src.core.logging import logger
from src.services.file_service import FileService
from src.services.ocr_service import OCRService
from src.services.db_service import DBService
from src.db.session import init_db

app = FastAPI(title="Receipt Processing API")

@app.get("/")
async def root():
    # デバッグメッセージを表示
    print("[DEBUG] : Root endpoint accessed")
    return {"message": "Receipt Processing Service"}

# メイン関数
if __name__ == "__main__":
    # デバッグメッセージを表示
    print("[DEBUG] : Starting the application")
    import uvicorn
    # デバッグメッセージを表示
    print("[DEBUG] : Running uvicorn server")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
