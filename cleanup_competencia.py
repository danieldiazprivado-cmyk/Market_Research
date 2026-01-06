from google.oauth2 import service_account
from googleapiclient.discovery import build
import os

CREDENTIALS_FILE = 'credentials.json'
SHEET_ID = "1ZiaahbrXOhEJMn7PkmdA7LrdhRUmVfegnZr-Or6tVyY"
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def main():
    creds = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)

    print("--- CLEANING ENTIRE COMPETITOR AREA (C-Z) ---")
    try:
        # Clear everything from C6 onwards to reset layout
        # This removes the old alternating columns (C, E, G, I, K)
        range_to_clear = "Competencia!C6:Z100"
        service.spreadsheets().values().clear(
            spreadsheetId=SHEET_ID, range=range_to_clear).execute()
        print(f"CLEARED: {range_to_clear}")
    except Exception as e:
        print(f"Error clearing: {e}")

if __name__ == '__main__':
    main()
