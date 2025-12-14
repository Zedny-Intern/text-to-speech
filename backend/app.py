from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional
import os
import asyncio
from datetime import datetime

from config import VOICES, AUDIO_OUTPUT_DIR, MAX_TEXT_LENGTH
from utils.text_processing import prepare_text
from utils.language_detector import detect_language, detect_per_sentence
from utils.audio_postprocess import concatenate_audio_files
from utils.file_manager import ensure_dir, generate_filename, list_audio_files
from utils.logger import log_synthesis, log_error, log_request
from services.tts_engine import synthesize_text, synthesize_sentences, get_configured_voices

# Initialize FastAPI app
app = FastAPI(
    title="Multilingual TTS API",
    description="Arabic-English Text-to-Speech API with Edge-TTS",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure output directory exists
ensure_dir(AUDIO_OUTPUT_DIR)

# Request models
class SynthesisRequest(BaseModel):
    text: str
    language: Optional[str] = "auto"  # 'ar', 'en', or 'auto'
    gender: Optional[str] = "female"  # 'male' or 'female'

class TextUploadRequest(BaseModel):
    language: Optional[str] = "auto"
    gender: Optional[str] = "female"


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Multilingual TTS API", "version": "1.0.0"}


@app.get("/status")
async def status():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "TTS API"
    }


@app.get("/voices")
async def get_voices():
    """Get available voice options."""
    return {
        "voices": get_configured_voices(),
        "languages": ["ar", "en", "auto"],
        "genders": ["male", "female"]
    }


@app.post("/synthesize")
async def synthesize(request: SynthesisRequest):
    """
    Synthesize text to speech.
    Supports Arabic, English, and mixed language text.
    """
    log_request("/synthesize", "POST", {"text_len": len(request.text)})
    
    # Validate input
    if not request.text or not request.text.strip():
        raise HTTPException(status_code=400, detail="Text is required")
    
    if len(request.text) > MAX_TEXT_LENGTH:
        raise HTTPException(status_code=400, detail=f"Text exceeds maximum length of {MAX_TEXT_LENGTH}")
    
    try:
        start_time = datetime.now()
        
        # Prepare text (normalize and segment)
        sentences = prepare_text(request.text)
        
        if request.language == "auto":
            # Detect language per sentence
            sentences_with_lang = detect_per_sentence(sentences)
        else:
            # Use specified language for all sentences
            sentences_with_lang = [(s, request.language) for s in sentences]
        
        # Synthesize each sentence
        audio_files = await synthesize_sentences(sentences_with_lang, request.gender)
        
        if not audio_files:
            raise HTTPException(status_code=500, detail="Failed to generate audio")
        
        # If multiple files, concatenate them
        if len(audio_files) > 1:
            output_filename = generate_filename("speech", "mp3")
            output_path = os.path.join(AUDIO_OUTPUT_DIR, output_filename)
            concatenate_audio_files(audio_files, output_path)
            
            # Clean up individual segment files
            for f in audio_files:
                if os.path.exists(f):
                    os.remove(f)
        else:
            output_path = audio_files[0]
            output_filename = os.path.basename(output_path)
        
        # Calculate duration
        duration = (datetime.now() - start_time).total_seconds() * 1000
        log_synthesis(request.text[:100], request.language, request.gender, duration)
        
        return {
            "success": True,
            "filename": output_filename,
            "download_url": f"/download/{output_filename}",
            "duration_ms": round(duration, 2),
            "text_length": len(request.text),
            "sentences_count": len(sentences)
        }
        
    except Exception as e:
        log_error("Synthesis failed", str(e))
        raise HTTPException(status_code=500, detail=f"Synthesis failed: {str(e)}")


@app.post("/upload-text")
async def upload_text(
    file: UploadFile = File(...),
    language: str = "auto",
    gender: str = "female"
):
    """Upload a text file for synthesis."""
    log_request("/upload-text", "POST", {"filename": file.filename})
    
    if not file.filename.endswith('.txt'):
        raise HTTPException(status_code=400, detail="Only .txt files are supported")
    
    try:
        # Read file content
        content = await file.read()
        text = content.decode('utf-8')
        
        # Create synthesis request
        request = SynthesisRequest(text=text, language=language, gender=gender)
        
        # Call synthesis endpoint
        return await synthesize(request)
        
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="File encoding not supported. Use UTF-8")
    except Exception as e:
        log_error("File upload failed", str(e))
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@app.get("/download/{filename}")
async def download_audio(filename: str):
    """Download generated audio file."""
    log_request(f"/download/{filename}", "GET")
    
    filepath = os.path.join(AUDIO_OUTPUT_DIR, filename)
    
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Audio file not found")
    
    return FileResponse(
        filepath,
        media_type="audio/mpeg",
        filename=filename
    )


@app.get("/audio-files")
async def get_audio_files():
    """List all generated audio files."""
    files = list_audio_files(AUDIO_OUTPUT_DIR)
    return {"files": files, "count": len(files)}


@app.delete("/audio-files/{filename}")
async def delete_audio_file(filename: str):
    """Delete a specific audio file."""
    filepath = os.path.join(AUDIO_OUTPUT_DIR, filename)
    
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="File not found")
    
    os.remove(filepath)
    return {"success": True, "message": f"Deleted {filename}"}


# Run with: uvicorn app:app --reload --host 0.0.0.0 --port 8000
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
