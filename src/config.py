# src/config.py
# ---------------------------------------------------------------
# Brand Identity Konfiguration für endometriose.app / Endo-App
# Dieser "Style Anchor" wird an JEDEN Bildprompt angehängt,
# um visuelle Konsistenz über alle 10 Header-Bilder sicherzustellen.
# ---------------------------------------------------------------

# Die 10 Blog-Titel von endometriose.app/aktuelles-2/
BLOG_TITLES = [
    "Aktuelle Forschung zu Endometriose: Ein Interview mit Louis Taffs",
    "Aktuelle Forschung zu Endometriose: Ein Interview mit Idhaliz Flores, PhD",
    "Aktuelle Forschung zu Endometriose: Ein Interview mit Dr. Giorgia Elisabeth Colombo",
    "Aktuelle Forschung zu Endometriose: Ein Interview mit Dr. Lilian Aragão",
    "Aktuelle Forschung zu Endometriose: Ein Interview mit Dr. Jodie Avery",
    "Aktuelle Forschung zu Endometriose: Ein Interview mit Luana De Giorgio",
    "Aktuelle Forschung zu Endometriose: Ein Interview mit Dr. Tatjana Gibbons",
    "Aktuelle Forschung zu Endometriose: Ein Interview mit Dr. Liza Ball",
    "Aktuelle Forschung zu Endometriose: Ein Interview mit Britteny Gibson",
    "Aktuelle Forschung zu Endometriose: Ein Interview mit Dr. Ayse Nihan Kilinc",
]

# ---------------------------------------------------------------
# STYLE ANCHOR: Dieser Text wird an JEDEN DALL-E Prompt gehängt.
# Er definiert Farben, Stil, Stimmung und visuelle Sprache der Brand.
# Änderungen hier wirken sich auf ALLE 10 Bilder aus → Konsistenz!
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

# Qualität: "hd" für beste Qualität (kostet mehr Credits)
IMAGE_QUALITY = "hd"

# Ausgabe-Verzeichnis
OUTPUT_DIR = "output"