from google.oauth2 import service_account
from googleapiclient.discovery import build

CREDENTIALS_FILE = 'credentials.json'
SHEET_ID = "1ZiaahbrXOhEJMn7PkmdA7LrdhRUmVfegnZr-Or6tVyY"
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def main():
    creds = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)

    print("--- FIXING CONCLUSION (Col B) ---")
    
    # Text
    conclusion_text = "Breatify domina el 'Blue Ocean' entre la eficacia clínica de TheraBreath y la deseabilidad natural de GuruNanda. La estrategia es: 'Potencia de Dentista, Alma Botánica, Velocidad del Rayo'."

    # RESTORE DAMAGE (Row 15)
    print("Restoring Row 15 'Pruebas'...")
    service.spreadsheets().values().update(
        spreadsheetId=SHEET_ID, range="Competencia!A15",
        valueInputOption='USER_ENTERED', body={'values': [['Pruebas']]}).execute()
    service.spreadsheets().values().clear(
        spreadsheetId=SHEET_ID, range="Competencia!B15").execute()

    # FORCE WRITE CONCLUSION (Row 29)
    # Previous operations overwrote the original row. We place it safely below PES.
    print("Writing Conclusion to Row 29...")
    
    # Label
    service.spreadsheets().values().update(
        spreadsheetId=SHEET_ID, range="Competencia!A29",
        valueInputOption='USER_ENTERED', body={'values': [['CONCLUSIÓN GENERAL']]}).execute()
        
    # Text
    service.spreadsheets().values().update(
        spreadsheetId=SHEET_ID, range="Competencia!B29",
        valueInputOption='USER_ENTERED', body={'values': [[conclusion_text]]}).execute()
    
    print("Conclusion Written.")

if __name__ == '__main__':
    main()
