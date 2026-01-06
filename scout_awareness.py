import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

CREDENTIALS_FILE = 'credentials.json'
SHEET_ID = "1ZiaahbrXOhEJMn7PkmdA7LrdhRUmVfegnZr-Or6tVyY"
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def authenticate():
    return service_account.Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)

def main():
    service = build('sheets', 'v4', credentials=authenticate())
    print("--- SCOUTING AWARENESS TAB ---")
    
    # 1. Get Tab Names
    meta = service.spreadsheets().get(spreadsheetId=SHEET_ID).execute()
    sheets = meta.get('sheets', [])
    print("Tabs found:")
    target_sheet = None
    for s in sheets:
        title = s['properties']['title']
        print(f"- '{title}'")
        if "Conciencia" in title or "Consciencia" in title: 
            target_sheet = title

    if not target_sheet:
        print("CRITICAL: Could not find 'Nivel Conciencia' tab.")
        return

    print(f"Targeting Sheet: '{target_sheet}'")
    
    # 2. Check headers
    try:
        res = service.spreadsheets().values().get(
            spreadsheetId=SHEET_ID, range=f"'{target_sheet}'!A1:H10").execute()
        rows = res.get('values', [])
        for i, row in enumerate(rows):
            print(f"Row {i+1}: {row}")
            
    except Exception as e:
        print(f"Error reading sheet '{target_sheet}': {e}")

if __name__ == '__main__':
    main()
