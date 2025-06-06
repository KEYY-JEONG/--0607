import os

try:
    import requests  # Needed for external API calls
except ImportError:  # pragma: no cover - requests may not be installed
    requests = None


def generate_visual(summary: str, output_path: str) -> None:
    """Generate a visualization image from summary text via external API."""
    anthropic_key = os.getenv('ANTHROPIC_API_KEY')
    gemini_key = os.getenv('GEMINI_API_KEY')

    if not anthropic_key and not gemini_key:
        # If API config missing, create a placeholder image
        try:
            from PIL import Image, ImageDraw
        except ImportError as e:
            raise RuntimeError(
                "Pillow is required to generate placeholder images but is not installed"
            ) from e

        img = Image.new('RGB', (800, 400), color=(73, 109, 137))
        d = ImageDraw.Draw(img)
        d.text((10, 10), 'Visualization Placeholder', fill=(255, 255, 0))
        img.save(output_path)
        return

    if requests is None:
        raise RuntimeError(
            "The requests package is required for API visualization but is not installed."
        )

    headers = {
        "Content-Type": "application/json",
    }
    if anthropic_key:
        headers["x-api-key"] = anthropic_key
        payload = {"prompt": summary}
        resp = requests.post(
            "https://api.anthropic.com/v1/visualize",
            json=payload,
            headers=headers,
            timeout=30,
        )
    else:
        headers["Authorization"] = f"Bearer {gemini_key}"
        payload = {"prompt": summary}
        resp = requests.post(
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-turbo:generateImage",
            json=payload,
            headers=headers,
            timeout=30,
        )
    resp.raise_for_status()
    with open(output_path, "wb") as f:
        f.write(resp.content)
