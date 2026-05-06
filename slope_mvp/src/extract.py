import sys

import fitz


def extract_text(path: str) -> str:
    """Extract text from PDF or plain text file."""
    if path.endswith(".pdf"):
        doc = fitz.open(path)
        text = "\n".join(page.get_text() for page in doc)
        doc.close()
    elif path.endswith((".txt", ".md")):
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        raise ValueError(f"Unsupported file type: {path}")

    # Collapse excessive whitespace
    lines = [line.strip() for line in text.splitlines()]
    text = "\n".join(line for line in lines if line)

    if len(text) > 150_000:
        print(f"[extract] Warning: truncating from {len(text)} to 150000 chars", file=sys.stderr)
        text = text[:150_000]

    return text
