from typing import Generator
from openai import OpenAI
from backend.config import LLM_BASE_URL, LLM_API_KEY, MODEL_NAME, PROVIDER, KEEP_ALIVE
from backend.prompts import SYSTEM_PROMPT, generate_prompt
from backend.extractor import extract_text

client = OpenAI(base_url=LLM_BASE_URL, api_key=LLM_API_KEY)


def run_panic_stream(notes_file, notes_text: str, weak_topic: str, mode: str) -> Generator[str, None, None]:
    """
    Validates input, builds prompt, and streams token-by-token response from LLM engine.
    """
    context = extract_text(notes_file, notes_text)
    if not context.strip():
        yield "⚠️ **No study material provided!**\n\nPlease upload a PDF or paste notes in the input section on the left."
        return

    prompt = generate_prompt(mode, context, weak_topic)

    try:
        extra_args = {}
        if PROVIDER == "ollama":
            extra_args["extra_body"] = {"keep_alive": KEEP_ALIVE}

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            stream=True,
            **extra_args
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
            if PROVIDER == "ollama":
                yield (
                    f"❌ **Cannot connect to Ollama at `{LLM_BASE_URL}`**\n\n"
                    "👉 **If running locally:** Run `ollama serve` and `ollama pull llama3.2:3b`.\n\n"
                    "👉 **If running on Render / Cloud:** Set `GROQ_API_KEY` (free key at https://console.groq.com) or `OPENAI_API_KEY` in your Render Environment Variables."
                )
            else:
                yield f"❌ **Network Connection Error to {PROVIDER}:** `{err_msg}`"
        else:
            yield f"❌ **Inference Error ({PROVIDER} - {MODEL_NAME}):**\n\n`{err_msg}`"
