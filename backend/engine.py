from typing import Generator
from openai import OpenAI
from backend.config import OLLAMA_BASE_URL, OLLAMA_MODEL, KEEP_ALIVE
from backend.prompts import SYSTEM_PROMPT, generate_prompt
from backend.extractor import extract_text

client = OpenAI(base_url=OLLAMA_BASE_URL, api_key="ollama")


def run_panic_stream(notes_file, notes_text: str, weak_topic: str, mode: str) -> Generator[str, None, None]:
    """
    Validates input, builds prompt, and streams token-by-token response from Ollama.
    """
    context = extract_text(notes_file, notes_text)
    if not context.strip():
        yield "⚠️ **No study material provided!**\n\nPlease upload a PDF or paste notes in the input section on the left."
        return

    prompt = generate_prompt(mode, context, weak_topic)

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

        accumulated = ""
        for chunk in response:
            if chunk.choices and len(chunk.choices) > 0:
                delta = chunk.choices[0].delta.content or ""
                accumulated += delta
                yield accumulated

    except Exception as e:
        err_msg = str(e)
        if "Connection refused" in err_msg or "Failed to connect" in err_msg:
            yield (
                f"❌ **Cannot connect to Ollama at `{OLLAMA_BASE_URL}`**\n\n"
                "**Troubleshooting Checklist:**\n"
                "1. Make sure Ollama is active (`ollama serve`).\n"
                f"2. Ensure model is pulled: `ollama pull {OLLAMA_MODEL}`.\n"
                "3. If deployed on Render/Cloud, set `OLLAMA_BASE_URL` to your remote Ollama endpoint."
            )
        else:
            yield f"❌ **Ollama Inference Error:**\n\n`{err_msg}`"
