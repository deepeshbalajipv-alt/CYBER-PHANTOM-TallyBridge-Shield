# TallyBridge Integration Abuse Detection & Prevention

Beginner-friendly, offline Streamlit prototype for the CYBER PHANTOM Crimeathon defense project.

## What it does
- Accepts investigator-provided CSV evidence files.
- Identifies potential vendor/payment account changes.
- Flags rows where an approval reference is blank or unavailable.
- Displays evidence ID, request ID, vendor, old/new account suffix, credential and source context.
- Supports exact request-ID context and CSV export of alerts.
- Includes illustrative demo data for testing the dashboard.
- Includes flexible column matching and a diagnostics table to help troubleshoot CSV headers.

## Important limitations
- Rule-based prototype; it is not a trained AI model.
- It analyses only uploaded CSV files and does not connect to real systems.
- It does not block or change payments.
- A missing approval reference in a CSV is not proof that approval never existed.
- A detected change is an investigation lead, not proof of malicious activity.
- Validate column names and evidence mappings against the actual supplied evidence files.

## Windows + VS Code setup

1. Install Python 3.11 or newer from https://www.python.org/downloads/ and select **Add Python to PATH**.
2. Install Visual Studio Code from https://code.visualstudio.com/.
3. Extract this ZIP file.
4. In VS Code, choose **File > Open Folder** and open the extracted `TallyBridge_Defense_Toolkit` folder.
5. Open **Terminal > New Terminal**.
6. Create a virtual environment:
   ```powershell
   py -m venv .venv
   ```
7. Activate it in PowerShell:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```
   If PowerShell blocks activation, use Command Prompt terminal and run:
   ```bat
   .venv\Scripts\activate.bat
   ```
   Or for this terminal session only, in PowerShell:
   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   .\.venv\Scripts\Activate.ps1
   ```
8. Install packages:
   ```powershell
   py -m pip install -r requirements.txt
   ```
9. Start the app:
   ```powershell
   py -m streamlit run app.py
   ```
10. A browser tab opens. Click **Load illustrative demo data** to see a sample alert, or upload your authorized case CSV files.

## Demo workflow
1. Click **Load illustrative demo data**.
2. Confirm the app shows one potential bank-account change alert.
3. Inspect the request ID, evidence IDs and blank approval field.
4. Download the alert report as CSV.
5. For the actual case, clear demo mode by uploading your real supplied evidence CSV files.

## GitHub
Do not upload confidential evidence or credentials. Upload source code, README, and safe synthetic sample data only.


## If the alert count stays at zero
1. Check the **Input column diagnostics** table in the app.
2. Confirm that the CSV contains a recognizable action/event/description field, or old and new account fields.
3. Open **View uploaded evidence preview** and verify that the row with the change is actually present.
4. The detector flags a row when old/new account values differ, or when its text indicates a vendor/bank/account change.
5. If your evidence uses unusual column names, adjust the `ALIASES` dictionary near the top of `app.py` to include the exact header names.

The app deliberately does not treat a read-only request such as `GET vendor bank details` as a bank-account change by itself.
