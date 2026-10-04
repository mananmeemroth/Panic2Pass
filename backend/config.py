import os
from dotenv import load_dotenv

load_dotenv()

# Server Settings (Render dynamically sets PORT)
HOST = os.getenv("HOST", "0.0.0.0")
DEFAULT_PORT = int(os.getenv("PORT", 7860))

# Ollama Engine Settings
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
OLLAMA_API_BASE = os.getenv("OLLAMA_API_BASE", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
KEEP_ALIVE = os.getenv("OLLAMA_KEEP_ALIVE", "24h")

# Context Limits
MAX_PDF_PAGES = int(os.getenv("MAX_PDF_PAGES", 15))
MAX_CONTEXT_CHARS = int(os.getenv("MAX_CONTEXT_CHARS", 8000))
