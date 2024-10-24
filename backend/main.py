# backend/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import receipt, item
from src.core.config import settings
from src.db.session import engine
from src.db.models import Base
from src.core.logger import setup_logger

# Setup logger
logger = setup_logger(__name__)

# Create tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="Receipt OCR API",
    description="API for processing and managing receipts"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(receipt.router, prefix="/api/v1", tags=["receipts"])
app.include_router(item.router, prefix="/api/v1", tags=["items"])

@app.on_event("startup")
async def startup_event():
    """Initialize application"""
    logger.info("Starting application")
    settings.validate_paths()

@app.get("/")
async def hello():
    return {"message": "Hello, World!"}

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup application"""
    logger.info("Shutting down application")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
