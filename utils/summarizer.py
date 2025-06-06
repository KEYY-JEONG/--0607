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
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())
        abstract = " ".join(sentences[:3])
        introduction = " ".join(sentences[3:8])
        results = " ".join(sentences[8:13])
        discussion = " ".join(sentences[13:18])
        return "\n".join([
            "# Abstract",
            abstract,
            "",
            "# Introduction",
            introduction,
            "",
            "# Results",
            results,
            "",
            "# Discussion",
            discussion,
        ])

    headers = {"Authorization": f"Bearer {API_KEY}"}
    payload = {"text": text}
    resp = requests.post(API_URL, json=payload, headers=headers, timeout=30)
    resp.raise_for_status()
    return resp.json().get('summary', '')
