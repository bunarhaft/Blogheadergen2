from src.generator import generate_all_headers
from src.config import fetch_blog_titles  # <-- fetch statt BLOG_TITLES

if __name__ == "__main__":
    print("🚀 Blog Header Generator – Endo-App")
    print("=" * 50)

    # Titel live von der Website laden
    titles = fetch_blog_titles(limit=10)

    print(f"Generiere {len(titles)} Header-Bilder...\n")
    paths = generate_all_headers(titles)

    print("\n" + "=" * 50)
    print("✅ Alle Bilder erfolgreich generiert!")
    for path in paths:
        print(f"  → {path}")