import logging
import os
import tempfile
from typing import List

from fastapi import APIRouter, File, HTTPException, UploadFile

from backend.src.engine.STT import SpeechToText
from src.schemas.stt_schema import STTResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/stt", tags=["speech-to-text"])

stt_service = SpeechToText()


@router.post("/transcribe", response_model=STTResponse)
async def transcribe_audio(
    file: UploadFile = File(...),
    chunk_size: int = 64,
    left_context_size: int = 128,
    right_context_size: int = 128,
    total_batch_duration: int = 14400,
    return_timestamps: bool = False,
):
    """Transcribe audio file to Vietnamese text using ChunkFormer"""
    if not stt_service:
        raise HTTPException(status_code=503, detail="STT service not available")

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name

        transcription = stt_service.transcribe(
            audio_path=tmp_path,
            chunk_size=chunk_size,
            left_context_size=left_context_size,
            right_context_size=right_context_size,
            total_batch_duration=total_batch_duration,
            return_timestamps=return_timestamps,
        )

        os.unlink(tmp_path)

        return STTResponse(transcription=transcription)

    except Exception as e:
        logger.error(f"Transcription error: {e}")
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")


@router.post("/batch-transcribe", response_model=List[STTResponse])
async def batch_transcribe_audio(
    files: List[UploadFile] = File(...),
    chunk_size: int = 64,
    left_context_size: int = 128,
    right_context_size: int = 128,
    total_batch_duration: int = 1800,
):
    """Batch transcribe multiple audio files to Vietnamese text"""
    if not stt_service:
        raise HTTPException(status_code=503, detail="STT service not available")

    try:
        audio_paths = []
        temp_files = []

        for file in files:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                content = await file.read()
                tmp.write(content)
                audio_paths.append(tmp.name)
                temp_files.append(tmp.name)

        transcriptions = stt_service.batch_transcribe(
            audio_paths=audio_paths,
            chunk_size=chunk_size,
            left_context_size=left_context_size,
            right_context_size=right_context_size,
            total_batch_duration=total_batch_duration,
        )

        for temp_file in temp_files:
            os.unlink(temp_file)

        return [STTResponse(transcription=text) for text in transcriptions]

    except Exception as e:
        logger.error(f"Batch transcription error: {e}")
        raise HTTPException(
            status_code=500, detail=f"Batch transcription failed: {str(e)}"
        )
