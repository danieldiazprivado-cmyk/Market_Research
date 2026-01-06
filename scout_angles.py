import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

CREDENTIALS_FILE = 'credentials.json'
SHEET_ID = "1ZiaahbrXOhEJMn7PkmdA7LrdhRUmVfegnZr-Or6tVyY"
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def authenticate():
    creds = None
    if os.path.exists(CREDENTIALS_FILE):
        creds = service_account.Credentials.from_service_account_file(
            CREDENTIALS_FILE, scopes=SCOPES)
    return creds

def find_cell_coordinates(service, sheet_name, search_text, spreadsheet_id):
    try:
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id, range=f"'{sheet_name}'!A1:Z50").execute()
        rows = result.get('values', [])
        
        for r_idx, row in enumerate(rows):
            for c_idx, cell in enumerate(row):
                if search_text.upper() in str(cell).upper():
                    return chr(65 + c_idx), r_idx + 1
        return None, None
    except Exception as e:
        print(f"Error: {e}")
        return None, None

def main():
    service = build('sheets', 'v4', credentials=authenticate())
    print("--- SCOUTING TABS & ANGLES ---")
    
    # 1. Get Tab Names
    meta = service.spreadsheets().get(spreadsheetId=SHEET_ID).execute()
    sheets = meta.get('sheets', [])
    print("Tabs found:")
    target_sheet = None
    for s in sheets:
        title = s['properties']['title']
        print(f"- '{title}'")
        if "ngul" in title or "ngle" in title: # Match Ángulos, Angulos, Angles
            target_sheet = title

    if not target_sheet:
        print("CRITICAL: Could not find 'Ángulos Venta' tab.")
        return

    print(f"Targeting Sheet: '{target_sheet}'")

    # 2. Search for Headers
    red_col, red_row = find_cell_coordinates(service, target_sheet, "ACTUALES", SHEET_ID)
    print(f"Zona ROJA (Actuales) encontrada en: {red_col}{red_row}")

    green_col, green_row = find_cell_coordinates(service, target_sheet, "NUEVOS", SHEET_ID)
    if not green_col:
         green_col, green_row = find_cell_coordinates(service, target_sheet, "DESEOS", SHEET_ID)
    print(f"Zona VERDE (Nuevos) encontrada en: {green_col}{green_row}")

    # 3. Dump Data
    if red_row:
        dump = service.spreadsheets().values().get(
            spreadsheetId=SHEET_ID, range=f"'{target_sheet}'!A{red_row}:C{red_row+15}").execute()
        print("Muestra de datos:\n", dump.get('values', []))

if __name__ == '__main__':
    main()
