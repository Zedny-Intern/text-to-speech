import re
from langdetect import detect, LangDetectException

def is_arabic(text):
    """Check if text contains Arabic characters."""
    arabic_pattern = re.compile(r'[\u0600-\u06FF\u0750-\u077F]')
    return bool(arabic_pattern.search(text))

def is_english(text):
    """Check if text contains English characters."""
    english_pattern = re.compile(r'[a-zA-Z]')
    return bool(english_pattern.search(text))

def detect_language(text):
    """
    Detect the primary language of text.
    Returns: 'ar', 'en', or 'mixed'
    """
    has_arabic = is_arabic(text)
    has_english = is_english(text)
    
    if has_arabic and has_english:
        # Mixed language - determine dominant
        arabic_chars = len(re.findall(r'[\u0600-\u06FF\u0750-\u077F]', text))
        english_chars = len(re.findall(r'[a-zA-Z]', text))
        
        if arabic_chars > english_chars:
            return 'ar'
        else:
            return 'en'
    elif has_arabic:
        return 'ar'
    elif has_english:
        return 'en'
    else:
        # Fallback to langdetect
        try:
            lang = detect(text)
            return 'ar' if lang == 'ar' else 'en'
        except LangDetectException:
            return 'en'

def detect_per_sentence(sentences):
    """Detect language for each sentence."""
    return [(sentence, detect_language(sentence)) for sentence in sentences]
