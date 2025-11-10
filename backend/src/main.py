import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from src.routers.stt_routes import router as stt_router
from src.routers.summarizer_routes import router as summarizer_router
from src.routers.unified_routes import router as unified_router

app = FastAPI(
    title="Vietnamese STT News Summarization API",
    description="Vietnamese STT News Summarization API",
    version="0.1.0",
)

app.include_router(stt_router)
app.include_router(summarizer_router)
app.include_router(unified_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
