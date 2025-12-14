# Multilingual TTS System

Arabic-English Text-to-Speech with Neural Voices using Edge-TTS.

## Features

- 🎙️ **Neural Voices** - High-quality Microsoft Edge neural TTS
- 🌐 **Multilingual** - Arabic (Egyptian) and English (US) support
- 🔀 **Code-Switching** - Seamless Arabic-English mixed text
- 📁 **File Upload** - Upload .txt files for batch synthesis
- ⬇️ **Download** - Save generated audio as MP3
- 🎨 **Modern UI** - Premium dark theme with glassmorphism

## Quick Start

### 1. Backend Setup

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app:app --reload --port 8000
```

### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

### 3. Open Browser

Navigate to `http://localhost:5173`

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/synthesize` | POST | Text to speech |
| `/upload-text` | POST | Upload .txt file |
| `/download/{filename}` | GET | Download audio |
| `/voices` | GET | List voices |
| `/status` | GET | Health check |

## Voice Options

| Language | Voice (Female) | Voice (Male) |
|----------|----------------|--------------|
| Arabic | ar-EG-SalmaNeural | ar-EG-ShakirNeural |
| English | en-US-JennyNeural | en-US-GuyNeural |

## Project Structure

```
TTS/
├── backend/
│   ├── app.py              # FastAPI application
│   ├── config.py           # Voice configuration
│   ├── services/
│   │   └── tts_engine.py   # Edge-TTS wrapper
│   └── utils/
│       ├── text_processing.py
│       ├── language_detector.py
│       ├── audio_postprocess.py
│       └── file_manager.py
└── frontend/
    └── src/
        ├── components/     # React components
        ├── pages/          # Page components
        └── api/            # API layer
```

## Requirements

- Python 3.8+
- Node.js 18+
- Internet connection (Edge-TTS requires online access)
