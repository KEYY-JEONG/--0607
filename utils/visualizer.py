import os

try:
    import requests  # Needed for external API calls
except ImportError:  # pragma: no cover - requests may not be installed
    requests = None

VISUAL_API_URL = os.environ.get('VISUAL_API_URL')  # Placeholder for image generation endpoint
VISUAL_API_KEY = os.environ.get('VISUAL_API_KEY')


def generate_visual(summary: str, output_path: str) -> None:
    """Generate a visualization image from summary text via external API."""
    if not VISUAL_API_URL or not VISUAL_API_KEY:
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

    headers = {"Authorization": f"Bearer {VISUAL_API_KEY}"}
    payload = {"prompt": summary}
    resp = requests.post(VISUAL_API_URL, json=payload, headers=headers, timeout=30)
    resp.raise_for_status()
    with open(output_path, 'wb') as f:
        f.write(resp.content)
