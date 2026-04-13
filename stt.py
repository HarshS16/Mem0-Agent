import os
from groq import Groq
from config import GROQ_API_KEY, WHISPER_MODEL

def get_client():
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is not set.")
    return Groq(api_key=GROQ_API_KEY)

def transcribe_audio(audio_bytes: bytes, filename: str = "audio.wav") -> str:
    """Send audio to Groq Whisper and return transcription text."""
    try:
        client = get_client()
        # Groq expects a tuple for the file upload (filename, file_content)
        completion = client.audio.transcriptions.create(
            file=(filename, audio_bytes),
            model=WHISPER_MODEL,
        )
        return completion.text
    except Exception as e:
        return f"Error transcribing audio: {e}"
