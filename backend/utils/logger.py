import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('tts_app.log', encoding='utf-8')
    ]
)

logger = logging.getLogger("TTS")

def log_synthesis(text, language, voice, duration=None):
    """Log TTS synthesis request."""
    logger.info(f"Synthesis: lang={language}, voice={voice}, len={len(text)}, duration={duration}ms")

def log_error(error_msg, details=None):
    """Log error with details."""
    logger.error(f"Error: {error_msg} | Details: {details}")

def log_request(endpoint, method, params=None):
    """Log API request."""
    logger.info(f"Request: {method} {endpoint} | Params: {params}")

def log_performance(operation, start_time):
    """Log operation timing."""
    duration = (datetime.now() - start_time).total_seconds() * 1000
    logger.info(f"Performance: {operation} took {duration:.2f}ms")
    return duration
