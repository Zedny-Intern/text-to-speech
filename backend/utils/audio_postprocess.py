import os
from pydub import AudioSegment

def concatenate_audio_files(audio_files, output_path):
    """Merge multiple audio files into one."""
    if not audio_files:
        return None
    
    combined = AudioSegment.empty()
    
    for audio_file in audio_files:
        if os.path.exists(audio_file):
            segment = AudioSegment.from_mp3(audio_file)
            combined += segment
            # Add small silence between segments
            combined += AudioSegment.silent(duration=200)
    
    # Export combined audio
    combined.export(output_path, format="mp3")
    return output_path

def normalize_audio(input_path, output_path, target_dBFS=-20.0):
    """Normalize audio volume."""
    audio = AudioSegment.from_mp3(input_path)
    change_in_dBFS = target_dBFS - audio.dBFS
    normalized = audio.apply_gain(change_in_dBFS)
    normalized.export(output_path, format="mp3")
    return output_path

def convert_to_wav(input_path, output_path):
    """Convert MP3 to WAV."""
    audio = AudioSegment.from_mp3(input_path)
    audio.export(output_path, format="wav")
    return output_path
