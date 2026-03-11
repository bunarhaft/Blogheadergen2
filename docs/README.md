# BlogHeaderGen2 – Projektdokumentation

> **AI-gestützte Blog-Header-Generierung für die Endo-App**

BlogHeaderGen2 automatisiert die Erstellung von visuell konsistenten Blog-Header-Bildern für die [Endo-App](https://endometriose.app) – eine Gesundheitsapp rund um das Thema Endometriose. Das System kombiniert Web-Scraping, GPT-4o und DALL-E 3, um aus Blog-Titeln professionelle 16:9-Header-Bilder zu generieren.

---

## Inhaltsverzeichnis

- [Projektübersicht](#projektübersicht)
- [Schnellstart](#schnellstart)
- [Projektstruktur](#projektstruktur)
- [Dokumentation im Detail](#dokumentation-im-detail)

---

## Projektübersicht

### Was macht die App?

```
Blog-Titel scrapen → GPT-4o optimiert Prompt → DALL-E 3 generiert Bild → Speichern
```

1. **Scraping**: Blog-Titel werden automatisch von `endometriose.app/aktuelles-2/` gesammelt
2. **Prompt-Optimierung**: GPT-4o wandelt den deutschen Blog-Titel in eine präzise visuelle Beschreibung um
3. **Bildgenerierung**: DALL-E 3 erzeugt ein 1792×1024 px Bild im Endo-App Stil
4. **Speicherung**: Bilder werden lokal im `output/`-Ordner abgelegt

### Technologie-Stack

| Komponente | Technologie |
|---|---|
| Sprache | Python 3.11 |
| Web-UI | Streamlit |
| Text-KI | GPT-4o (OpenAI) |
| Bild-KI | DALL-E 3 (OpenAI) |
| Web-Scraping | BeautifulSoup4 + Requests |
| Deployment | Dev Container (Docker) |

---

## Schnellstart

### Voraussetzungen

- Python 3.11+
- OpenAI API Key mit Zugriff auf GPT-4o und DALL-E 3

### Installation

```bash
# Repository klonen
git clone <repo-url>
cd BlogHeaderGen2

# Abhängigkeiten installieren
pip install -r requirements.txt

# API Key konfigurieren
cp .env.example .env
# OPENAI_API_KEY in .env eintragen
```

### Nutzung

**Kommandozeile (CLI):**
```bash
python main.py
```

**Web-Interface (Streamlit):**
```bash
streamlit run app.py
```
Dann im Browser: [http://localhost:8501](http://localhost:8501)

---

## Projektstruktur

```
BlogHeaderGen2/
├── docs/                    # Projektdokumentation (diese Dateien)
│   ├── README.md            # Einstiegspunkt (diese Datei)
│   ├── architecture.md      # Systemarchitektur & Datenfluss
│   ├── configuration.md     # Konfigurationsreferenz
│   ├── usage.md             # Bedienungsanleitung
│   └── api-reference.md     # API-Integrations-Details
├── src/
│   ├── config.py            # Konfiguration, Scraping, Stilparameter
│   └── generator.py         # Bildgenerierungs-Pipeline
├── output/                  # Generierte Header-Bilder
├── app.py                   # Streamlit Web-UI
├── main.py                  # CLI-Einstiegspunkt
├── requirements.txt         # Python-Abhängigkeiten
└── .env                     # API Keys (nicht in Git!)
```

---

## Dokumentation im Detail

| Dokument | Inhalt |
|---|---|
| [architecture.md](./architecture.md) | Systemarchitektur, Datenfluss, Komponentenübersicht |
| [configuration.md](./configuration.md) | Alle Konfigurationsoptionen, Umgebungsvariablen, Stilparameter |
| [usage.md](./usage.md) | Schritt-für-Schritt Anleitung für CLI und Web-UI |
| [api-reference.md](./api-reference.md) | OpenAI API Integration, Parameter, Rate Limits |
