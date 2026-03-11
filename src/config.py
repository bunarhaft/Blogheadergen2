
# src/config.py
import requests
from bs4 import BeautifulSoup

BLOG_URL = "https://endometriose.app/aktuelles-2/"

# Nur URLs mit diesen Pfad-Segmenten sind echte Blog-Posts
BLOG_URL_KEYWORDS = [
    "/impulse/",
    "/wissen-und-tipps/",
    "/erfahrungsberichte/",
    "/ernaehrung/",
    "/forschung/",
    "/studien/",
    "/experten-interviews/",
]


def fetch_blog_titles(limit: int = 10) -> list:
    """
    Scrapt Blog-Titel von der Endo-App Website.
    Filtert anhand der URL-Struktur nur echte Blog-Posts heraus
    (keine App-Seiten, Downloads, etc.)
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    response = requests.get(BLOG_URL, headers=headers, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    titles = []
    # Alle slide-entry-title Links durchgehen
    for el in soup.select("h3.slide-entry-title a"):
        href = el.get("href", "")
        title = el.get_text(strip=True)

        # Nur URLs die einem Blog-Kategorie-Pfad entsprechen
        if any(keyword in href for keyword in BLOG_URL_KEYWORDS):
            titles.append(title)

        if len(titles) >= limit:
            break

    if not titles:
        raise ValueError(f"Keine Blog-Titel gefunden auf {BLOG_URL}.")

    print(f"✅ {len(titles)} Blog-Titel gescrapt:")
    for i, t in enumerate(titles, 1):
        print(f"  {i}. {t}")

    return titles


# ---------------------------------------------------------------
# STYLE ANCHOR
# ---------------------------------------------------------------
STYLE_ANCHOR = (
    "soft sage green (#A8C5A0), and clean white backgrounds. "
    "Professional health-app brand identity. "
    "16:9 widescreen header format. "
    "Photorealistic yet artistic, soft-focus photography style. "
    "Warm, trustworthy, and scientifically modern mood."
)

IMAGE_SIZE = "1792x1024"
IMAGE_QUALITY = "standard"
OUTPUT_DIR = "output"