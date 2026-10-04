from pypdf import PdfReader
from backend.config import MAX_PDF_PAGES, MAX_CONTEXT_CHARS


def extract_text(file_obj, manual_notes: str) -> str:
    """
    Extracts text from uploaded PDF with a page limit and falls back to manual notes.
    Caps character length to prevent context overflow.
    """
    extracted = ""
    if file_obj is not None:
        try:
            reader = PdfReader(file_obj.name)
            pages_to_read = min(len(reader.pages), MAX_PDF_PAGES)
            for idx in range(pages_to_read):
                page = reader.pages[idx]
                page_text = page.extract_text()
                if page_text:
                    extracted += f"[Page {idx + 1}]\n" + page_text.strip() + "\n\n"
        except Exception:
            extracted = ""

    if not extracted.strip():
        extracted = manual_notes.strip() if manual_notes else ""

    return extracted[:MAX_CONTEXT_CHARS]
