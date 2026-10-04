from typing import Generator
from openai import OpenAI
from backend.config import OLLAMA_BASE_URL, OLLAMA_MODEL, KEEP_ALIVE
from backend.prompts import SYSTEM_PROMPT, generate_prompt
from backend.extractor import extract_text

client = OpenAI(base_url=OLLAMA_BASE_URL, api_key="ollama")


def run_panic_stream(notes_file, notes_text: str, weak_topic: str, mode: str) -> Generator[str, None, None]:
    """
    Validates input, builds prompt, and streams token-by-token response from cached Ollama model.
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
                "❌ **Cannot connect to Ollama**\n\n"
                "- Verify that Ollama is active (`ollama serve`).\n"
                f"- Check that the model is downloaded (`ollama pull {OLLAMA_MODEL}`)."
            )
        else:
            yield f"❌ **Inference Error:**\n\n`{err_msg}`"
