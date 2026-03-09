# src/generator.py
# ---------------------------------------------------------------
# Hauptlogik:
# 1. GPT-4 generiert einen optimierten DALL-E Prompt aus dem Blog-Titel
# 2. DALL-E 3 generiert das Bild
# 3. Bild wird lokal gespeichert
# ---------------------------------------------------------------

import os
import re
import time
import requests
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
from src.config import STYLE_ANCHOR, IMAGE_SIZE, IMAGE_QUALITY, OUTPUT_DIR

# API Key aus .env laden
load_dotenv()

# OpenAI Client initialisieren
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def sanitize_filename(title: str) -> str:
    """
    Konvertiert einen Blog-Titel in einen sicheren Dateinamen.
    z.B. "Interview mit Dr. Liza Ball" → "interview_mit_dr_liza_ball"
    """
    # Umlaute ersetzen
    replacements = {"ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss"}
    for char, replacement in replacements.items():
        title = title.lower().replace(char, replacement)
    # Alle Nicht-Alphanumerischen Zeichen durch Underscore ersetzen
    return re.sub(r"[^a-z0-9]+", "_", title).strip("_")[:60]


def build_dalle_prompt(blog_title: str) -> str:
    """
    Nutzt GPT-4 um aus einem Blog-Titel einen optimierten DALL-E Prompt zu generieren.
    GPT-4 versteht den Kontext des Titels und erstellt eine visuelle Beschreibung,
    die dann mit dem Style Anchor kombiniert wird.
    """
    system_prompt = (
        "You are an expert visual designer for a women's health app about endometriosis. "
        "Given a German blog post title, create a SHORT (max 2 sentences) visual scene description.\n\n"
        "IMPORTANT - match the image to the topic:\n"
        "- Rehabilitation / Reha / Hospital stay → calm hospital room, packed bag, cozy recovery setting, "
        "warm sunlight through window, comfortable bed with soft blankets\n"
        "- Nutrition / Ernährung / Food → fresh vegetables, colorful anti-inflammatory foods, "
        "herbs, olive oil, wholesome ingredients\n"
        "- Research / Forschung / Interview → microscope, laboratory glassware, scientific papers, "
        "DNA strands, petri dishes in soft light\n"
        "- Mental health / Psyche → serene nature scene, calm water, soft morning light, "
        "mindfulness, breathing space\n"
        "- Early detection / Früherkennung → medical examination, ultrasound imagery abstracted, "
        "gentle clinical setting\n"
        "- General endometriosis → abstract cell motifs, organic botanical shapes, soft anatomy\n\n"
        "Write in English. Output ONLY the visual description, nothing else."
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Blog title: {blog_title}"},
        ],
        max_tokens=120,
        temperature=0.7,
    )

    # Die visuelle Beschreibung aus GPT-4s Antwort extrahieren
    visual_description = response.choices[0].message.content.strip()

    # Visuelle Beschreibung + Style Anchor kombinieren → finaler DALL-E Prompt
    full_prompt = f"{visual_description} {STYLE_ANCHOR}"

    print(f"  📝 Prompt: {full_prompt[:100]}...")
    return full_prompt


def generate_and_save_image(blog_title: str, index: int) -> str:
    """
    Generiert ein Header-Bild für einen Blog-Titel und speichert es lokal.

    Args:
        blog_title: Der Blog-Titel als Text
        index: Laufende Nummer (für Dateiname)

    Returns:
        Pfad zur gespeicherten Bilddatei
    """
    print(f"\n🎨 Generiere Bild {index + 1}/10: '{blog_title[:50]}...'")

    # Schritt 1: GPT-4 generiert optimierten Prompt
    prompt = build_dalle_prompt(blog_title)

    # Schritt 2: DALL-E 3 generiert das Bild
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size=IMAGE_SIZE,       # 1792x1024 = perfektes Header-Format
        quality=IMAGE_QUALITY, # "hd" für beste Qualität
        n=1,                   # 1 Bild pro Aufruf (DALL-E 3 Limit)
        style="natural",       # "natural" für professionellere, weniger dramatische Bilder
    )

    # Bild-URL aus der Antwort extrahieren
    image_url = response.data[0].url

    # Schritt 3: Bild von URL herunterladen
    image_data = requests.get(image_url, timeout=30).content

    # Schritt 4: Bild lokal speichern
    Path(OUTPUT_DIR).mkdir(exist_ok=True)
    filename = f"{index + 1:02d}_{sanitize_filename(blog_title)}.png"
    filepath = os.path.join(OUTPUT_DIR, filename)

    with open(filepath, "wb") as f:
        f.write(image_data)

    print(f"  ✅ Gespeichert: {filepath}")
    return filepath


def generate_all_headers(titles: list, progress_callback=None) -> list:
    """
    Generiert Header-Bilder für alle Blog-Titel.

    Args:
        titles: Liste der Blog-Titel
        progress_callback: Optionale Callback-Funktion für Streamlit Progress Bar

    Returns:
        Liste der Dateipfade zu den generierten Bildern
    """
    saved_paths = []

    for i, title in enumerate(titles):
        path = generate_and_save_image(title, i)
        saved_paths.append(path)

        # Fortschritt an UI zurückgeben (für Streamlit)
        if progress_callback:
            progress_callback(i + 1, len(titles), title)

        # Rate-Limiting: DALL-E 3 erlaubt ~5 Bilder/Minute im Standard-Tier
        # Kurze Pause zwischen Anfragen, um API-Limits zu respektieren
        if i < len(titles) - 1:
            print("  ⏳ Warte 15 Sekunden (Rate-Limiting)...")
            time.sleep(15)

    return saved_paths