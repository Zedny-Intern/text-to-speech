# TTS Full Technical Documentation

## Overview

Multilingual Text-to-Speech system supporting Arabic, English, and code-switching using Microsoft Edge Neural Voices.

---

## Architecture

```
Frontend (React + Vite)
   │
   │ HTTP/REST
   ▼
Backend (FastAPI)
   │
   │ Text Processing Pipeline
   ▼
TTS Engine (Edge-TTS)
   │
   ▼
Audio Files (MP3/WAV)
```

---

## Backend Components

### 1. Text Processing (`utils/text_processing.py`)

- **normalize_text()** - Remove unsupported characters, normalize whitespace
- **segment_sentences()** - Split text on punctuation (Arabic & English)
- **chunk_long_sentence()** - Break sentences > 500 chars
- **prepare_text()** - Full pipeline

### 2. Language Detection (`utils/language_detector.py`)

- **is_arabic()** - Check for Arabic Unicode range
- **is_english()** - Check for Latin characters
- **detect_language()** - Returns 'ar', 'en', or dominant language for mixed
- **detect_per_sentence()** - Language per sentence for code-switching

### 3. TTS Engine (`services/tts_engine.py`)

- **synthesize_text()** - Single text synthesis
- **synthesize_sentences()** - Batch synthesis with per-sentence voices
- **get_configured_voices()** - Available voice options

### 4. Audio Post-Processing (`utils/audio_postprocess.py`)

- **concatenate_audio_files()** - Merge sentence audio files
- **normalize_audio()** - Volume normalization
- **convert_to_wav()** - Format conversion

---

## API Reference

### POST /synthesize

Synthesize text to speech.

**Request:**
```json
{
  "text": "Hello مرحبا",
  "language": "auto",
  "gender": "female"
}
```

**Response:**
```json
{
  "success": true,
  "filename": "speech_20231201_123456_abc12345.mp3",
  "download_url": "/download/speech_20231201_123456_abc12345.mp3",
  "duration_ms": 1523.45,
  "text_length": 12,
  "sentences_count": 1
}
```

### POST /upload-text

Upload .txt file for synthesis.

**Request:** `multipart/form-data` with file + query params
- `file`: .txt file
- `language`: ar, en, or auto
- `gender`: male or female

### GET /download/{filename}

Download generated audio file.

### GET /voices

Get available voice configurations.

### GET /status

Health check endpoint.

---

## Voice Configurations

| Language | Gender | Voice ID |
|----------|--------|----------|
| Arabic (Egyptian) | Female | ar-EG-SalmaNeural |
| Arabic (Egyptian) | Male | ar-EG-ShakirNeural |
| English (US) | Female | en-US-JennyNeural |
| English (US) | Male | en-US-GuyNeural |

---

## Code-Switching Strategy

Edge-TTS handles code-switching natively. For best results:

1. Text is segmented into sentences
2. Each sentence's dominant language is detected
3. Appropriate voice is selected per sentence
4. Audio segments are concatenated with 200ms silence gaps

---

## Hardware Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| CPU | Any modern | Multi-core |
| RAM | 2GB | 4GB |
| GPU | Not required | Not required |
| Network | Required | Required |

---

## Future Enhancements

- [ ] Real-time WebSocket streaming
- [ ] Offline TTS with Coqui/Piper fallback
- [ ] More language/dialect support
- [ ] SSML support for prosody control
