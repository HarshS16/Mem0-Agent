import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

WHISPER_MODEL = "whisper-large-v3-turbo"
LLM_MODEL = "llama-3.3-70b-versatile"

# Ensure output directory exists for safety constraint
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

SUPPORTED_AUDIO_FORMATS = ["wav", "mp3", "ogg", "m4a", "flac"]
