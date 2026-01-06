import time
from google.oauth2 import service_account
from googleapiclient.discovery import build

CREDENTIALS_FILE = 'credentials.json'
SHEET_ID = "1ZiaahbrXOhEJMn7PkmdA7LrdhRUmVfegnZr-Or6tVyY"
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def authenticate():
    return service_account.Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)

def main():
    service = build('sheets', 'v4', credentials=authenticate())
    print("--- SCOUTING 'COHORTES' ---")
    
    sheet_name = "Cohortes" 
    
    try:
        # Read a large chunk to see the layout of the 3 Cohorts
        res = service.spreadsheets().values().get(
            spreadsheetId=SHEET_ID, range=f"'{sheet_name}'!A1:H30").execute()
        rows = res.get('values', [])
        for i, row in enumerate(rows):
            print(f"Row {i+1}: {row}")

    except Exception as e:
        print(f"Error reading sheet '{sheet_name}': {e}")

if __name__ == '__main__':
    main()
