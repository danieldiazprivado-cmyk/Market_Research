
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os

CREDENTIALS_FILE = 'credentials.json'
SHEET_ID = "1ZiaahbrXOhEJMn7PkmdA7LrdhRUmVfegnZr-Or6tVyY"
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

def main():
    if not os.path.exists(CREDENTIALS_FILE):
        print("Credentials file not found.")
        return

    creds = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)

    try:
        sheet_metadata = service.spreadsheets().get(spreadsheetId=SHEET_ID).execute()
        sheets = sheet_metadata.get('sheets', '')
        print(f"SUCCESS: Connected to Spreadsheet '{sheet_metadata.get('properties', {}).get('title')}'")
        print("Available Tabs (ID - Title):")
        for sheet in sheets:
            props = sheet.get('properties', {})
            print(f" - ID: {props.get('sheetId')} | Title: '{props.get('title')}'")
            
    except Exception as e:
        print(f"ERROR: Could not access spreadsheet. Detail: {e}")

if __name__ == '__main__':
    main()
