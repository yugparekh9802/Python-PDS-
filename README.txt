STUDENT MANAGEMENT SYSTEM - SIMPLIFIED PBL 3

Files:
- app.py: Streamlit application with dashboard and Add/View/Search/Update/Delete.
- students.csv: Your original dataset copied without changes.
- requirements.txt: Only Streamlit and Pandas.
- generate_dataset.py: Optional generator. Running it overwrites students.csv.

Setup in VS Code:
1. Extract this folder.
2. Open the folder in VS Code.
3. Open Terminal > New Terminal.
4. (Optional) Create a virtual environment:
   py -m venv .venv
   .venv\Scripts\activate
5. Install packages:
   py -m pip install -r requirements.txt
6. Start the application:
   py -m streamlit run app.py

Important:
Keep app.py and students.csv in the same folder.
The app automatically saves added, updated, and deleted records in students.csv.
Do not run generate_dataset.py unless you want to replace the current dataset.
