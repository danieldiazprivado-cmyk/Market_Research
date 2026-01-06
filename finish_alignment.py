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
    print("Sleeping 30s to cool down API quota...")
    time.sleep(30)
    
    creds = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)

    print("--- RESUMING ALIGNMENT (SLOW MODE) ---")
    
    # 1. RESUME COMPETITORS
    target_cols = ['C', 'E', 'G', 'I', 'K']
    separator_cols = ['D', 'F', 'H', 'J']

    # Data Map (Partial - Start from Propuesta)
    resume_map = {
        "Propuesta única de venta": [
            "Creado por dentista para su propia hija. Enfoque clínico puro.",
            "La alternativa ayurvédica auténtica y viral en TikTok.",
            "Sistema de doble botella (se activa al servir para potencia máxima).",
            "Certificado 'Microbiome Safe' + Enfoque en blanqueamiento no tóxico.",
            "Marca lifestyle/moderna visualmente atractiva y accesible en retail."
        ],
        "Afirmaciones generales de marketing": [
            "Dentist Formulated. Clinical Strength.",
            "Voted #1 Oil Pulling. Alcohol Free.",
            "No morning breath. 24 Hour Protection.",
            "Non-Toxic. Whitens without sensitivity.",
            "Naturally friendly. Leaping Bunny Certified."
        ],
        "Pruebas": [
            "Millones de vendidos. Dr. Harold Katz endorsement.",
            "Millones de vistas en TikTok. Testimonios virales.",
            "Patentes tecnológicas. Recomendado por dentistas.",
            "Estudios clínicos de no-toxicidad. 50k+ reseñas.",
            "Certificaciones éticas (Cruelty Free, Vegan) + Retail presence."
        ],
        "Declaración de beneficios": [
            "Confianza clínica de que el mal aliento desaparece.",
            "Salud holística (encías sanas) y dientes blancos.",
            "Seguridad social total 24/7 (elimina 'aliento de mañana').",
            "Belleza (blanqueamiento) sin dolor ni riesgo.",
            "Sentirse 'cool' y responsable con un producto ético."
        ],
        "Entregables / Características": [
            "Botella grande (Enjuague).",
            "Botella con copa medidora (Aceite enjuague).",
            "Sistema Dual-Pour (Dos botellas unidas).",
            "Enjuague Premium (Botella).",
            "Enjuague Standard (Botella estética)."
        ],
        "Precio y términos de pago": [
            "$12 - $15 USD. (Suscripción disponible).",
            "$15 - $18 USD. (Suscripción).",
            "$11 - $14 USD.",
            "$18 - $22 USD. (Premium).",
            "$6 - $9 USD. (Económico)."
        ],
        "Reversión de riesgo / Garantías": [ 
            "Garantía Incondicional (Reembolso completo).",
            "Política de Devolución 30 Días (Compra directa).",
            "Garantía de Satisfacción (Contra gases VSC).",
            "Garantía 'Love the Results' (30 días).",
            "Garantía 'Friendly' (Reemplazo/Reembolso)."
        ],
        "Observaciones adicionales ": [ 
            "Branding médico anticuado. Sabor 'medicine-like'. No lifestyle.",
            "Rutina de 10 minutos (barrera alta). Botella aceitosa/messy.",
            "Sistema Dual-Pour complejo/frágil. No travel-friendly.",
            "Precio Premium ($20+). Requiere uso continuo (lento).",
            "Percibido como genérico/débil. Falta autoridad clínica."
        ]
    }
    
    for header_key, values_list in resume_map.items():
        col_found, row_found = find_cell_coordinates(service, "Competencia", header_key, SHEET_ID)
        if row_found:
            print(f"Aligning '{header_key}' at Row {row_found}")
            # Write Data
            for i, val in enumerate(values_list):
                if i < len(target_cols):
                    write_data(service, SHEET_ID, f"Competencia!{target_cols[i]}{row_found}", [[val]])
                    time.sleep(0.5) # Rate Limit Protection
            # Clear Separators
            for sep in separator_cols:
                service.spreadsheets().values().clear(
                    spreadsheetId=SHEET_ID, range=f"Competencia!{sep}{row_found}"
                ).execute()
                time.sleep(0.5)
        else:
             print(f"WARNING: '{header_key}' row not found.")

    print("--- 2. WRITING ANALYSIS (SLOW MODE) ---")
    time.sleep(2)

    # PES
    pes_items = [
        ("PROBLEMA (Market Gaps)", "El mercado está polarizado entre 'Clínico Aburrido' (TheraBreath, SmartMouth) y 'Natural Lento' (GuruNanda). Falta una solución RÁPIDA, NATURAL y POTENTE."),
        ("ENEMIGO", "El 'Alcohol' (Listerine) ya es villano, pero el nuevo enemigo es el 'Tiempo' (GuruNanda requiere 10 mins) y la 'Química Agresiva' (incluso en marcas clínicas)."),
        ("SOLUCIÓN", "Un SERUM concentrado (Potencia Clínica) que funciona en segundos (Rapidez), con ingredientes botánicos (Seguridad Natural). El 'Bio-Hack' perfecto para el aliento.")
    ]
    
    # We assume PES header is at Row 24 (A24=Análisis P.E.S).
    # We write to 25, 26, 27.
    start_pes_row = 25
    for i, (label, text) in enumerate(pes_items):
        curr = start_pes_row + i
        write_data(service, SHEET_ID, f"Competencia!A{curr}", [[label]])
        time.sleep(0.5)
        write_data(service, SHEET_ID, f"Competencia!B{curr}", [[text]])
        time.sleep(0.5)
        service.spreadsheets().values().clear(
            spreadsheetId=SHEET_ID, range=f"Competencia!C{curr}:Z{curr}"
        ).execute()

    time.sleep(1)

    # Conclusion
    conc_row = 29
    conc_text = "Breatify domina el 'Blue Ocean' entre la eficacia clínica de TheraBreath y la deseabilidad natural de GuruNanda. La estrategia es: 'Potencia de Dentista, Alma Botánica, Velocidad del Rayo'."
    
    write_data(service, SHEET_ID, f"Competencia!A{conc_row}", [["CONCLUSIÓN GENERAL"]])
    time.sleep(0.5)
    write_data(service, SHEET_ID, f"Competencia!B{conc_row}", [[conc_text]])
    time.sleep(0.5)
    service.spreadsheets().values().clear(
        spreadsheetId=SHEET_ID, range=f"Competencia!C{conc_row}:Z{conc_row}"
    ).execute()
    
    print("--- JOB DONE ---")

if __name__ == '__main__':
    main()
