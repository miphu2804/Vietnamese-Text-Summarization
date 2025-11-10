# TMG301 Project - Vietnamese News Speech-to-Text Summarization

Vietnamese News Speech-to-Text Summarization Full-Stack Application with FastAPI backend and React frontend, using ChunkFormer for STT and ViT5 for text summarization.

## Project Structure

```
TMG301_Project/
├── README.md
├── .gitignore
├── .python-version
├── requirements.txt
├── backend/
│   ├── pyproject.toml
│   ├── uv.lock
│   └── src/
│       ├── main.py                    # FastAPI application entry point
│       ├── app_config.py              # Application configuration
│       ├── unified_service.py         # Unified service for STT + Summarization pipeline
│       ├── engine/
│       │   ├── STT.py                 # Speech-to-Text engine (ChunkFormer)
│       │   └── summarizer.py          # Text-to-Summary engine (ViT5)
│       ├── routers/
│       │   ├── stt_routes.py          # STT API endpoints
│       │   ├── summarizer_routes.py   # Summarization API endpoints
│       │   └── unified_routes.py      # Unified pipeline endpoints
│       ├── services/
│       │   └── api.py                 # API service layer
│       └── schemas/
│           ├── stt_schema.py          # STT response schemas
│           ├── summarizer_schema.py   # Summarization request schemas
│           └── unified_schema.py      # Unified pipeline schemas
└── frontend/
    ├── package.json                   # Node.js dependencies
    ├── vite.config.ts                 # Vite configuration
    ├── tailwind.config.js             # Tailwind CSS configuration
    ├── postcss.config.js              # PostCSS configuration
    ├── tsconfig.json                  # TypeScript configuration
    └── src/
        ├── main.tsx                   # React application entry point
        ├── App.tsx                    # Main application component
        ├── index.css                  # Global styles
        ├── store/
        │   ├── index.ts               # Redux store configuration
        │   └── slices/
        │       ├── transcriptionSlice.ts    # Transcription state
        │       └── summarizationSlice.ts   # Summarization state
        ├── services/
        │   └── api.ts                 # API integration with backend
        ├── hooks/
        │   ├── useTranscription.ts    # Transcription hook
        │   ├── useSummarization.ts    # Summarization hook
        │   └── useUnifiedProcessing.ts # Unified pipeline hook
        ├── components/
        │   ├── audio/
        │   │   ├── AudioUploader.tsx  # File upload component
        │   │   └── AudioPlayer.tsx    # Audio playback component
        │   ├── layout/
        │   │   ├── Header.tsx         # Navigation header
        │   │   └── Layout.tsx         # Main layout component
        │   └── common/
        │       ├── LoadingSpinner.tsx # Loading indicator
        │       └── ErrorMessage.tsx   # Error display component
        └── pages/
            ├── TranscriptionPage.tsx  # Transcription interface
            ├── SummarizationPage.tsx  # Summarization interface
            └── UnifiedPage.tsx        # Unified pipeline interface
```

## Features

- **Speech-to-Text (STT)**: Transcribe Vietnamese news audio using ChunkFormer
- **Text-to-Summary**: Summarize Vietnamese news text using ViT5 seq2seq model
- **Unified Pipeline**: Complete audio → transcription → summary workflow
- **Multi-format Audio Support**: Automatic conversion of various audio formats (MP3, M4A, WAV, FLAC, MP4, AVI) to WAV
- **News Processing**: Specialized for Vietnamese news content
- **Batch Processing**: Support for batch transcription and summarization of multiple news audio files
- **Modern Frontend**: React 18 + TypeScript with Tailwind CSS for responsive UI
- **State Management**: Redux Toolkit for managing application state
- **RESTful API**: Clean FastAPI endpoints with proper error handling
- **CORS Support**: Configured for cross-origin requests
- **Real-time Processing**: Progress tracking and loading states
- **Error Handling**: Comprehensive error management and user feedback

## Prerequisites

### Backend
- Python 3.11+
- UV (Astral Python package manager)

### Frontend
- Node.js 18+
- npm or yarn package manager

## Installation & Setup

### Backend Setup

#### 1. Install UV (if not already installed)

```bash
# Install UV using pip
pip install uv
```

#### 2. Clone and Setup Backend

```bash
# Clone the repository
cd TMG301_Project

# Navigate to backend directory
cd backend

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .

# Or install directly without venv (uses system Python)
uv pip install -e .
```

### Frontend Setup

#### 1. Install Node.js (if not already installed)

```bash
# Verify Node.js installation (requires 18+)
node --version
npm --version

# If not installed, download from https://nodejs.org/ or use version manager:
# nvm install 18
# nvm use 18
```

#### 2. Setup Frontend Dependencies

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Or using yarn (if preferred)
yarn install
```

## Running the Application

### Option 1: Full Stack Development (Recommended)

#### Terminal 1: Start Backend
```bash
cd backend
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

