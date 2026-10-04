import os
from dotenv import load_dotenv

load_dotenv()

# Server Settings (Render automatically provides PORT)
HOST = os.getenv("HOST", "0.0.0.0")
DEFAULT_PORT = int(os.getenv("PORT", 7860))

# Provider Detection
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()

if GROQ_API_KEY:
    PROVIDER = "groq"
    LLM_BASE_URL = "https://api.groq.com/openai/v1"
    LLM_API_KEY = GROQ_API_KEY
    MODEL_NAME = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
elif OPENAI_API_KEY:
    PROVIDER = "openai"
    LLM_BASE_URL = "https://api.openai.com/v1"
    LLM_API_KEY = OPENAI_API_KEY
    MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
else:
    PROVIDER = "ollama"
    LLM_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
    LLM_API_KEY = "ollama"
    MODEL_NAME = os.getenv("OLLAMA_MODEL", "llama3.2:3b")

OLLAMA_API_BASE = os.getenv("OLLAMA_API_BASE", "http://localhost:11434")
KEEP_ALIVE = os.getenv("OLLAMA_KEEP_ALIVE", "24h")

# Context Limits
MAX_PDF_PAGES = int(os.getenv("MAX_PDF_PAGES", 15))
MAX_CONTEXT_CHARS = int(os.getenv("MAX_CONTEXT_CHARS", 8000))
