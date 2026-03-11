# API-Referenz

---

## OpenAI API Integration

Die gesamte OpenAI-Kommunikation läuft über das offizielle `openai` Python-Paket (Version ≥ 1.30.0).

### Client-Initialisierung

```python
# src/generator.py
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
```

Der API Key wird über die Umgebungsvariable `OPENAI_API_KEY` geladen, die in `.env` definiert und durch `python-dotenv` eingelesen wird.

---

## GPT-4o: Prompt-Optimierung

### Funktion

```python
build_dalle_prompt(title: str) -> str
```

**Zweck**: Wandelt einen deutschen Blog-Titel in eine optimierte visuelle Beschreibung für DALL-E 3 um.

### API-Aufruf

```python
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user",   "content": title}
    ],
    max_tokens=120,
    temperature=0.7,
)
```

### Parameter

| Parameter | Wert | Begründung |
|---|---|---|
| `model` | `gpt-4o` | Beste Reasoning-Fähigkeiten für Kontext-Mapping |
| `max_tokens` | `120` | Kurze, präzise visuelle Beschreibungen (2 Sätze) |
| `temperature` | `0.7` | Ausgewogenes Verhältnis: kreativ, aber konsistent |

### System-Prompt (Auszug)

Der System-Prompt instruiert GPT-4o, themenspezifische visuelle Metaphern zu wählen:

```
Du bist ein Experte für visuelle Kommunikation im Gesundheitsbereich.
Generiere eine kurze, präzise visuelle Beschreibung (max. 2 Sätze) für ein
Blog-Header-Bild basierend auf dem Titel. Berücksichtige den medizinischen
Kontext der Endometriose-App.

Thematisches Mapping:
- Rehabilitation → Krankenhauszimmer, gepackte Taschen, Erholung
- Ernährung → frisches Gemüse, entzündungshemmende Lebensmittel
- Forschung → Mikroskope, Laborgeräte
- Mental Health → Naturszenen, ruhiges Wasser
...
```

### Rückgabewert

Eine englische visuelle Beschreibung, max. 2 Sätze.

**Beispiel:**
```
Eingabe: "Interview mit Dr. Liza Ball"
Ausgabe: "A warm, professional portrait of a female doctor in a modern
          clinic setting, surrounded by medical literature and plants."
```

---

## DALL-E 3: Bildgenerierung

### Funktion

```python
generate_and_save_image(prompt: str, title: str, index: int) -> str
```

**Zweck**: Generiert ein Header-Bild und speichert es lokal.

### API-Aufruf

```python
response = client.images.generate(
    model="dall-e-3",
    prompt=f"{prompt} {STYLE_ANCHOR}",
    size=IMAGE_SIZE,       # "1792x1024"
    quality=IMAGE_QUALITY, # "standard"
    style="natural",
    n=1,
)
image_url = response.data[0].url
```

### Parameter

| Parameter | Wert | Optionen | Beschreibung |
|---|---|---|---|
| `model` | `dall-e-3` | `dall-e-2`, `dall-e-3` | DALL-E 3 für beste Qualität |
| `size` | `1792x1024` | `1024x1024`, `1792x1024`, `1024x1792` | 16:9 Landscape für Header |
| `quality` | `standard` | `standard`, `hd` | HD = höhere Qualität + höhere Kosten |
| `style` | `natural` | `natural`, `vivid` | `natural` = realistischer, weniger überdramatisch |
| `n` | `1` | `1` | DALL-E 3 unterstützt nur n=1 |

### Prompt-Aufbau

```
[GPT-4o Output] + " " + [STYLE_ANCHOR]
```

**Beispiel des finalen Prompts:**
```
A warm, professional portrait of a female doctor in a modern clinic setting,
surrounded by medical literature and plants. soft sage green (#A8C5A0), and
clean white backgrounds. Professional health-app brand identity. 16:9
widescreen header format. Photorealistic yet artistic, soft-focus photography
style. Warm, trustworthy, and scientifically modern mood.
```

### Rückgabewert

Datei-Pfad der gespeicherten PNG-Datei.

---

## Web Scraping

### Funktion

```python
fetch_blog_titles(limit: int = 10) -> list[str]
```

**Zweck**: Scrapt Blog-Titel von der Endo-App-Website.

### HTTP-Request

```python
headers = {"User-Agent": "Mozilla/5.0 ..."}
response = requests.get(BLOG_URL, headers=headers, timeout=10)
```

| Parameter | Wert |
|---|---|
| URL | `https://endometriose.app/aktuelles-2/` |
| Timeout | 10 Sekunden |
| User-Agent | Browser-ähnlicher String (Vermeidung von Blockierung) |

### HTML-Parsing

```python
soup = BeautifulSoup(response.text, "html.parser")
entries = soup.find_all("h3", class_="slide-entry-title")
```

Jeder gefundene Eintrag wird auf URL-Keywords geprüft:
```python
link_href = entry.find("a")["href"]
if any(kw in link_href for kw in BLOG_URL_KEYWORDS):
    titles.append(entry.get_text(strip=True))
```

### Rückgabewert

Liste von Blog-Titeln (max. `limit` Einträge).

---

## Rate Limits und Kosten

### DALL-E 3 Rate Limits (Standard-Tier)

| Limit | Wert |
|---|---|
| Images per minute (IPM) | ~5 |
| Images per day | Abhängig vom Account-Tier |

Die eingebaute 15-Sekunden-Pause zwischen Generierungen hält die Rate bei ~4 Bildern/Minute.

### Geschätzte Kosten pro Durchlauf (10 Bilder)

| Komponente | Kosten |
|---|---|
| GPT-4o (10 × ~120 Tokens Input + Output) | ~$0.01 |
| DALL-E 3 Standard (10 × 1792×1024) | ~$0.80 |
| **Gesamt** | **~$0.81** |

> Preise können sich ändern. Aktuelle Preise: [openai.com/api/pricing](https://openai.com/api/pricing)

---

## Hilfsfunktionen

### `sanitize_filename(title: str) -> str`

Konvertiert Blog-Titel in sichere Dateinamen:

```python
def sanitize_filename(title: str) -> str:
    title = title.lower()
    # Umlauts ersetzen
    replacements = {"ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss", ...}
    for char, replacement in replacements.items():
        title = title.replace(char, replacement)
    # Nicht-alphanumerische Zeichen durch Underscore ersetzen
    title = re.sub(r"[^a-z0-9]+", "_", title)
    # Auf 60 Zeichen begrenzen
    return title[:60].strip("_")
```

### `generate_all_headers(titles: list, callback=None) -> list[str]`

Batch-Verarbeitung aller Titel mit Rate-Limiting:

```python
def generate_all_headers(titles, callback=None):
    paths = []
    for i, title in enumerate(titles):
        prompt = build_dalle_prompt(title)
        path = generate_and_save_image(prompt, title, i + 1)
        paths.append(path)
        if callback:
            callback(i + 1, len(titles), path)
        if i < len(titles) - 1:
            time.sleep(15)  # Rate limiting
    return paths
```

Der optionale `callback`-Parameter wird vom Streamlit-UI für Fortschrittsanzeigen genutzt.
