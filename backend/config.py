# TTS Configuration

# Voice mappings for Edge-TTS
VOICES = {
    "ar": {
        "male": "ar-EG-ShakirNeural",
        "female": "ar-EG-SalmaNeural"
    },
    "en": {
        "male": "en-US-GuyNeural",
        "female": "en-US-JennyNeural"
    }
}

# Default settings
DEFAULT_LANGUAGE = "auto"
DEFAULT_GENDER = "female"
DEFAULT_RATE = "+0%"
DEFAULT_VOLUME = "+0%"

# Audio output settings
AUDIO_OUTPUT_DIR = "audio_outputs"
AUDIO_FORMAT = "mp3"

# Text limits
MAX_TEXT_LENGTH = 10000
MAX_SENTENCE_LENGTH = 500
