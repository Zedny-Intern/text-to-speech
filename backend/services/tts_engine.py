import edge_tts
import asyncio
import os
import uuid
from config import VOICES, AUDIO_OUTPUT_DIR, DEFAULT_RATE, DEFAULT_VOLUME
from utils.file_manager import ensure_dir

async def synthesize_text(text, language="en", gender="female", rate=DEFAULT_RATE, volume=DEFAULT_VOLUME):
    """
    Synthesize text to speech using Edge-TTS.
    Returns path to generated audio file.
    """
    # Get voice based on language and gender
    voice = VOICES.get(language, VOICES["en"]).get(gender, "female")
    
    # Generate unique filename
    output_dir = ensure_dir(AUDIO_OUTPUT_DIR)
    filename = f"tts_{uuid.uuid4().hex[:8]}.mp3"
    output_path = os.path.join(output_dir, filename)
    
    # Create TTS communicate object
    communicate = edge_tts.Communicate(text, voice, rate=rate, volume=volume)
    
    # Save audio
    await communicate.save(output_path)
    
    return output_path, filename

async def synthesize_sentences(sentences_with_lang, gender="female"):
    """
    Synthesize multiple sentences, each with its detected language.
    Returns list of audio file paths.
    """
    audio_files = []
    
    for sentence, language in sentences_with_lang:
        if sentence.strip():
            path, filename = await synthesize_text(sentence, language, gender)
            audio_files.append(path)
    
    return audio_files

async def get_available_voices():
    """Get list of available Edge-TTS voices."""
    voices = await edge_tts.list_voices()
    # Filter for Arabic and English voices
    filtered = [v for v in voices if v["Locale"].startswith(("ar", "en"))]
    return filtered

def get_configured_voices():
    """Get the configured voice options."""
    return {
        "arabic": {
            "male": VOICES["ar"]["male"],
            "female": VOICES["ar"]["female"]
        },
        "english": {
            "male": VOICES["en"]["male"],
            "female": VOICES["en"]["female"]
        }
    }

# Synchronous wrapper for async functions
def run_synthesis(text, language="en", gender="female"):
    """Synchronous wrapper for synthesize_text."""
    return asyncio.run(synthesize_text(text, language, gender))

def run_batch_synthesis(sentences_with_lang, gender="female"):
    """Synchronous wrapper for synthesize_sentences."""
    return asyncio.run(synthesize_sentences(sentences_with_lang, gender))
