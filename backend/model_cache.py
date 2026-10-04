import json
import urllib.request
import urllib.error
import threading
from typing import Tuple, Dict, Any
from backend.config import OLLAMA_API_BASE, OLLAMA_MODEL, KEEP_ALIVE

_CACHE_STATUS = {
    "is_cached": False,
    "model": OLLAMA_MODEL,
    "message": "Initializing...",
    "error": None
}
_lock = threading.Lock()


def check_ollama_health() -> Tuple[bool, str]:
    """
    Checks if Ollama server is reachable.
    """
    try:
        req = urllib.request.Request(f"{OLLAMA_API_BASE}/api/tags", method="GET")
        with urllib.request.urlopen(req, timeout=3) as resp:
            if resp.status == 200:
                data = json.loads(resp.read().decode("utf-8"))
                models = [m.get("name", "") for m in data.get("models", [])]
                model_base = OLLAMA_MODEL.split(":")[0]
                matched = any(OLLAMA_MODEL in m or model_base in m for m in models)
                if matched:
                    return True, f"Ollama is running with model '{OLLAMA_MODEL}'."
                else:
                    return False, f"Ollama is running, but model '{OLLAMA_MODEL}' is missing. Run `ollama pull {OLLAMA_MODEL}`."
            return False, f"Ollama returned HTTP status {resp.status}."
    except urllib.error.URLError as e:
        return False, f"Cannot connect to Ollama at {OLLAMA_API_BASE}: {e.reason}"
    except Exception as e:
        return False, f"Ollama check failed: {str(e)}"


def preload_model_into_cache() -> Dict[str, Any]:
    """
    Sends a warm-up request to Ollama with keep_alive parameter.
    This forces Ollama to load the model weights into memory/GPU cache immediately.
    """
    global _CACHE_STATUS
    is_healthy, health_msg = check_ollama_health()
    if not is_healthy:
        with _lock:
            _CACHE_STATUS["is_cached"] = False
            _CACHE_STATUS["error"] = health_msg
            _CACHE_STATUS["message"] = f"⚠️ {health_msg}"
        return _CACHE_STATUS

    try:
        payload = json.dumps({
            "model": OLLAMA_MODEL,
            "prompt": "",  # Empty prompt only loads the model into cache
            "keep_alive": KEEP_ALIVE
        }).encode("utf-8")

        req = urllib.request.Request(
            f"{OLLAMA_API_BASE}/api/generate",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            if resp.status == 200:
                with _lock:
                    _CACHE_STATUS["is_cached"] = True
                    _CACHE_STATUS["error"] = None
                    _CACHE_STATUS["message"] = f"🟢 Cached & Ready (`{OLLAMA_MODEL}` in VRAM/RAM)"
                return _CACHE_STATUS
    except Exception as e:
        with _lock:
            _CACHE_STATUS["is_cached"] = False
            _CACHE_STATUS["error"] = str(e)
            _CACHE_STATUS["message"] = f"⚠️ Warm-up failed: {str(e)}"

    return _CACHE_STATUS


def get_cache_status() -> Dict[str, Any]:
    """
    Returns current cache status without re-triggering warm-up unless uninitialized.
    """
    global _CACHE_STATUS
    with _lock:
        if not _CACHE_STATUS["is_cached"] and _CACHE_STATUS["error"] is None:
            # Trigger in background
            threading.Thread(target=preload_model_into_cache, daemon=True).start()
        return dict(_CACHE_STATUS)
