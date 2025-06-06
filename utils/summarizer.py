import os
import re

try:
    import requests  # Only needed when using the external API
except ImportError:  # pragma: no cover - requests may not be installed
    requests = None


def summarize_text(text: str) -> str:
    """Create a structured summary of the provided text.

    If API credentials are configured, send the text to the external API.
    Otherwise fallback to a simple local summarization based on sentence
    extraction.
    """
    api_key = os.getenv('OPENAI_API_KEY')

    if not api_key:
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

    if requests is None:
        raise RuntimeError(
            "The requests package is required for API summarization but is not installed."
        )

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    prompt = (
        "Summarize the following text into the sections: "
        "Abstract, Introduction, Results, Discussion."
        " Provide the response in Markdown format.\n\n" + text
    )
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
    }
    resp = requests.post(
        "https://api.openai.com/v1/chat/completions",
        json=data,
        headers=headers,
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"].strip()
