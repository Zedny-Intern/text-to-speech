import os
import uuid
from datetime import datetime

def ensure_dir(directory):
    """Create directory if it doesn't exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory

def generate_filename(prefix="audio", extension="mp3"):
    """Generate unique filename with timestamp."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    return f"{prefix}_{timestamp}_{unique_id}.{extension}"

def save_text_file(text, directory, filename=None):
    """Save text to file."""
    ensure_dir(directory)
    if filename is None:
        filename = generate_filename("text", "txt")
    filepath = os.path.join(directory, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)
    return filepath

def list_audio_files(directory):
    """List all audio files in directory."""
    ensure_dir(directory)
    files = []
    for f in os.listdir(directory):
        if f.endswith(('.mp3', '.wav')):
            filepath = os.path.join(directory, f)
            files.append({
                "filename": f,
                "path": filepath,
                "size": os.path.getsize(filepath),
                "created": os.path.getctime(filepath)
            })
    return sorted(files, key=lambda x: x["created"], reverse=True)

def delete_file(filepath):
    """Delete a file if it exists."""
    if os.path.exists(filepath):
        os.remove(filepath)
        return True
    return False

def cleanup_temp_files(directory, pattern="temp_"):
    """Remove temporary files."""
    if not os.path.exists(directory):
        return
    for f in os.listdir(directory):
        if f.startswith(pattern):
            delete_file(os.path.join(directory, f))
