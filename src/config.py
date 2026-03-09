# src/config.py
# ---------------------------------------------------------------
# Brand Identity Konfiguration für endometriose.app / Endo-App
# Blog-Titel werden automatisch von der Website gescrapt.
# ---------------------------------------------------------------

import requests
from bs4 import BeautifulSoup

# URL des Blogs
BLOG_URL = "https://endometriose.app/aktuelles-2/"


def fetch_blog_titles(limit: int = 10) -> list:
    """
    Scrapt automatisch die aktuellen Blog-Titel von der Website.
    Kein Hardcoding – immer up-to-date!

    Args:
        limit: Maximale Anzahl an Titeln (Standard: 10)

    Returns:
        Liste der Blog-Titel als Strings
    """
    response = requests.get(BLOG_URL, timeout=10)
    response.raise_for_status()  # Fehler bei schlechtem HTTP-Status

    soup = BeautifulSoup(response.text, "html.parser")

    # Blog-Titel aus den h2/h3 Tags extrahieren
    # Die Endo-App nutzt WordPress → Standard entry-title Klassen
    selectors = ["h2.entry-title", "h3.entry-title", "h2.wp-block-post-title", ".post-title"]
    titles = []

    for selector in selectors:
        found = [el.get_text(strip=True) for el in soup.select(selector)]
        if found:
            titles = found
            break  # Ersten funktionierenden Selector nehmen

    if not titles:
        raise ValueError(f"Keine Blog-Titel auf {BLOG_URL} gefunden. Bitte Selector prüfen.")

    print(f"✅ {len(titles)} Blog-Titel von Website gescrapt.")
    return titles[:limit]


# ---------------------------------------------------------------
# STYLE ANCHOR: Dieser Text wird an JEDEN DALL-E Prompt gehängt.
# Er definiert Farben, Stil, Stimmung und visuelle Sprache der Brand.
# Änderungen hier wirken sich auf ALLE Bilder aus → Konsistenz!
# ---------------------------------------------------------------
STYLE_ANCHOR = (
    "Soft minimalist medical illustration style. "
    "Color palette: muted rose (#E8A598), warm lavender (#C3B1E1), "
    "soft sage green (#A8C5A0), and clean white backgrounds. "
    "Abstract, hopeful, and empowering aesthetic. "
    "No text or typography in the image. "
    "Gentle gradients, organic shapes, subtle cell or botanical motifs. "
    "Professional health-app brand identity. "
    "16:9 widescreen header format. "
    "Photorealistic yet artistic, soft-focus photography style. "
    "Warm, trustworthy, and scientifically modern mood."
)

# Bildgröße: DALL-E 3 unterstützt 1792x1024 für Querformat
IMAGE_SIZE = "1792x1024"

# Qualität: "standard" zum Testen, "hd" für finale Version
IMAGE_QUALITY = "standard"

# Ausgabe-Verzeichnis
OUTPUT_DIR = "output"