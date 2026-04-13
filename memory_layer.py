import os
import json
from config import OUTPUT_DIR

MEMORY_FILE = os.path.join(OUTPUT_DIR, "session_memory.json")

def _load_history():
    if not os.path.exists(MEMORY_FILE):
        return []
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def _save_history(history):
    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2)
    except Exception:
        pass

def record_user_message(text: str, user_id: str = "default_user"):
    """Saves memory to a persistent JSON store without relying on mem0 bindings which require separate Embedders."""
    history = _load_history()
    history.append({"user_id": user_id, "memory": text})
    _save_history(history)

def get_relevant_memories(query: str, user_id: str = "default_user") -> str:
    """Gets recent relevant interactions safely acting as a session memory layer."""
    history = _load_history()
    user_history = [item["memory"] for item in history if item.get("user_id") == user_id]
    
    if not user_history:
        return ""
    
    # Return last 5 interactions as immediate context to avoid context bloat
    recent = user_history[-5:]
    return "\n".join(recent)
