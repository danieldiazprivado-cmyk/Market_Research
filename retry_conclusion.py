from google.oauth2 import service_account
from googleapiclient.discovery import build
import time

CREDENTIALS_FILE = 'credentials.json'
SHEET_ID = "1ZiaahbrXOhEJMn7PkmdA7LrdhRUmVfegnZr-Or6tVyY"
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def main():
    creds = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)

    print("--- RETRYING ANALYSIS/CONCLUSION WRITE ---")
    
    pes_analysis = [
        "PROBLEMA (Market Gaps): El mercado está polarizado entre 'Clínico Aburrido' (TheraBreath, SmartMouth) y 'Natural Lento' (GuruNanda). Falta una solución RÁPIDA, NATURAL y POTENTE.",
        "ENEMIGO: El 'Alcohol' (Listerine) ya es villano, pero el nuevo enemigo es el 'Tiempo' (GuruNanda requiere 10 mins) y la 'Química Agresiva' (incluso en marcas clínicas).",
        "SOLUCIÓN (Breatify): Un SERUM concentrado (Potencia Clínica) que funciona en segundos (Rapidez), con ingredientes botánicos (Seguridad Natural). El 'Bio-Hack' perfecto para el aliento."
    ]
    
    conclusion = "CONCLUSIÓN: Breatify domina el 'Blue Ocean' entre la eficacia clínica de TheraBreath y la deseabilidad natural de GuruNanda. La estrategia es: 'Potencia de Dentista, Alma Botánica, Velocidad del Rayo'."

    try:
        # Hardcoding targets based on known row finding (25, 27)
        # PES Row: 24 found -> Writing to 25, 26, 27?
        # A25, A26, A27.
        range_pes = "Competencia!A25:A27"
        service.spreadsheets().values().update(
            spreadsheetId=SHEET_ID, range=range_pes,
            valueInputOption='USER_ENTERED',
            body={'values': [[p] for p in pes_analysis]}
        ).execute()
        print("Written PES Analysis.")
        
        # Conclusion Row: 26 found header? -> Write to 27?
        # Let's write Conclusion to A28 to be safe/below.
        range_conc = "Competencia!A28"
        service.spreadsheets().values().update(
            spreadsheetId=SHEET_ID, range=range_conc,
            valueInputOption='USER_ENTERED',
            body={'values': [[conclusion]]}
        ).execute()
        print("Written General Conclusion.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
