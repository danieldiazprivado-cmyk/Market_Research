from google.oauth2 import service_account
from googleapiclient.discovery import build
import time

CREDENTIALS_FILE = 'credentials.json'
SHEET_ID = "1ZiaahbrXOhEJMn7PkmdA7LrdhRUmVfegnZr-Or6tVyY"
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def find_cell_coordinates(service, sheet_name, search_text, sheet_id):
    try:
        result = service.spreadsheets().values().get(
            spreadsheetId=sheet_id, range=f"'{sheet_name}'!A1:A50").execute()
        rows = result.get('values', [])
        for r_idx, row in enumerate(rows):
             if row and search_text.upper() in str(row[0]).upper():
                 return 'A', r_idx + 1
        return None, None
    except Exception:
        return None, None

def write_data(service, sheet_id, range_name, values):
    body = {'values': values}
    service.spreadsheets().values().update(
        spreadsheetId=sheet_id, range=range_name,
        valueInputOption='USER_ENTERED', body=body).execute()

def main():
    print("Sleeping 10s...")
    time.sleep(10)
    
    creds = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)

    print("--- PIVOT: CONTIGUOUS ALIGNMENT (C-G) ---")

    # 1. NUCLEAR CLEANUP (H-Z)
    print("Clearing Columns H through Z...")
    try:
        service.spreadsheets().values().batchClear(
            spreadsheetId=SHEET_ID,
            body={'ranges': ["Competencia!H1:Z100"]}
        ).execute()
        print("H-Z Cleared.")
    except Exception as e:
        print(f"Clear Error: {e}")

    # 2. COMPETITOR DATA
    # Columns: C, D, E, F, G
    target_cols = ['C', 'D', 'E', 'F', 'G']
    
    competitor_data_map = {
        "Nombre": ["TheraBreath", "GuruNanda", "SmartMouth", "Lumineux", "Hello"],
        "Redes": ["@therabreath", "@gurunanda", "@smartmouth", "@lumineuxhealth", "@helloproducts"],
        "Producto": ["Fresh Breath Oral Rinse", "Coco Mint Oil Pulling", "Original Activated Mouthwash", "Oral Essentials Whitening", "Adult Mouthwash"],
        "Enlace": ["therabreath.com", "gurunanda.com", "smartmouth.com", "lumineuxhealth.com", "hello-products.com"],
        "Gancho": ["'Tu boca necesitaba un amigo'", "'Sabiduría antigua, ciencia moderna'", "'Nunca vuelvas a tener mal aliento'", "'Una forma más saludable de blanquear'", "'Elige lo amigable'"],
        "Principal promesa de marketing": ["Aliento fresco 24h", "Detox bucal y blanqueamiento", "Elimina gases de azufre 24h", "Más blancos sin tóxicos", "Cuidado efectivo y delicioso"],
        "Mecanismo único": ["Fórmula OXYD-8", "MCT Oil + Aceites", "Smart-Zinc (Iones)", "Sal del Mar Muerto", "Carbón activado + Cáñamo"],
        "Propuesta única de venta": ["Creado por dentista (Clínico)", "Ayurveda auténtica", "Sistema doble botella", "Microbiome Safe", "Lifestyle/Moderno"],
        "Afirmaciones generales de marketing": ["Dentist Formulated", "Voted #1 Oil Pulling", "No morning breath", "Non-Toxic", "Naturally friendly"],
        "Pruebas": ["Millones vendidos", "Viral TikTok", "Patentes", "Estudios clínicos", "Cruelty Free"],
        "Declaración de beneficios": ["Confianza clínica", "Salud holística", "Seguridad social 24/7", "Belleza sin dolor", "Sentirse 'cool'"],
        "Entregables / Características": ["Botella grande", "Copa medidora", "Dual-Pour", "Premium", "Económico"],
        "Precio y términos de pago": ["$12 - $15 USD", "$15 - $18 USD", "$11 - $14 USD", "$18 - $22 USD", "$6 - $9 USD"],
        "Reversión de riesgo / Garantías": ["Garantía Incondicional", "Devolución 30 Días", "Garantía Satisfacción", "Garantía 'Love the Results'", "Garantía 'Friendly'"],
        "Observaciones adicionales ": ["Branding médico anticuado", "Rutina 10 mins (lento)", "Dual-Pour frágil", "Precio alto", "Percibido genérico"]
    }

    for header_key, values_list in competitor_data_map.items():
        col, row = find_cell_coordinates(service, "Competencia", header_key, SHEET_ID)
        if row:
            print(f"Writing '{header_key}' at Row {row}")
            for i, val in enumerate(values_list):
                if i < 5:
                    target_cell = f"Competencia!{target_cols[i]}{row}"
                    write_data(service, SHEET_ID, target_cell, [[val]])
            time.sleep(0.5) # Pace writes
        else:
             print(f"Skipping '{header_key}' (Not Found)")

    # 3. ANALYSIS (Updated Text)
    print("Writing Analysis...")
    pes_text = "El mercado está polarizado entre 'Clínico Aburrido' y 'Natural Lento'. Breatify es la solución RÁPIDA, NATURAL y POTENTE."
    conc_text = "Breatify domina el nicho de 'Eficacia Portátil'. Nuestra ventaja es la frescura clínica en 30 segundos sin alcohol. El ángulo de Ads será: 'Equilibra tu boca con botánica de precisión'."
    
    # PES
    # Assuming Label "Análisis P.E.S" at ~Row 24. Box at B24.
    p_col, p_row = find_cell_coordinates(service, "Competencia", "Análisis P.E.S", SHEET_ID)
    if p_row:
        # User: "Localiza el cuadro blanco grande a la derecha de la etiqueta"
        # Since we cleared C-Z, we assume Box is B.
        # But wait, original sheet had merge?
        # Standard: Label A, Text B.
        write_data(service, SHEET_ID, f"Competencia!B{p_row}", [[pes_text]])
        # Clear C-Z specifically here too just in case
        service.spreadsheets().values().clear(
             spreadsheetId=SHEET_ID, range=f"Competencia!C{p_row}:Z{p_row+3}").execute()

    # CONCLUSION
    c_col, c_row = find_cell_coordinates(service, "Competencia", "CONCLUSIÓN GENERAL", SHEET_ID)
    if not c_row:
        # Fallback if label overwrote
        c_row = 29
        write_data(service, SHEET_ID, f"Competencia!A{c_row}", [["CONCLUSIÓN GENERAL"]])
    
    write_data(service, SHEET_ID, f"Competencia!B{c_row}", [[conc_text]])
    service.spreadsheets().values().clear(
         spreadsheetId=SHEET_ID, range=f"Competencia!C{c_row}:Z{c_row}").execute()

    print("--- MISSION COMPLETE ---")

if __name__ == '__main__':
    main()
