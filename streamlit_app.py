import os
import re
import streamlit as st
import ezdxf
from datetime import datetime

def extract_series_and_page(filename):
    match = re.search(r'_([A-Z])_(\d{3})', filename)
    if match:
        return f"{match.group(1)}_{match.group(2)}"
    return None

def replace_text_in_dxf(filepath, output_folder, sht_value, cont_value, title_text):
    filename = os.path.basename(filepath)
    try:
        doc = ezdxf.readfile(filepath)
    except Exception as e:
        st.error(f"Failed to open {filename}: {e}")
        return

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

    output_path = os.path.join(output_folder, filename)
    doc.saveas(output_path)
    st.success(f"Processed: {filename} → SHT: {sht_value}, CONT: {cont_value}")

def main():
    st.title("DXF Text Replacer Tool")
    st.markdown("Upload DXF files and replace placeholder text like `SHT`, `CONT`, `TITLE1` automatically.")

    input_folder = st.text_input("Enter the full path of the **Input Folder** (contains DXF files):")
    output_folder = st.text_input("Enter the full path of the **Output Folder** (save edited DXFs):")

    if st.button("Start Processing"):
        if not os.path.isdir(input_folder) or not os.path.isdir(output_folder):
            st.error("Please enter valid folder paths.")
            return

        dxf_files = sorted([f for f in os.listdir(input_folder) if f.lower().endswith('.dxf')])
        series_page_map = []
        for file in dxf_files:
            series_page = extract_series_and_page(file)
            if series_page:
                series_page_map.append((file, series_page))
            else:
                st.warning(f"Skipped invalid file name format: {file}")

        for idx, (file, sht_val) in enumerate(series_page_map):
            cont_val = series_page_map[idx + 1][1] if idx + 1 < len(series_page_map) else ""
            filepath = os.path.join(input_folder, file)
            replace_text_in_dxf(filepath, output_folder, sht_val, cont_val, title_text=f"TITLE {idx + 1}")

        st.balloons()
        st.success("All DXF files processed successfully!")

if __name__ == "__main__":
    main()
