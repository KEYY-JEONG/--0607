import os
import re
import requests

API_URL = os.environ.get('SUMMARY_API_URL')
API_KEY = os.environ.get('SUMMARY_API_KEY')


def summarize_text(text: str) -> str:
    """Create a structured summary of the provided text.

    If API credentials are configured, send the text to the external API.
    Otherwise fallback to a simple local summarization based on sentence
    extraction.
    """
    if not API_URL or not API_KEY:
        sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if s.strip()]
        parts = {
            "Abstract": sentences[:3],
            "Introduction": sentences[3:8],
            "Results": sentences[8:13],
            "Discussion": sentences[13:18],
        }

        lines = []
        for title, seg in parts.items():
            lines.append(f"# {title}")
            lines.append(" ".join(seg) if seg else "N/A")
            lines.append("")
        return "\n".join(lines).strip()

    headers = {"Authorization": f"Bearer {API_KEY}"}
    payload = {"text": text}
    resp = requests.post(API_URL, json=payload, headers=headers, timeout=30)
    resp.raise_for_status()
    return resp.json().get('summary', '')
