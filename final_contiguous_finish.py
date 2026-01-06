from google.oauth2 import service_account
from googleapiclient.discovery import build
import time

CREDENTIALS_FILE = 'credentials.json'
SHEET_ID = "1ZiaahbrXOhEJMn7PkmdA7LrdhRUmVfegnZr-Or6tVyY"
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def main():
    print("Sleeping 30s to cool down...")
    time.sleep(30)
    
    creds = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)

    print("--- RESUMING CONTIGUOUS FINISH (ROW 20+) ---")
    
    target_cols = ['C', 'D', 'E', 'F', 'G']
    
    # Warranties (Row 20)
    warranties = ["Garantía de Satisfacción VitalHealth", "Calidad farmacéutica certificada", "Marca legendaria (confianza histórica)", "Garantía de sabor", "Respaldo de marca Tienda"]
    print("Writing Warranties (C20-G20)...")
    for i, val in enumerate(warranties):
        service.spreadsheets().values().update(
            spreadsheetId=SHEET_ID, range=f"Competencia!{target_cols[i]}20",
            valueInputOption='USER_ENTERED', body={'values': [[val]]}).execute()
        time.sleep(0.5)

    # Observations (Row 21)
    observations = ["Gana por goleada en 'Ingredientes por Dosis'", "Excelente producto pero barrera de precio alta", "Sólido pero imagen anticuada", "Mucha azúcar/fructosa", "Cumple, pero no emociona"]
    print("Writing Observations (C21-G21)...")
    for i, val in enumerate(observations):
        service.spreadsheets().values().update(
            spreadsheetId=SHEET_ID, range=f"Competencia!{target_cols[i]}21",
            valueInputOption='USER_ENTERED', body={'values': [[val]]}).execute()
        time.sleep(0.5)

    # Analysis
    print("Writing Analysis...")
    pes_text = "V-Organex ofrece un 'Reset Completo'. Ataca la raíz (hígado/bilis) con 7 armas naturales. No es solo protección, es RESTAURACIÓN activa que se siente en la energía y la talla."
    conc_text = "V-Organex domina el nicho de 'Bienestar Digestivo Integral'. Mientras Usana vende ciencia cara y Himalaya vende tradición barata, V-Organex vende RESULTADOS SENTIDOS (Energía + Ligereza)."
    
    # We write to B24 and B29 (Assuming exact locations based on previous scans)
    # PES
    # Write to B24 (A24=Header). Text in B.
    # Previous scan said "Found PES at A24". So we write to B24. Wait, usually text is below?
    # User said "cuadro blanco grande a la derecha de la etiqueta".
    # So B24 is correct.
    service.spreadsheets().values().update(spreadsheetId=SHEET_ID, range=f"Competencia!B24", valueInputOption='USER_ENTERED', body={'values': [[pes_text]]}).execute()
    
    # Conclusion (Row 29)
    # Write to B29.
    service.spreadsheets().values().update(spreadsheetId=SHEET_ID, range=f"Competencia!B29", valueInputOption='USER_ENTERED', body={'values': [[conc_text]]}).execute()

    print("--- JOB DONE ---")

if __name__ == '__main__':
    main()
