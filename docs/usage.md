# Bedienungsanleitung

---

## Voraussetzungen

- **Python 3.11** oder neuer
- **OpenAI API Key** mit aktiviertem Zugriff auf:
  - `gpt-4o` (Chat Completions)
  - `dall-e-3` (Image Generation)
- Internetverbindung (für Scraping und API-Aufrufe)

---

## Installation

### 1. Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

Die `requirements.txt` enthält:

```
openai>=1.30.0
streamlit>=1.35.0
pillow>=10.4.0
python-dotenv>=1.0.1
requests>=2.32.2
beautifulsoup4>=4.12.0
```

### 2. API Key konfigurieren

Erstelle oder bearbeite die Datei `.env` im Projektroot:

```env
OPENAI_API_KEY=sk-proj-dein-api-key-hier
```

> Der API Key wird automatisch beim Programmstart geladen. Die Datei wird durch `python-dotenv` eingelesen.

---

## CLI-Modus (`main.py`)

### Starten

```bash
python main.py
```

### Was passiert?

1. Das Programm begrüßt dich mit einem ASCII-Header
2. Es scrapt die aktuellen 10 Blog-Titel von `endometriose.app`
3. Für jeden Titel wird ein Header-Bild generiert
4. Die Bilder werden im `output/`-Ordner gespeichert
5. Am Ende werden alle Dateipfade ausgegeben

### Beispiel-Ausgabe

```
🌸 Endo-App Blog Header Generator 🌸

Blog-Titel werden geladen...
✓ 10 Titel gefunden

[1/10] Interview mit Dr. Liza Ball
  → Prompt wird optimiert...
  → Bild wird generiert...
  → Gespeichert: output/01_interview_mit_dr_liza_ball.png

[2/10] Ernährung bei Endometriose
  → ...

Fertig! Generierte Bilder:
  output/01_interview_mit_dr_liza_ball.png
  output/02_ernaehrung_bei_endometriose.png
  ...
```

### Laufzeit

Bei 10 Bildern dauert der Prozess **ca. 2,5–3 Minuten** (15 Sekunden Pause zwischen jedem Bild wegen API Rate Limits).

---

## Web-UI-Modus (`app.py`)

### Starten

```bash
streamlit run app.py
```

Danach die App im Browser öffnen: [http://localhost:8501](http://localhost:8501)

### Modus 1: Alle Bilder anzeigen

1. In der Sidebar "Alle 10 Bilder anzeigen" auswählen
2. Zuvor generierte Bilder werden in einem 2-Spalten-Raster angezeigt
3. Unter jedem Bild erscheint der zugehörige Blog-Titel

> **Hinweis**: Dieser Modus zeigt nur bereits generierte Bilder. Sind noch keine vorhanden, erscheint eine Warnung. Erst mit "Neues Bild generieren" können Bilder erstellt werden.

### Modus 2: Einzelnes Bild generieren

1. In der Sidebar "Neues Bild generieren" auswählen
2. Blog-Titel aus dem Dropdown auswählen
   - Die Titel werden automatisch von der Endo-App-Website geladen (gecacht für 1 Stunde)
3. Auf "Bild generieren" klicken
4. Einen Moment warten (ca. 15–30 Sekunden)
5. Das generierte Bild erscheint auf der Seite
6. Mit dem "Download"-Button das Bild herunterladen

---

## Dev Container (VS Code)

Das Projekt enthält eine Dev Container-Konfiguration für VS Code. Diese startet automatisch den Streamlit-Server.

### Voraussetzungen

- VS Code mit Dev Containers Extension
- Docker Desktop

### Starten

1. Repository in VS Code öffnen
2. Befehl-Palette öffnen (`Ctrl+Shift+P`)
3. "Dev Containers: Reopen in Container" auswählen
4. Warten bis der Container gebaut ist
5. Streamlit startet automatisch auf Port 8501

---

## Generierte Bilder

Alle Bilder werden im `output/`-Ordner gespeichert:

```
output/
├── 01_interview_mit_dr_liza_ball.png
├── 02_ernaehrung_bei_endometriose.png
├── 03_neue_studie_zeigt.png
└── ...
```

**Dateiformat**: PNG
**Auflösung**: 1792 × 1024 Pixel
**Seitenverhältnis**: 16:9 (ideal für Blog-Header)

### Dateinamen-Konventionen

- Kleinbuchstaben
- Leerzeichen → Unterstriche
- Umlauts werden transkribiert: `ä→ae`, `ö→oe`, `ü→ue`, `ß→ss`
- Maximale Länge: 60 Zeichen
- Präfix: zweistelliger Index (`01_`, `02_`, ...)

---

## Häufige Probleme

### "AuthenticationError: Incorrect API key"

**Ursache**: Der API Key in `.env` ist falsch oder fehlt.
**Lösung**: Überprüfe den Key in der `.env`-Datei und stelle sicher, dass kein Leerzeichen am Anfang oder Ende steht.

### "RateLimitError" von OpenAI

**Ursache**: Das API-Kontingent wurde überschritten (zu viele Anfragen in kurzer Zeit).
**Lösung**: Warte einige Minuten und starte neu. Die 15-Sekunden-Pause zwischen den Bildern sollte das normalerweise verhindern.

### Scraping liefert keine Titel

**Ursache**: Die Website-Struktur von `endometriose.app` hat sich geändert.
**Lösung**: Überprüfe `fetch_blog_titles()` in `src/config.py` – der CSS-Selektor (`h3.slide-entry-title`) muss ggf. aktualisiert werden.

### Bilder werden nicht im Web-UI angezeigt

**Ursache**: Keine Bilder im `output/`-Ordner.
**Lösung**: Zuerst mindestens ein Bild über "Neues Bild generieren" erstellen.
