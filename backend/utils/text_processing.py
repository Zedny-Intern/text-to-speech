import re

def normalize_text(text):
    """Clean and normalize input text."""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text.strip())
    # Remove unsupported characters but keep Arabic, English, numbers, punctuation
    text = re.sub(r'[^\u0600-\u06FF\u0750-\u077Fa-zA-Z0-9\s.,!?;:\'\"-،؛؟]', '', text)
    return text

def segment_sentences(text):
    """Split text into sentences."""
    # Split on common sentence endings (English and Arabic)
    pattern = r'(?<=[.!?،؛؟])\s+'
    sentences = re.split(pattern, text)
    # Filter empty sentences and strip whitespace
    sentences = [s.strip() for s in sentences if s.strip()]
    return sentences

def chunk_long_sentence(sentence, max_length=500):
    """Break long sentences into smaller chunks."""
    if len(sentence) <= max_length:
        return [sentence]
    
    chunks = []
    words = sentence.split()
    current_chunk = []
    current_length = 0
    
    for word in words:
        if current_length + len(word) + 1 > max_length:
            if current_chunk:
                chunks.append(' '.join(current_chunk))
            current_chunk = [word]
            current_length = len(word)
        else:
            current_chunk.append(word)
            current_length += len(word) + 1
    
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks

def prepare_text(text, max_sentence_length=500):
    """Full text preprocessing pipeline."""
    text = normalize_text(text)
    sentences = segment_sentences(text)
    
    result = []
    for sentence in sentences:
        chunks = chunk_long_sentence(sentence, max_sentence_length)
        result.extend(chunks)
    
    return result
