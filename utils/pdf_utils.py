from io import StringIO

try:
    from pdfminer.high_level import extract_text
except ImportError:  # pragma: no cover - pdfminer.six may not be installed
    extract_text = None


def extract_text_from_pdf(path: str) -> str:
    """Extract text from a PDF file using pdfminer.six."""
    if extract_text is None:
        raise RuntimeError(
            "pdfminer.six is required for PDF text extraction but is not installed."
        )

    try:
        text = extract_text(path)
        return text
    except Exception as e:
        return f"Error extracting text: {e}"
