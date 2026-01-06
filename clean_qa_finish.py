from google.oauth2 import service_account
from googleapiclient.discovery import build
import time

CREDENTIALS_FILE = 'credentials.json'
SHEET_ID = "1ZiaahbrXOhEJMn7PkmdA7LrdhRUmVfegnZr-Or6tVyY"
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def main():
    print("Sleeping 30s for Quota Safety (Rate Limit Recovery)...")
    time.sleep(30)
    
    creds = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)

    print("--- RESUMING QA CLEANUP (MAGIC EXPLORERS) ---")

    print("Writing Boxed Analysis (Confirmation)...")
    pes_items = [
        ("PROBLEM (Market Gaps)", "The market offers two extremes: Passive plastic toys (quick trash) or 'hard skills' Educational Kits (Science/Engineering) that can feel like homework. The fun 'soft skill' is missing: Empathy, Confidence, and Communication."),
        ("ENEMY", "Digital 'Zombie-fication'. Children isolated on tablets, consuming content passively, losing the ability to interact face-to-face and handle real-world frustration."),
        ("SOLUTION", "MAPs uses MAGIC not as an end, but as a means. It is a fun 'Trojan Horse' that delivers critical life skills (Grit, Empathy) without the child realizing they are learning.")
    ]
    
    # Assuming Row 25 for PES (Standard Template)
    start_r = 25
    for i, (label, text) in enumerate(pes_items):
        r = start_r + i
        service.spreadsheets().values().update(spreadsheetId=SHEET_ID, range=f"Competitors!A{r}", valueInputOption='USER_ENTERED', body={'values': [[label]]}).execute()
        service.spreadsheets().values().update(spreadsheetId=SHEET_ID, range=f"Competitors!B{r}", valueInputOption='USER_ENTERED', body={'values': [[text]]}).execute()

    conc_text = "While KiwiCo and Lovevery dominate hardware (toy/material) and Mel Science dominates hard knowledge, Magic Explorers conquers HUMAN SOFTWARE (Character). We win by becoming the most fun parent-child 'connection' tool, promising not a smarter child, but a HAPPIER and more CONFIDENT child."
    
    service.spreadsheets().values().update(spreadsheetId=SHEET_ID, range=f"Competitors!A29", valueInputOption='USER_ENTERED', body={'values': [['GENERAL CONCLUSION']]}).execute()
    service.spreadsheets().values().update(spreadsheetId=SHEET_ID, range=f"Competitors!B29", valueInputOption='USER_ENTERED', body={'values': [[conc_text]]}).execute()

    # 3. NUCLEAR CLEANUP (Batch Clear)
    print("EXECUTING NUCLEAR BATCH CLEANUP...")
    cleanup_ranges = [
        "Competitors!H1:H100",
        "Competitors!J1:J100",
        "Competitors!C25:Z40" # Clear right of Analysis
    ]
    try:
        service.spreadsheets().values().batchClear(
            spreadsheetId=SHEET_ID,
            body={'ranges': cleanup_ranges}
        ).execute()
        print("Nuclear Clean Complete.")
    except Exception as e:
        print(f"Cleanup Failed: {e}")

if __name__ == '__main__':
    main()
