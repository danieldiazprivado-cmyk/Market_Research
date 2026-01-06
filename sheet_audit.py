
import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

# CONFIGURATION
CREDENTIALS_FILE = 'credentials.json'
SHEET_ID = "1ZiaahbrXOhEJMn7PkmdA7LrdhRUmVfegnZr-Or6tVyY"
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

def authenticate():
    creds = None
    if os.path.exists(CREDENTIALS_FILE):
        creds = service_account.Credentials.from_service_account_file(
            CREDENTIALS_FILE, scopes=SCOPES)
    return creds

def get_sheet_values(service, sheet_range):
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SHEET_ID, range=sheet_range).execute()
    return result.get('values', [])

def audit_structure():
    creds = authenticate()
    service = build('sheets', 'v4', credentials=creds)

    print("--- FASE 1: AUDITORÍA DE COORDENADAS (PRODUCTO) ---\n")
    
    # Scan Columns A to G, Rows 1 to 50
    print("Scanning 'Producto'!A1:H50 for key headers...")
    prod_values = get_sheet_values(service, "'Producto'!A1:H50")
    
    targets = [
        "NOMBRE DEL PRODUCTO",
        "DATOS TÉCNICOS", # Often the start of table
        "CARACTERÍSTICAS", # Col A header check
        "BENEFICIOS", # Col C header check
        "SIGNIFICADOS", # Col E header check
        "INFORMACIÓN DEL PRODUCTOR",
        "HISTORIA DEL PRODUCTO",
        "PALABRAS CLAVE"
    ]
    
    found_map = {}

    for r_idx, row in enumerate(prod_values):
        for c_idx, cell in enumerate(row):
            cell_str = str(cell).upper().strip()
            # Check if any target is in cell content
            for t in targets:
                if t in cell_str:
                    col_letter = chr(65 + c_idx)
                    row_num = r_idx + 1
                    coord = f"{col_letter}{row_num}"
                    print(f"FOUND '{t}' at {coord} => Content: '{cell}'")
                    found_map[t] = (col_letter, row_num)
    
    print("\n--- INFERRED DATA TARGETS (WHITE CELLS) ---")
    
    if "NOMBRE DEL PRODUCTO" in found_map:
        c, r = found_map["NOMBRE DEL PRODUCTO"] # e.g. A3
        print(f"-> WRITE NAME AT: {c}{int(r)+1}")

    if "INFORMACIÓN DEL PRODUCTOR" in found_map:
        c, r = found_map["INFORMACIÓN DEL PRODUCTOR"] # e.g. A22
        print(f"-> WRITE PRODUCER AT: {c}{int(r)+1}")

    if "HISTORIA DEL PRODUCTO" in found_map:
        c, r = found_map["HISTORIA DEL PRODUCTO"] # e.g. A26
        print(f"-> WRITE HISTORY AT: {c}{int(r)+1}")

    if "PALABRAS CLAVE" in found_map:
        c, r = found_map["PALABRAS CLAVE"]
        print(f"-> WRITE KEYWORDS AT: {c}{int(r)+1}")
        
    print("\nCheck Table Columns presence:")
    # Verify if Features=A, Benefits=C, Meanings=E based on proximity or explicit finding
    # We dump Row 7 just to see if it looks like the start of the table
    print("Checking Row 7 content (potential table start):")
    if len(prod_values) >= 7:
        print(prod_values[6]) # 0-indexed idx 6 is Row 7
    
if __name__ == '__main__':
    audit_structure()
