import os
import io
import socket
import threading
import uvicorn
from typing import Generator
from fastapi import FastAPI, UploadFile, File, Request, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from pypdf import PdfReader
from openai import OpenAI
from contextlib import asynccontextmanager

from backend.config import (
    HOST, DEFAULT_PORT, OLLAMA_BASE_URL, OLLAMA_MODEL, KEEP_ALIVE, MAX_PDF_PAGES, MAX_CONTEXT_CHARS
)
from backend.model_cache import preload_model_into_cache, get_cache_status
from backend.prompts import SYSTEM_PROMPT, generate_prompt


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Preloads the model weights into RAM/VRAM cache on server boot."""
    print(f"🔥 Warming up Ollama model ({OLLAMA_MODEL}) into cache...")
    threading.Thread(target=preload_model_into_cache, daemon=True).start()
    yield


# Initialize FastAPI App with Lifespan
app = FastAPI(title="Panic2Pass API", description="Emergency Pre-Exam AI Rescue Engine", lifespan=lifespan)

# Mount Static Files & Templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Initialize OpenAI-compatible Ollama client
client = OpenAI(base_url=OLLAMA_BASE_URL, api_key="ollama")


class RescueRequest(BaseModel):
    context: str
    weak_topic: str = ""
    mode: str = "⚡ 30-Min Crash Plan"


@app.get("/", response_class=HTMLResponse)
async def serve_landing_page(request: Request):
    """Serves the full-page Lando-styled landing page."""
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/api/status")
async def api_status():
    """Returns the current cache & health status of the Ollama model."""
    status = get_cache_status()
    return JSONResponse(content=status)


@app.post("/api/parse-pdf")
async def parse_pdf(file: UploadFile = File(...)):
    """Extracts text from uploaded PDF syllabus or lecture slides."""
    try:
        contents = await file.read()
        reader = PdfReader(io.BytesIO(contents))
        pages_to_read = min(len(reader.pages), MAX_PDF_PAGES)

        extracted_text = ""
        for i in range(pages_to_read):
            page_text = reader.pages[i].extract_text()
            if page_text:
                extracted_text += f"[Page {i + 1}]\n" + page_text.strip() + "\n\n"

        if not extracted_text.strip():
            return JSONResponse(content={"success": False, "error": "No readable text found in PDF."})

        cleaned = extracted_text[:MAX_CONTEXT_CHARS]
        return JSONResponse(content={
            "success": True,
            "pages": pages_to_read,
            "char_count": len(cleaned),
            "text": cleaned
        })
    except Exception as e:
        return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)


@app.post("/api/stream-rescue")
async def stream_rescue(payload: RescueRequest):
    """Streams the emergency rescue plan directly from Ollama."""
    if not payload.context.strip():
        raise HTTPException(status_code=400, detail="Study material context is empty.")

    prompt = generate_prompt(payload.mode, payload.context, payload.weak_topic)

    def event_generator() -> Generator[str, None, None]:
        try:
            response = client.chat.completions.create(
                model=OLLAMA_MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                stream=True,
                extra_body={"keep_alive": KEEP_ALIVE}
            )

            for chunk in response:
                if chunk.choices and len(chunk.choices) > 0:
                    delta = chunk.choices[0].delta.content or ""
                    if delta:
                        yield delta

        except Exception as e:
            yield f"\n\n❌ **Error streaming from Ollama:** `{str(e)}`"

    return StreamingResponse(event_generator(), media_type="text/plain; charset=utf-8")


def find_free_port(start_port: int = DEFAULT_PORT, max_attempts: int = 20) -> int:
    """Finds the first available TCP port to avoid binding conflicts."""
    for port in range(start_port, start_port + max_attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(("127.0.0.1", port)) != 0:
                return port
    return start_port


if __name__ == "__main__":
    port = find_free_port(DEFAULT_PORT)
    print(f"🚀 Launching Panic2Pass on http://localhost:{port}")
    uvicorn.run("app:app", host=HOST, port=port, reload=False)