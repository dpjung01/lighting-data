# lighting

BEFORE STARTING:
Create a folder called "Outputs". This is where the excel files will be saved. If this is not done, the files will be generated but you will not be able to access it because the code won't have a place to store it.



TO USE:
1. Create an output folder called "outputs"
2. All 'input' files should include a letter "A", "B', .. "I"
3. Create an inputs folder. You can name it whatever you want. Make sure ALL input files are in this folder.
4. In the very last section, change:
  input_folder = "data" --> input_folder "your input folder name"

if __name__ == "__main__":

    **input_folder = "data"          # folder with your .txt files**
    
    output_folder = "outputs"       # folder to save Excel files
    
    os.makedirs(output_folder, exist_ok=True)
    
    process_folder(input_folder, output_folder)



TO RUN:
1. Clone the Repository:
  git clone <repository_url>
  cd <repository_folder>

2. Create a virtual environment
  python3 -m venv venv

3. Activate the venv
  windows: venv\Scripts\Activate.ps1
  mac: source venv/bin/activate

4. Install required packages
  pip install pandas openpyxl

5. Run the script
  python main.py
