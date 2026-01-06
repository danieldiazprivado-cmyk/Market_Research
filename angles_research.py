import time
from google.oauth2 import service_account
from googleapiclient.discovery import build

CREDENTIALS_FILE = 'credentials.json'
SHEET_ID = "1ZiaahbrXOhEJMn7PkmdA7LrdhRUmVfegnZr-Or6tVyY"
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def authenticate():
    creds = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE, scopes=SCOPES)
    return creds

def main():
    service = build('sheets', 'v4', credentials=authenticate())
    print("--- WRITING SALES ANGLES (MAGIC EXPLORERS) ---")

    # 1. 10 MARKET ANGLES (MAPs)
    current_angles = [
        "Screen-Free Detox",
        "STEM/STEAM Learning",
        "Boredom Buster / Rainy Day",
        "Grandparent Gifting",
        "Confidence Building",
        "Social Skills",
        "Montessori / Tactile Play",
        "Subscription Convenience",
        "Art & Creativity",
        "Easy Parenting / 'Done for You'"
    ]
    
    print("Writing 10 Market Angles from A6...")
    for i, angle in enumerate(current_angles):
        row = 6 + i
        service.spreadsheets().values().update(
            spreadsheetId=SHEET_ID, range=f"'Sales Angles'!A{row}", 
            valueInputOption='USER_ENTERED', body={'values': [[angle]]}
        ).execute()
        time.sleep(0.3)

    # 2. 5 NEW DISRUPTIVE ANGLES (MAPs)
    new_angles = [
        "Stealth SEL: 'Empathy hidden in a magic trick'.",
        "The Grit Gym: 'The only game where failing is necessary'.",
        "Service Magic: 'Tricks to Give vs Deceive'.",
        "Structured Bonding: 'Scripts for parents to be heroes'.",
        "The Anti-Zombie Cure: 'Active cerebral engagement vs passive consumption'."
    ]

    print("Writing 5 Disruptive Angles from A29...")
    for i, angle in enumerate(new_angles):
        row = 29 + i
        try:
            service.spreadsheets().values().update(
                spreadsheetId=SHEET_ID, range=f"'Sales Angles'!A{row}", 
                valueInputOption='USER_ENTERED', body={'values': [[angle]]}
            ).execute()
            time.sleep(2.0) # Increased sleep for safety
        except Exception as e:
            print(f"Error (sleeping 10s): {e}")
            time.sleep(10)
            # Retry once
            service.spreadsheets().values().update(
                spreadsheetId=SHEET_ID, range=f"'Sales Angles'!A{row}", 
                valueInputOption='USER_ENTERED', body={'values': [[angle]]}
            ).execute()

    print("--- SALES ANGLES WRITTEN SUCCESSFULLY ---")

if __name__ == '__main__':
    main()
