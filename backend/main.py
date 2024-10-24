from fastapi import FastAPI, BackgroundTasks
from src.core.config import settings
from src.core.logging import logger
from src.services.file_service import FileService
from src.services.ocr_service import OCRService
from src.services.db_service import DBService
from src.db.session import init_db

app = FastAPI(title="Receipt Processing API")

# データベース初期化
@app.on_event("startup")
async def startup_event():
    init_db()
    logger.info("Database initialized")

@app.get("/")
async def root():
    return {"message": "Receipt Processing Service"}

@app.post("/process")
async def process_receipts(background_tasks: BackgroundTasks):
    """未処理のレシートを処理するエンドポイント"""
    background_tasks.add_task(process_pending_receipts)
    return {"message": "Processing started"}

async def process_pending_receipts():
    """未処理のレシートを処理する非同期タスク"""
    file_service = FileService()
    ocr_service = OCRService()
    db_service = DBService()

    files = file_service.get_files_to_process()
    logger.info(f"Found {len(files)} files to process")

    for file_path in files:
        try:
            # ファイルを現在の処理フォルダに移動
            current_path = file_service.move_to_current(file_path)

            # OCR処理実行
            ocr_result = ocr_service.process_image(current_path)

            # テキストファイル保存
            file_service.save_text_result(file_path.stem, ocr_result.text)

            # 構造化データをJSONとして保存
            parsed_data = ocr_service.parse_receipt_data(ocr_result.text)
            file_service.save_json_result(file_path.stem, parsed_data)

            # データベースに保存
            db_service.save_receipt(parsed_data)

            # 処理完了したファイルを移動
            file_service.move_to_done(current_path)
            logger.info(f"Successfully processed {file_path.name}")

        except Exception as e:
            logger.error(f"Error processing {file_path.name}: {str(e)}")
            file_service.move_to_error(file_path, str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
