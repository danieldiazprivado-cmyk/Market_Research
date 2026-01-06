from google.oauth2 import service_account
from googleapiclient.discovery import build
import os

CREDENTIALS_FILE = 'credentials.json'
SHEET_ID = "1ZiaahbrXOhEJMn7PkmdA7LrdhRUmVfegnZr-Or6tVyY"
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

def main():
    creds = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)

    print("--- AUDITING GAPS (COMPETENCIA) ---")
    try:
        # Read the whole block to find rows dynamically again just to be safe
        result = service.spreadsheets().values().get(
            spreadsheetId=SHEET_ID, range="Competencia!A1:K30").execute()
        rows = result.get('values', [])
        
        target_rows = {
            "Reversión de riesgo / Garantías": None,
            "Observaciones adicionales": None
        }

        # Find rows
        for i, row in enumerate(rows):
            if not row: continue
            header = row[0].strip()
            # Loose match
            for target in target_rows.keys():
                if target in header:
                    target_rows[target] = i # 0-indexed row index
                    print(f"Found '{target}' at Row {i+1}")
                    # Print the row content
                    print(f"Values: {row}")

        # Check for columns C (idx 2), D (idx 3), E (idx 4), F (idx 5), G (idx 6) ... K (idx 10)
        # to see where the data sits.
        
    except Exception as e:
        print(f"Error auditing: {e}")

if __name__ == '__main__':
    main()
