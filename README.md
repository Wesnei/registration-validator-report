# Registration Validation and PDF Reporting System

## Overview
This is a **simple Python project** designed to automate the validation of participant registrations from Excel spreadsheets and generate organized PDF reports. The system classifies participants as eligible or ineligible based on rigorous validation rules applied to personal data fields, and produces clean, professional reports suitable for institutional use.

## Features
- **Excel Data Import:** Reads participant data from `.xlsx` files using the `pandas` library.
- **Data Validation:** Checks the validity of critical fields:
  - CPF (Brazilian individual taxpayer registry) with format and checksum validation.
  - RG (identity document) for minimum length and alphanumeric format.
  - Tractor operation hours (numeric and positive).
  - Age (between 1 and 120 years).
  - Email (valid format).
- **Automatic Classification:** Separates valid ("Aptos") and invalid ("Inaptos") registrations.
- **PDF Report Generation:** Creates customized PDF files for each classification using `fpdf`, featuring:
  - Institutional header.
  - Highlighted participant names.
  - Formatted participant details.
- **Automatic PDF Opening:** Opens the generated PDF reports after creation for quick review.

## Technologies
- Python 3.x
- pandas
- fpdf
- re (regular expressions)
- os & subprocess (file and system operations)

## Project Structure
```

cadastros.xlsx          # Input Excel spreadsheet with registration data
saida/                  # Output folder containing generated PDF reports
├─ aptos.pdf         # PDF report for eligible participants
└─ inaptos.pdf       # PDF report for ineligible participants
main.py                 # Main Python script executing validation and report generation
.gitignore              # Git ignore configuration (excludes venv and saida/)
README.md               # Project documentation (this file)

````

## Setup and Usage

### 1. Create and activate a Python virtual environment (venv)
```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
````

### 2. Install dependencies

```bash
pip install pandas fpdf
```

### 3. Run the script

```bash
python main.py
```

### 4. Results

* The PDF reports will be generated inside the `saida/` folder.
* The reports will open automatically after generation.

## License

This project is licensed under the MIT License.


