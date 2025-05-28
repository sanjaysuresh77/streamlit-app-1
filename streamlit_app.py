import streamlit as st
from PIL import Image
import base64
import zipfile
import os

# ===== Function to Set Background with CSS =====
def set_background():
    with open("background.png", "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()

    st.markdown(f"""
        <style>
        /* Background image */
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-attachment: fixed;
            background-position: center;
        }}

        /* Optional: Glass-style box overrides */
        .glass {{
            background: rgba(255, 255, 255, 0.15);
            border-radius: 16px;
            padding: 2rem;
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            border: 1px solid rgba(255, 255, 255, 0.18);
            max-width: 850px;
            margin: auto;
            margin-top: 2rem;
        }}

        h1, h2, h3, p {{
            color: #ffffff !important;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.7);
        }}

        .block-container {{
            padding-top: 1rem !important;
        }}

        /* Header text customization */
        header {{
            background: rgba(0,0,0,0);
        }}
        header .st-emotion-cache-18ni7ap {{
            font-size: 32px;
            font-weight: bold;
            color: white !important;
            text-align: center;
            padding: 0.5rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.6);
        }}
        </style>
    """, unsafe_allow_html=True)

# ===== Streamlit App =====
st.set_page_config(layout="wide", page_title="EDRC Sheet Number Tool")

set_background()

# Write E2E RAIL to the built-in top box
st.title("E2E RAIL")

st.markdown('<div class="glass">', unsafe_allow_html=True)

st.markdown("### 📝 EDRC - Sheet Number Updater for Railway DXF Files")
st.write("Upload a **ZIP** file containing `.dxf` files.")

uploaded_file = st.file_uploader("Drag and drop file here", type=['zip'])

if uploaded_file is not None:
    with zipfile.ZipFile(uploaded_file, "r") as zip_ref:
        extract_path = "extracted_files"
        os.makedirs(extract_path, exist_ok=True)
        zip_ref.extractall(extract_path)
    st.success("✅ ZIP file uploaded and extracted successfully.")
    st.info(f"Files extracted to: `{extract_path}`")

st.markdown('</div>', unsafe_allow_html=True)
