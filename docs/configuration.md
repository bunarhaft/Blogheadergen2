# Konfigurationsreferenz

Alle konfigurierbaren Werte des Projekts sind zentral in zwei Dateien gebündelt: `.env` für Secrets und `src/config.py` für Anwendungsparameter.

---

## Umgebungsvariablen (`.env`)

| Variable | Pflicht | Beschreibung |
|---|---|---|
| `OPENAI_API_KEY` | ✅ Ja | OpenAI API Key für GPT-4o und DALL-E 3 |

**Beispiel `.env`:**
```env
OPENAI_API_KEY=sk-proj-...
```

> **Sicherheitshinweis**: Die `.env`-Datei enthält sensible Zugangsdaten und darf **niemals** in das Git-Repository eingecheckt werden. Füge `.env` zu `.gitignore` hinzu.

---

## Anwendungskonfiguration (`src/config.py`)

### Blog-Quelle

```python
BLOG_URL = "https://endometriose.app/aktuelles-2/"
```

Die URL der Blog-Übersichtsseite, von der Titel gescrapt werden.

---

### URL-Filter für Blog-Kategorien

```python
BLOG_URL_KEYWORDS = [
    "/impulse/",
    "/wissen-und-tipps/",
    "/ernaehrung/",
    "/forschung/",
    "/studien/",
    "/experten-interviews/",
]
```

Nur Links, die eines dieser URL-Segmente enthalten, werden als echte Blog-Posts erkannt. Dadurch werden Navigations-Links, Werbeanzeigen oder andere Seiteninhalte automatisch herausgefiltert.

**Neue Kategorie hinzufügen:**
```python
BLOG_URL_KEYWORDS = [
    "/impulse/",
    "/meine-neue-kategorie/",  # Einfach anhängen
    ...
]
```

---

### Marken-Stilrichtlinie (STYLE_ANCHOR)

```python
STYLE_ANCHOR = (
    "soft sage green (#A8C5A0), and clean white backgrounds. "
    "Professional health-app brand identity. "
    "16:9 widescreen header format. "
    "Photorealistic yet artistic, soft-focus photography style. "
    "Warm, trustworthy, and scientifically modern mood."
)
```

Der `STYLE_ANCHOR` wird an jeden DALL-E 3 Prompt angehängt und sorgt für visuelle Konsistenz über alle generierten Bilder hinweg.

**Elemente der Stilrichtlinie:**

| Element | Wert | Zweck |
|---|---|---|
| Primärfarbe | Sage Green `#A8C5A0` | Markenfarbe der Endo-App |
| Hintergrund | Clean White | Hoher Kontrast, professionell |
| Fotostil | Photorealistic, soft-focus | Authentisch, nicht steril |
| Format | 16:9 Widescreen | Header-Optimierung |
| Stimmung | Warm, trustworthy, scientifically modern | Zielgruppen-angepasst |

**Stil anpassen:**
```python
STYLE_ANCHOR = (
    "warm coral tones (#E8A090), minimal design. "
    "Medical-app aesthetic. "
    # Weitere Direktiven...
)
```

---

### Bildgröße und Qualität

```python
IMAGE_SIZE = "1792x1024"
IMAGE_QUALITY = "standard"
```

| Parameter | Wert | Optionen | Auswirkung |
|---|---|---|---|
| `IMAGE_SIZE` | `1792x1024` | `1024x1024`, `1792x1024`, `1024x1792` | Format des generierten Bildes |
| `IMAGE_QUALITY` | `standard` | `standard`, `hd` | Bildqualität und API-Kosten |

> **Hinweis**: `hd` verdoppelt die API-Kosten bei DALL-E 3 (Stand: 2024).

**DALL-E 3 Preise (ca.):**

| Qualität | Größe | Preis pro Bild |
|---|---|---|
| `standard` | `1792x1024` | ~$0.08 |
| `hd` | `1792x1024` | ~$0.12 |

---

### Ausgabe-Ordner

```python
OUTPUT_DIR = "output"
```

Relativer Pfad (ausgehend vom Projektroot) zum Ordner für generierte Bilder. Der Ordner wird automatisch erstellt, falls er nicht existiert.

---

## GPT-4o Parameter (`src/generator.py`)

Diese Werte sind direkt im Code in `build_dalle_prompt()` definiert:

| Parameter | Wert | Beschreibung |
|---|---|---|
| `model` | `gpt-4o` | Verwendetes OpenAI-Modell |
| `max_tokens` | `120` | Maximale Ausgabelänge (kurze Prompts gewünscht) |
| `temperature` | `0.7` | Kreativitätsgrad (0=deterministisch, 1=kreativ) |

---

## DALL-E 3 Parameter (`src/generator.py`)

Diese Werte sind direkt im Code in `generate_and_save_image()` definiert:

| Parameter | Wert | Beschreibung |
|---|---|---|
| `model` | `dall-e-3` | Verwendetes Bildgenerierungs-Modell |
| `size` | `1792x1024` | Bildgröße (aus `IMAGE_SIZE`) |
| `quality` | `standard` | Bildqualität (aus `IMAGE_QUALITY`) |
| `style` | `natural` | Bildästhetik (`natural` = weniger dramatisch als `vivid`) |
| `n` | `1` | Anzahl generierter Bilder pro Aufruf |

---

## Rate-Limiting-Parameter

| Parameter | Wert | Beschreibung |
|---|---|---|
| Pause zwischen Bildern | `15` Sekunden | Verhindert Überschreitung des DALL-E 3 API-Limits |
| DALL-E 3 Limit | ~5 Bilder/Minute | Standard-Tarif |

---

## Streamlit-Cache (`app.py`)

```python
@st.cache_data(ttl=3600)
def get_cached_titles():
    ...
```

| Parameter | Wert | Beschreibung |
|---|---|---|
| `ttl` | `3600` Sekunden | Blog-Titel werden 1 Stunde lang gecacht |
