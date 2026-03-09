# main.py  ← im Projektstamm anlegen
# ---------------------------------------------------------------
# Direkt ausführbar: python main.py
# Generiert alle 10 Header-Bilder und speichert sie in /output
# ---------------------------------------------------------------

from src.generator import generate_all_headers
from src.config import BLOG_TITLES

if __name__ == "__main__":
    print("🚀 Blog Header Generator – Endo-App")
    print("=" * 50)
    print(f"Generiere {len(BLOG_TITLES)} Header-Bilder...\n")

    paths = generate_all_headers(BLOG_TITLES)

    print("\n" + "=" * 50)
    print("✅ Alle Bilder erfolgreich generiert!")
    print("\nGespeicherte Dateien:")
    for path in paths:
        print(f"  → {path}")