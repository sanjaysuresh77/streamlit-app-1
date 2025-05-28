import streamlit as st
from PIL import Image
import base64
import zipfile
import os

# ===== Function to Set Background with CSS and Glassmorphism Panel =====
def set_background():
    with open("background.png", "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()
    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-attachment: fixed;
            background-position: center;
        }}

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
            margin-top: 3rem;
        }}

        h1, h2, h3, p, .css-17eq0hr {{
            color: #ffffff !important;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.7);
        }}

        .block-container {{
            padding-top: 0rem;
        }}

        /* Move file uploader slightly right and down to avoid EDRC text */
        div[data-testid="stFileUploader"] {{
            margin-top: 30px;
            margin-left: 30px;
            background: rgba(255, 255, 255, 0.9);
            border-radius: 12px;
            padding: 15px;
            width: 90%;
            max-width: 600px;
            box-shadow: 0 0 10px rgba(0,0,0,0.2);
        }}

        /* Hide any unexpected top text inputs if present */
        .element-container:has(input[type="text"]) {{
            display: none !important;
        }}
        </style>
    """, unsafe_allow_html=True)

# ===== Streamlit App =====
set_background()

st.markdown('<div class="glass">', unsafe_allow_html=True)

st.markdown("### 📝 EDRC - Sheet Number Tool")
st.write("Upload a **ZIP** file containing `.dxf` files.")

uploaded_file = st.file_uploader("Drag and drop file here", type=['zip'])

if uploaded_file is not None:
    with zipfile.ZipFile(uploaded_file, "r") as zip_ref:
        extract_path = "extracted_files"
        os.makedirs(extract_path, exist_ok=True)
        zip_ref.extractall(extract_path)
    st.success("✅ ZIP file uploaded and extracted successfully.")
    st.info(f"Files extracted to: `{extract_path}`")

    # You can place DXF handling or renaming code here...
    # For example:
    # process_dxf_files(extract_path)

st.markdown('</div>', unsafe_allow_html=True)
