import streamlit as st
import os
from pathlib import Path
from src.config import fetch_blog_titles, OUTPUT_DIR  # BLOG_TITLES → fetch_blog_titles
from src.generator import generate_and_save_image

# --- Titel einmalig beim App-Start laden (gecacht für Performance) ---
@st.cache_data(ttl=3600)  # Cache für 1 Stunde, dann neu scrapen
def get_titles():
    return fetch_blog_titles(limit=10)

st.set_page_config(
    page_title="Endo-App Blog Header Generator",
    page_icon="🌸",
    layout="wide",
)

st.markdown("""
    <style>
    .main { background-color: #fdf8f6; }
    h1 { color: #c0607a; }
    .stButton button { 
        background-color: #c0607a; 
        color: white; 
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🌸 Endo-App Blog Header Generator")
st.markdown(
    "Automatische KI-generierte Header-Bilder für den Endo-Blog. "
    "Konsistenter Stil, abgestimmt auf die Brand Identity der Endo-App."
)
st.divider()

# Titel von Website laden
BLOG_TITLES = get_titles()

mode = st.radio(
    "Modus wählen:",
    ["📋 Alle 10 Bilder anzeigen (bereits generiert)", "🎨 Neues Bild generieren"],
    horizontal=True,
)

if mode == "📋 Alle 10 Bilder anzeigen (bereits generiert)":
    st.subheader("Generierte Header-Bilder")
    cols = st.columns(2)
    output_path = Path(OUTPUT_DIR)
    image_files = sorted(output_path.glob("*.png"))

    if not image_files:
        st.warning("Noch keine Bilder generiert. Führe zuerst `python main.py` aus.")
    else:
        for i, (img_path, title) in enumerate(zip(image_files, BLOG_TITLES)):
            with cols[i % 2]:
                st.image(str(img_path), use_container_width=True)
                st.caption(f"**{title}**")

elif mode == "🎨 Neues Bild generieren":
    st.subheader("Einzelnes Bild generieren")

    selected_title = st.selectbox("Blog-Titel auswählen:", BLOG_TITLES, index=0)
    selected_index = BLOG_TITLES.index(selected_title)

    if st.button("🎨 Bild generieren", type="primary"):
        with st.spinner("KI generiert dein Bild... (ca. 15-30 Sekunden)"):
            try:
                filepath = generate_and_save_image(selected_title, selected_index)
                st.success("✅ Bild erfolgreich generiert!")
                st.image(filepath, use_container_width=True)
                st.caption(f"**{selected_title}**")

                with open(filepath, "rb") as f:
                    st.download_button(
                        "⬇️ Bild herunterladen",
                        data=f,
                        file_name=os.path.basename(filepath),
                        mime="image/png",
                    )
            except Exception as e:
                st.error(f"Fehler: {e}")

st.divider()
st.markdown(
    "🤖 Powered by **GPT-4o** (Prompt-Optimierung) + **DALL-E 3** (Bildgenerierung) | "
    "Consistent style via Brand Style Anchor"
)