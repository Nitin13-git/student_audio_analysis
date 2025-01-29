import os
import tempfile
import openai


def transcribe_audio_with_openai(audio_file_path):
    """Transcribe audio using OpenAI's Whisper model."""
    temp_file_path = None  
    try:
        with open(audio_file_path, "rb") as audio_file:
            transcription = openai.Audio.transcribe(
                model="whisper-1",
                file=audio_file,
                response_format="verbose_json",
                language="en"
            )
        
        return transcription["text"]
    
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        return None

