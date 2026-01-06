from google.oauth2 import service_account
from googleapiclient.discovery import build
import os

CREDENTIALS_FILE = 'credentials.json'
# Verified ID from market_research.py
SHEET_ID = "1ZiaahbrXOhEJMn7PkmdA7LrdhRUmVfegnZr-Or6tVyY"
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

def main():
    creds = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)

    print(f"--- DEBUGGING SHEET: {SHEET_ID} ---")
    try:
        # 1. Get Spreadsheet Meta
        meta = service.spreadsheets().get(spreadsheetId=SHEET_ID).execute()
        print(f"Title: {meta.get('properties', {}).get('title')}")
        print("Tabs:")
        found_comp = False
        for s in meta.get('sheets', []):
            title = s['properties']['title']
            print(f" - {title}")
            if "Competencia" in title:
                found_comp = True
        
        if found_comp:
            print("\n--- READING 'Competencia!A1:Z10' (Header Search) ---")
            result = service.spreadsheets().values().get(
                spreadsheetId=SHEET_ID, range="Competencia!A1:Z10").execute()
            rows = result.get('values', [])
            for i, row in enumerate(rows):
                print(f"Row {i+1}: {row}")

            print("\n--- READING 'Competencia!A1:A100' (Row Search) ---")
            result_rows = service.spreadsheets().values().get(
                spreadsheetId=SHEET_ID, range="Competencia!A1:A100").execute()
            all_rows = result_rows.get('values', [])
            for i, row in enumerate(all_rows):
                if row: # Only print non-empty for brevity
                    print(f"Row {i+1}: {row}")
        else:
            print("\nCRITICAL: 'Competencia' tab NOT found in list.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
