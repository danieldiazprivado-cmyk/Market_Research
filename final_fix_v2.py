import time
from google.oauth2 import service_account
from googleapiclient.discovery import build

CREDENTIALS_FILE = 'credentials.json'
SHEET_ID = "1ZiaahbrXOhEJMn7PkmdA7LrdhRUmVfegnZr-Or6tVyY"
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def authenticate():
    creds = None
    creds = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE, scopes=SCOPES)
    return creds

def main():
    service = build('sheets', 'v4', credentials=authenticate())
    print("--- INICIANDO CORRECCIÓN FINAL (PES + CONCLUSIÓN) ---")

    # 1. DEFINICIÓN DE DATOS V-ORGANEX
    pes_problem = "El mercado está polarizado: remedios caseros débiles (tés) o fármacos caros/químicos. Falta una solución POTENTE pero NATURAL que aborde la digestión Y la energía."
    pes_enemy = "La 'Toxicidad Invisible' y la Resignación. Creer que vivir inflamado y cansado es 'normal'. La industria que solo trata síntomas (antiácidos) en lugar de limpiar el filtro."
    pes_solution = "V-Organex ofrece un 'Reset Completo'. Ataca la raíz (hígado/bilis) con 7 armas naturales. No es solo protección, es RESTAURACIÓN activa que se siente en la energía y la talla."
    
    conclusion = "V-Organex domina el nicho de 'Bienestar Digestivo Integral'. Mientras Usana vende ciencia cara y Himalaya vende tradición barata, V-Organex vende RESULTADOS SENTIDOS (Energía + Ligereza). La estrategia es: 'No solo limpies tu hígado, despierta tu vida con el poder de 7 plantas'."

    # 2. LIMPIEZA DE ZONA DE CONFLICTO (Filas 23 a 40)
    print("Limpiando zona de análisis (Row 23-40)...")
    service.spreadsheets().values().clear(
        spreadsheetId=SHEET_ID, range="Competencia!B24:Z40"
    ).execute()
    
    # 3. ESCRITURA PRECISA (B24 y B26)
    
    # ROW 24: PROBLEMA (Market Gaps)
    # Nota: El header YA existe en A24 (Black Box), escribimos en B24.
    print("Escribiendo PROBLEMA en B24...")
    service.spreadsheets().values().update(
        spreadsheetId=SHEET_ID, range="Competencia!B24", valueInputOption='USER_ENTERED',
        body={'values': [[pes_problem]]}
    ).execute()

    # ROW 26: CONCLUSIÓN
    # Nota: El header YA existe en A26 (Green Box), escribimos en B26.
    print("Escribiendo CONCLUSIÓN en B26...")
    service.spreadsheets().values().update(
        spreadsheetId=SHEET_ID, range="Competencia!B26", valueInputOption='USER_ENTERED',
        body={'values': [[conclusion]]}
    ).execute()

    print("--- CORRECCIÓN DE CASILLAS FINALIZADA ---")

if __name__ == '__main__':
    main()
