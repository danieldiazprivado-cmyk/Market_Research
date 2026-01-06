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
    print("--- SCOUTING 'DIFERENCIALES' ---")
    
    sheet_name = "Diferenciales" 
    
    try:
        # Check Grid Properties
        meta = service.spreadsheets().get(spreadsheetId=SHEET_ID, ranges=[f"'{sheet_name}'!A1:C10"], includeGridData=True).execute()
        sheet_data = meta['sheets'][0]['data'][0]
        
        print("Explicit Cell Dump:")
        rows = sheet_data.get('rowData', [])
        for i, row in enumerate(rows):
            values = []
            for cell in row.get('values', []):
                val = cell.get('userEnteredValue', {})
                eff = cell.get('effectiveValue', {})
                values.append(val or eff)
            print(f"Row {i+1}: {values}")

    except Exception as e:
        print(f"Error reading sheet '{sheet_name}': {e}")

if __name__ == '__main__':
    main()
