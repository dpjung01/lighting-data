import os
import pandas as pd
import re

# Fixed order for locations (L/M/R trays, 1–4 each)
TRAYS = ["L", "M", "R"]
MEASUREMENTS = ["1", "2", "3", "4"]

# Location order for sorting in Excel
SECTIONS = []  # will be populated dynamically from file names
LOCATION_ORDER = []

# Column headers
COLUMNS = ["Location", "PFD", "PPFD", "PVD-UV", "PFD-B", "PFD-G", "PFD-R", "PFD-FR"]

def parse_file(filepath, section_prefix):
    data = []
    with open(filepath, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    real_sections = lines[1:13]  # skip header

    for idx, line in enumerate(real_sections, start=1):
        values = line.split("\t")

        numeric_values = []
        for v in values:
            try:
                numeric_values.append(float(v))
            except ValueError:
                continue

        numeric_values = numeric_values[:7]

        location = f"{section_prefix}{TRAYS[(idx-1)//4]} {MEASUREMENTS[(idx-1)%4]}"
        row = [location] + numeric_values
        data.append(row)

    return data

def get_next_filename(output_folder, base_name, ext=".xlsx"):
    existing_files = [f for f in os.listdir(output_folder) if f.startswith(base_name) and f.endswith(ext)]
    counters = []
    pattern = re.compile(rf"{re.escape(base_name)}_(\d+){ext}")
    for f in existing_files:
        match = pattern.match(f)
        if match:
            counters.append(int(match.group(1)))
    next_counter = max(counters, default=0) + 1
    return os.path.join(output_folder, f"{base_name}_{next_counter}{ext}")

def process_folder(input_folder, output_folder):
    all_data = []

    txt_files = [f for f in os.listdir(input_folder) if f.endswith(".txt")]
    if not txt_files:
        print("No .txt files found in the folder")
        return
    txt_files.sort()

    global SECTIONS, LOCATION_ORDER
    SECTIONS = [os.path.splitext(f)[0] for f in txt_files]
    LOCATION_ORDER = [f"{s}{t} {m}" for s in SECTIONS for t in TRAYS for m in MEASUREMENTS]

    for filename in txt_files:
        filepath = os.path.join(input_folder, filename)
        section_prefix = os.path.splitext(filename)[0]
        file_data = parse_file(filepath, section_prefix)
        all_data.extend(file_data)

    df = pd.DataFrame(all_data, columns=COLUMNS)
    df["Location"] = pd.Categorical(df["Location"], categories=LOCATION_ORDER, ordered=True)
    df = df.sort_values("Location")

    # Use input folder name as Excel output filename
    base_name = os.path.basename(os.path.normpath(input_folder))
    output_excel = get_next_filename(output_folder, base_name=base_name)

    df.to_excel(output_excel, index=False)
    print(f"Saved Excel file: {output_excel}")

if __name__ == "__main__":
    input_folder = "100s_data"          # Input folder with .txt files
    output_folder = "outputs"           # Export folder to save Excel files
    os.makedirs(output_folder, exist_ok=True)
    process_folder(input_folder, output_folder)
