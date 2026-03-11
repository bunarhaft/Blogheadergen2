# Systemarchitektur

## Übersicht

BlogHeaderGen2 ist nach dem **Pipeline-Muster** aufgebaut: Jede Stufe hat eine klar definierte Eingabe und Ausgabe. Die Trennung zwischen Konfiguration (`config.py`), Logik (`generator.py`) und Oberfläche (`app.py` / `main.py`) erlaubt unabhängige Weiterentwicklung.

---

## Komponentendiagramm

```
┌──────────────────────────────────────────────────────────────┐
│                        Einstiegspunkte                        │
│                                                               │
│   ┌────────────┐                    ┌─────────────────────┐   │
│   │  main.py   │                    │       app.py        │   │
│   │  (CLI)     │                    │  (Streamlit Web-UI) │   │
│   └─────┬──────┘                    └──────────┬──────────┘   │
└─────────┼─────────────────────────────────────┼──────────────┘
          │                                     │
          └──────────────┬──────────────────────┘
                         │
          ┌──────────────▼──────────────┐
          │         src/config.py        │
          │  - BLOG_URL                  │
          │  - STYLE_ANCHOR              │
          │  - IMAGE_SIZE / QUALITY      │
          │  - fetch_blog_titles()       │
          └──────────────┬──────────────┘
                         │  Blog-Titel (Liste von Strings)
          ┌──────────────▼──────────────┐
          │        src/generator.py      │
          │  - build_dalle_prompt()      │  ←── GPT-4o API
          │  - generate_and_save_image() │  ←── DALL-E 3 API
          │  - generate_all_headers()    │
          │  - sanitize_filename()       │
          └──────────────┬──────────────┘
                         │  PNG-Dateien
          ┌──────────────▼──────────────┐
          │         output/              │
          │  01_titel_des_posts.png      │
          │  02_anderer_titel.png        │
          │  ...                         │
          └─────────────────────────────┘
```

---

## Zweistufige KI-Pipeline

Das Herzstück der Anwendung ist die zweistufige KI-Pipeline in `generator.py`:

### Stufe 1: Prompt-Optimierung mit GPT-4o

```
Eingabe: Deutscher Blog-Titel (z.B. "Interview mit Dr. Liza Ball")
   ↓
GPT-4o System-Prompt:
  - Erkennt den thematischen Kontext (Ernährung, Forschung, Mental Health, ...)
  - Wählt passende visuelle Metaphern
  - Gibt max. 2 Sätze zurück
   ↓
Ausgabe: Visuelle Beschreibung (Englisch, für DALL-E optimiert)
```

**Thematisches Mapping (im System-Prompt definiert):**

| Blog-Thema | Visuelle Metapher |
|---|---|
| Rehabilitation | Krankenhauszimmer, Rucksack, Erholung |
| Ernährung | Frisches Gemüse, entzündungshemmende Lebensmittel |
| Forschung / Studien | Mikroskope, Laborgeräte, wissenschaftliche Grafiken |
| Mental Health | Naturszenen, ruhiges Wasser |
| Früherkennung | Medizinische Untersuchung, Ultraschall |
| Allgemein | Abstrakte Zellmotive, botanische Formen |

### Stufe 2: Bildgenerierung mit DALL-E 3

```
Eingabe: Visuelle Beschreibung (aus Stufe 1)
   +
STYLE_ANCHOR: Marken-Stilrichtlinie (aus config.py)
   ↓
DALL-E 3:
  - Model: dall-e-3
  - Size: 1792×1024 (16:9 Header-Format)
  - Quality: standard
  - Style: natural
   ↓
Ausgabe: PNG-Bild (URL → lokal gespeichert)
```

---

## Datenfluss im Detail

```
1. SCRAPING
   GET https://endometriose.app/aktuelles-2/
   BeautifulSoup → <h3 class="slide-entry-title">
   Filter: URL enthält /impulse/ | /wissen-und-tipps/ | /ernaehrung/ | ...
   Limit: 10 Einträge
        ↓
2. PROMPT-OPTIMIERUNG (pro Titel, sequenziell)
   GPT-4o API Call
   max_tokens=120, temperature=0.7
   Eingabe: Blog-Titel (DE)
   Ausgabe: Visuelle Beschreibung (EN, 2 Sätze)
        ↓
3. BILDGENERIERUNG (pro Titel, mit 15s Pause)
   DALL-E 3 API Call
   Prompt: [Visuelle Beschreibung] + [STYLE_ANCHOR]
   Ausgabe: URL zum temporären OpenAI-Bild
        ↓
4. DOWNLOAD & SPEICHERUNG
   HTTP GET auf Bild-URL
   Dateiname: sanitize_filename(titel) → z.B. "01_interview_dr_ball.png"
   Zielordner: output/
```

---

## Dateistruktur der generierten Bilder

```
output/
├── 01_erster_blog_titel.png        # Index immer zweistellig
├── 02_zweiter_blog_titel.png       # Umlauts: ä→ae, ö→oe, ü→ue, ß→ss
├── ...                              # Max. 60 Zeichen im Dateinamen
└── 10_zehnter_blog_titel.png
```

---

## Benutzeroberflächen

### CLI (`main.py`)

```
Programmstart
  ↓
Ausgabe: ASCII-Header + Willkommenstext
  ↓
fetch_blog_titles(limit=10)   # Scraping
  ↓
generate_all_headers(titles)  # Vollständige Pipeline für alle Titel
  ↓
Ausgabe: Pfade zu allen generierten Bildern
```

### Web-UI (`app.py`)

```
Streamlit-App startet
  ↓
Blog-Titel werden gecacht (TTL: 1 Stunde)
  ↓
Modus-Auswahl durch Benutzer:
  ├── "Alle 10 Bilder anzeigen"
  │     ↓
  │   Zeigt output/ in 2-Spalten-Raster
  │   (Warnung wenn output/ leer)
  │
  └── "Neues Bild generieren"
        ↓
      Dropdown: Blog-Titel auswählen
        ↓
      Button: "Bild generieren"
        ↓
      Spinner (15-30 Sekunden)
        ↓
      Bild anzeigen + Download-Button
```

---

## Rate Limiting

DALL-E 3 erlaubt ca. **5 Bilder pro Minute** im Standardtarif.

```python
# src/generator.py
time.sleep(15)  # 15 Sekunden Pause zwischen Generierungen
```

Bei 10 Bildern beträgt die Gesamtlaufzeit damit ca. **2,5 Minuten**.

---

## Fehlerbehandlung

| Fehlerort | Behandlung |
|---|---|
| Web-Scraping schlägt fehl | Exception wird weitergegeben (kein Silent Fail) |
| GPT-4o API-Fehler | Exception landet im Caller (CLI: Abbruch, UI: Fehlermeldung) |
| DALL-E 3 API-Fehler | Exception landet im Caller (CLI: Abbruch, UI: Fehlermeldung) |
| Bild-Download schlägt fehl | Exception wird weitergegeben |
| `output/`-Ordner fehlt | `os.makedirs(exist_ok=True)` erstellt ihn automatisch |