#### Terminal 2: Start Frontend
```bash
cd frontend
npm run dev
```

Then visit:
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

### Option 2: Backend Only

```bash
cd backend
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

### Option 3: Using Traditional Python (Alternative)

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

### Option 4: Frontend Build for Production

```bash
cd frontend
npm run build
npm run preview  # Preview production build
```

## API Endpoints

### Unified Pipeline (Main Feature)

#### Complete Audio-to-Summary Processing
```http
POST /unified/transcribe-and-summarize
Content-Type: multipart/form-data

file: <news_audio_file>
```

**Response:**
```json
{
  "transcription": "Hôm nay Chính phủ đã ban hành nghị định mới về kinh tế số...",
  "summary": "Chính phủ ban hành nghị định mới về kinh tế số nhằm thúc đẩy chuyển đổi số quốc gia.",
  "original_audio_path": "/tmp/audio_20231210_123456.wav"
}
```

### Speech-to-Text (STT)

#### Single News Audio Transcription
```http
POST /stt/transcribe
Content-Type: multipart/form-data

file: <news_audio_file>
chunk_size: 64 (optional)
left_context_size: 128 (optional)
right_context_size: 128 (optional)
total_batch_duration: 14400 (optional)
return_timestamps: false (optional)
```

**Response:**
```json
{
  "transcription": "Hôm nay Chính phủ đã ban hành nghị định mới về kinh tế số...",
  "original_audio_path": "/tmp/audio_20231210_123456.wav"
}
```

#### Batch News Audio Transcription
```http
POST /stt/batch-transcribe
Content-Type: multipart/form-data

files: <news_audio_files>[]
chunk_size: 64 (optional)
left_context_size: 128 (optional)
right_context_size: 128 (optional)
total_batch_duration: 1800 (optional)
```

**Response:**
```json
[
  {
    "transcription": "Tin tức đầu tiên...",
    "original_audio_path": "/tmp/audio_1.wav"
  },
  {
    "transcription": "Tin tức thứ hai...",
    "original_audio_path": "/tmp/audio_2.wav"
  }
]
```

### Text-to-Summary (Summarizer)

#### JSON-based News Summarization
```http
POST /summarizer/summarize
Content-Type: application/json

{
  "text": "Your Vietnamese news text here",
  "max_length": 256
}
```

**Response:**
```json
{
  "summary": "Tóm tắt nội dung tin tức..."
}
```

#### Form-based News Summarization
```http
POST /summarizer/summarize-form
Content-Type: application/json

{
  "content": "Your Vietnamese news text here"
}
```

**Response:**
```json
{
  "summary": "Tóm tắt nội dung tin tức..."
}
```

## Usage Examples

### Testing with curl

#### Test Unified Pipeline
```bash
curl -X POST "http://localhost:8000/unified/transcribe-and-summarize" \
  -F "file=@news_audio.mp3"
```

#### Test STT Only
```bash
curl -X POST "http://localhost:8000/stt/transcribe" \
  -F "file=@news_audio.mp3" \
  -F "chunk_size=64" \
  -F "return_timestamps=true"
```

#### Test Summarizer Only
```bash
curl -X POST "http://localhost:8000/summarizer/summarize" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hôm nay Chính phủ đã ban hành nghị định mới về kinh tế số nhằm thúc đẩy chuyển đổi số quốc gia và tăng cường năng lực cạnh tranh trong bối cảnh cuộc cách mạng công nghiệp lần thứ tư.",
    "max_length": 100
  }'
```

### Frontend Usage

The React frontend provides an intuitive interface for all features:

1. **Unified Processing Page**: Upload audio → Get transcription + summary
2. **Transcription Page**: Upload audio → Get transcription only
3. **Summarization Page**: Input/paste text → Get summary

### Backend Service Usage

```python
from src.unified_service import UnifiedService

# Initialize service
service = UnifiedService()

# Process news video (auto-converts to WAV)
result = service.transcribe_and_summarize("news_video.mp4")

print(f"Transcription: {result.transcription}")
print(f"Summary: {result.summary}")
```

## STT Model Parameters Explanation

### ChunkFormer Parameters

- **chunk_size**: Audio segment size (default: 64 frames = 640ms)
- **left_context_size**: Context frames before current chunk (default: 128 = 1.28s)
- **right_context_size**: Context frames after current chunk (default: 128 = 1.28s)
- **total_batch_duration**: Max audio duration per batch in centiseconds (default: 14400 = 144s)
- **return_timestamps**: Include word-level timestamps (default: false)

### Optimal Settings for Vietnamese

- **News Content**: Use default settings for balanced speed/accuracy
- **Long Audio**: Increase `total_batch_duration` for better context
- **High Accuracy**: Decrease `chunk_size` and increase context sizes

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Spec**: http://localhost:8000/openapi.json


