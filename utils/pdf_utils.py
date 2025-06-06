from io import StringIO
from pdfminer.high_level import extract_text


def extract_text_from_pdf(path: str) -> str:
    """Extract text from a PDF file using pdfminer.six."""
    try:
        text = extract_text(path)
        return text
    except Exception as e:
        return f"Error extracting text: {e}"
