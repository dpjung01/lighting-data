import os
import re
import pandas as pd
import streamlit as st
from main import parse_file, process_folder, get_next_filename, TRAYS, MEASUREMENTS, COLUMNS

# --- Folders ---
BASE_INPUT = "user_data"     # all input folders go here
OUTPUT_FOLDER = "outputs"    # all Excel files go here
os.makedirs(BASE_INPUT, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

st.title("Lighting Data Processor")

# --- New Instance Creation ---
st.subheader("Create Input Folder")
folder_name = st.text_input("Enter a name for your new input folder:")

if st.button("Create Input Folder") and folder_name:
    folder_path = os.path.join(BASE_INPUT, folder_name)
    os.makedirs(folder_path, exist_ok=True)
    st.success(f"Input folder `{folder_name}` created at `{folder_path}`. You can now upload your .txt files.")

# --- File Upload ---
st.subheader("Upload .txt Files")
uploaded_files = st.file_uploader("Upload your .txt files here", type="txt", accept_multiple_files=True)

if uploaded_files and folder_name:
    input_folder_path = os.path.join(BASE_INPUT, folder_name)
    for file in uploaded_files:
        file_path = os.path.join(input_folder_path, file.name)
        with open(file_path, "wb") as f:
            f.write(file.getbuffer())
    st.success(f"{len(uploaded_files)} files uploaded to `{folder_name}`")

# --- Process Files to Excel ---
if folder_name and uploaded_files:
    if st.button("Generate Excel"):
        # process_folder now returns the path of the Excel file
        def process_for_streamlit(input_folder, output_folder):
            all_data = []

            txt_files = [f for f in os.listdir(input_folder) if f.endswith(".txt")]
            if not txt_files:
                st.warning("No .txt files found in the folder")
                return None
            txt_files.sort()

            sections = [os.path.splitext(f)[0] for f in txt_files]
            location_order = [f"{s}{t} {m}" for s in sections for t in TRAYS for m in MEASUREMENTS]

            for filename in txt_files:
                filepath = os.path.join(input_folder, filename)
                section_prefix = os.path.splitext(filename)[0]
                file_data = parse_file(filepath, section_prefix)
                all_data.extend(file_data)

            df = pd.DataFrame(all_data, columns=COLUMNS)
            df["Location"] = pd.Categorical(df["Location"], categories=location_order, ordered=True)
            df = df.sort_values("Location")

            base_name = os.path.basename(os.path.normpath(input_folder))
            output_excel = get_next_filename(output_folder, base_name=base_name)
            df.to_excel(output_excel, index=False)
            return output_excel

        output_excel_path = process_for_streamlit(input_folder_path, OUTPUT_FOLDER)
        if output_excel_path:
            st.success(f"Excel generated: `{output_excel_path}`")
            with open(output_excel_path, "rb") as f:
                st.download_button("Download Excel", f, file_name=os.path.basename(output_excel_path))

# --- Existing Excel Files ---
st.subheader("Download Previously Generated Excel Files")
existing_excels = [f for f in os.listdir(OUTPUT_FOLDER) if f.endswith(".xlsx")]
if existing_excels:
    selected_excel = st.selectbox("Select an Excel file to download:", existing_excels)
    selected_excel_path = os.path.join(OUTPUT_FOLDER, selected_excel)
    with open(selected_excel_path, "rb") as f:
        st.download_button("Download Selected Excel", f, file_name=selected_excel)

# --- Existing Input Folders ---
st.subheader("View Existing Input Folders")
input_folders = [f for f in os.listdir(BASE_INPUT) if os.path.isdir(os.path.join(BASE_INPUT, f))]
selected_folder = st.selectbox("Choose a folder to view files:", input_folders)
if selected_folder:
    folder_path = os.path.join(BASE_INPUT, selected_folder)
    files = os.listdir(folder_path)
    st.write(f"Files in `{selected_folder}`:", files)
