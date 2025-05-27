import os
import re
import streamlit as st
import ezdxf
import tempfile
from datetime import datetime

def extract_series_and_page(filename):
    match = re.search(r'_([A-Z])_(\d{3})', filename)
    if match:
        return f"{match.group(1)}_{match.group(2)}"
    return None

def replace_text_in_dxf(file, sht_value, cont_value, title_text):
    try:
        doc = ezdxf.read(file.read())
    except Exception as e:
        st.error(f"Failed to open {file.name}: {e}")
        return None, None

    msp = doc.modelspace()

    def replace_entity_text(entity):
        text = entity.dxf.text.strip()
        if text == 'SHT':
            entity.dxf.text = sht_value
        elif text == 'CONT':
            entity.dxf.text = cont_value
        elif text == 'TITLE1':
            entity.dxf.text = title_text

    for entity in msp:
        if entity.dxftype() in ('TEXT', 'MTEXT'):
            replace_entity_text(entity)
        elif entity.dxftype() == 'INSERT':
            for attrib in entity.attribs:
                if attrib.dxf.tag == 'SHT':
                    attrib.dxf.text = sht_value
                elif attrib.dxf.tag == 'CONT':
                    attrib.dxf.text = cont_value
                elif attrib.dxf.tag == 'TITLE1':
                    attrib.dxf.text = title_text

    for block in doc.blocks:
        for entity in block:
            if entity.dxftype() in ('TEXT', 'MTEXT'):
                replace_entity_text(entity)

    # Save to temp file
    temp_dir = tempfile.gettempdir()
    output_path = os.path.join(temp_dir, file.name)
    doc.saveas(output_path)

    return file.name, output_path

def main():
    st.title("📐 DXF Batch Text Replacer Tool")
    st.markdown("Upload DXF files and replace placeholder text like `SHT`, `CONT`, `TITLE1`. You’ll be able to download the updated files after processing.")

    uploaded_files = st.file_uploader("Upload DXF files", type="dxf", accept_multiple_files=True)

    if uploaded_files and st.button("Start Processing"):
        series_page_map = []
        for file in uploaded_files:
            series_page = extract_series_and_page(file.name)
            if series_page:
                series_page_map.append((file, series_page))
            else:
                st.warning(f"Skipped invalid file name format: {file.name}")

        output_files = []
        for idx, (file, sht_val) in enumerate(series_page_map):
            cont_val = series_page_map[idx + 1][1] if idx + 1 < len(series_page_map) else ""
            filename, output_path = replace_text_in_dxf(file, sht_val, cont_val, title_text=f"TITLE {idx + 1}")
            if output_path:
                output_files.append((filename, output_path))
                st.success(f"✅ Processed: {filename}")

        st.markdown("---")
        st.subheader("📥 Download Processed Files")

        for filename, path in output_files:
            with open(path, "rb") as f:
                st.download_button(
                    label=f"⬇ Download {filename}",
                    data=f,
                    file_name=filename,
                    mime="application/dxf"
                )

        st.balloons()
        st.success("All files processed successfully!")

if __name__ == "__main__":
    main()
