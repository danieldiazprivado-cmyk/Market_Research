from google.oauth2 import service_account
from googleapiclient.discovery import build
import time

CREDENTIALS_FILE = 'credentials.json'
SHEET_ID = "1ZiaahbrXOhEJMn7PkmdA7LrdhRUmVfegnZr-Or6tVyY"
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def find_cell_coordinates(service, sheet_name, search_text, sheet_id):
    try:
        result = service.spreadsheets().values().get(
            spreadsheetId=sheet_id, range=f"'{sheet_name}'!A1:Z50").execute()
        rows = result.get('values', [])
        for r_idx, row in enumerate(rows):
            for c_idx, cell in enumerate(row):
                if search_text.upper() in str(cell).upper():
                    return chr(65 + c_idx), r_idx + 1
        return None, None
    except Exception as e:
        print(f"Find Error: {e}")
        return None, None

def write_data(service, sheet_id, range_name, values):
    body = {'values': values}
    service.spreadsheets().values().update(
        spreadsheetId=sheet_id, range=range_name,
        valueInputOption='USER_ENTERED', body=body).execute()

def main():
    creds = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds) # Use 'service' consistently

    print("--- FIXING ALIGNMENT & PES ---")

    # 1. FIX PES & CONCLUSION (Move to Col B)
    # Define Content (Split Label vs Text)
    pes_items = [
        ("PROBLEMA (Market Gaps)", "El mercado está polarizado entre 'Clínico Aburrido' (TheraBreath, SmartMouth) y 'Natural Lento' (GuruNanda). Falta una solución RÁPIDA, NATURAL y POTENTE."),
        ("ENEMIGO", "El 'Alcohol' (Listerine) ya es villano, pero el nuevo enemigo es el 'Tiempo' (GuruNanda requiere 10 mins) y la 'Química Agresiva' (incluso en marcas clínicas)."),
        ("SOLUCIÓN", "Un SERUM concentrado (Potencia Clínica) que funciona en segundos (Rapidez), con ingredientes botánicos (Seguridad Natural). El 'Bio-Hack' perfecto para el aliento.")
    ]
    conclusion_text = "Breatify domina el 'Blue Ocean' entre la eficacia clínica de TheraBreath y la deseabilidad natural de GuruNanda. La estrategia es: 'Potencia de Dentista, Alma Botánica, Velocidad del Rayo'."

    col, row = find_cell_coordinates(service, "Competencia", "Análisis P.E.S", SHEET_ID)
    if col and row:
        print(f"Found PES Header at {col}{row}")
        # Write 3 rows below
        # Label in A, Text in B
        start_r = row + 1
        for i, (label, text) in enumerate(pes_items):
            current_r = start_r + i
            # Write Label (Col A)
            write_data(service, SHEET_ID, f"Competencia!A{current_r}", [[label]])
            # Write Text (Col B)
            write_data(service, SHEET_ID, f"Competencia!B{current_r}", [[text]])
            print(f"Written PES Row {current_r} (Label A, Text B)")

    # Conclusion
    c_col, c_row = find_cell_coordinates(service, "Competencia", "CONCLUSIÓN GENERAL", SHEET_ID)
    if c_col and c_row:
        # Write Text to B (Header is likely in A or Merged, so we target B next to it)
        # Assuming Header is in Row 'c_row'.
        # User said "rellenarse en el recuadro de al lado".
        # If header is in A29, Text goes to B29.
        target_cell = f"Competencia!B{c_row+1}" 
        # Wait, usually text is below header?
        # User said "al lado" (beside). 
        # If Header is "CONCLUSIÓN GENERAL" (Title), maybe text goes BELOW but "al lado" of implied label?
        # Actually, let's look at PES. 
        # Header "Análisis P.E.S".
        # Items "Problema", "Enemigo", "Solucion" are below.
        # "Conclusion" is likely a header like "Analisis".
        # So text goes below it.
        # But "Conclusion" might be just one block.
        # Let's write to A and B just in case?
        # If Header is A26.
        # I'll write "CONCLUSIÓN" to A27, Text to B27.
        write_data(service, SHEET_ID, f"Competencia!A{c_row+1}", [["CONCLUSIÓN"]])
        write_data(service, SHEET_ID, f"Competencia!B{c_row+1}", [[conclusion_text]])
        print(f"Written Conclusion to B{c_row+1}")

    # 2. FIX WARRANTIES & OBSERVATIONS (Strict C, E, G, I, K)
    warranties = [
        "Garantía Incondicional (Reembolso completo).",
        "Política de Devolución 30 Días (Compra directa).",
        "Garantía de Satisfacción (Contra gases VSC).",
        "Garantía 'Love the Results' (30 días).",
        "Garantía 'Friendly' (Reemplazo/Reembolso)."
    ]
    observations = [
        "Branding médico anticuado. Sabor 'medicine-like'. No lifestyle.",
        "Rutina de 10 minutos (barrera alta). Botella aceitosa/messy.",
        "Sistema Dual-Pour complejo/frágil. No travel-friendly.",
        "Precio Premium ($20+). Requiere uso continuo (lento).",
        "Percibido como genérico/débil. Falta autoridad clínica."
    ]

    target_cols = ['C', 'E', 'G', 'I', 'K']
    clear_cols = ['D', 'F', 'H', 'J'] # Explicit cleanup

    # Find Warranties Row
    w_col, w_row = find_cell_coordinates(service, "Competencia", "Reversión de riesgo", SHEET_ID)
    if w_row:
        print(f"Fixing Warranties at Row {w_row}")
        # Clear gaps first
        for c in clear_cols:
            service.spreadsheets().values().clear(
                spreadsheetId=SHEET_ID, range=f"Competencia!{c}{w_row}").execute()
        # Write data
        for i, val in enumerate(warranties):
            write_data(service, SHEET_ID, f"Competencia!{target_cols[i]}{w_row}", [[val]])

    # Find Observations Row
    o_col, o_row = find_cell_coordinates(service, "Competencia", "Observaciones adicionales", SHEET_ID)
    if o_row:
        print(f"Fixing Observations at Row {o_row}")
        # Clear gaps
        for c in clear_cols:
            service.spreadsheets().values().clear(
                spreadsheetId=SHEET_ID, range=f"Competencia!{c}{o_row}").execute()
        # Write data
        for i, val in enumerate(observations):
            write_data(service, SHEET_ID, f"Competencia!{target_cols[i]}{o_row}", [[val]])

    print("--- FIX COMPLETE ---")

if __name__ == '__main__':
    main()
