import os
import requests

API_URL = os.environ.get('SUMMARY_API_URL')  # Placeholder for AI API endpoint
API_KEY = os.environ.get('SUMMARY_API_KEY')


def summarize_text(text: str) -> str:
    """Send text to an external API to produce a structured summary."""
    if not API_URL or not API_KEY:
        # Placeholder summary when API info is missing
        return "\n".join([
            "# Abstract",
            text[:200] + '...',
            "\n# Introduction",
            text[200:400] + '...',
            "\n# Results",
            text[400:600] + '...',
            "\n# Discussion",
            text[600:800] + '...'
        ])

    headers = {"Authorization": f"Bearer {API_KEY}"}
    payload = {"text": text}
    resp = requests.post(API_URL, json=payload, headers=headers, timeout=30)
    resp.raise_for_status()
    return resp.json().get('summary', '')
