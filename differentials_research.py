import time
from google.oauth2 import service_account
from googleapiclient.discovery import build

CREDENTIALS_FILE = 'credentials.json'
SHEET_ID = "1ZiaahbrXOhEJMn7PkmdA7LrdhRUmVfegnZr-Or6tVyY"
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def authenticate():
    return service_account.Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)

def main():
    service = build('sheets', 'v4', credentials=authenticate())
    print("--- WRITING DIFFERENTIATORS (MAPs) ---")

    # MAPs Differentiators (Vs Market)
    differentiators = [
        ["Factor", "Traditional Market (KiwiCo/Lovevery)", "MAPs (Magic Explorers)", "Why We Win"],
        ["Main Focus", "Hard Skills (STEM, Science, Construction)", "Soft Skills (SEL, Empathy, Confidence)", "Parents value 'Character' more today."],
        ["Child's Role", "Solitary Engineer (Builds alone)", "Connected Showman (Presents to others)", "We promote real human connection."],
        ["Parents' Role", "Passive Supervisor ('Read the manual')", "Active Audience / Accomplice ('Be the hero')", "We give them a fun role, not a teacher's."],
        ["Mechanism", "Physical Materials (Wood/Plastic)", "The 3 Keys of Magic (Values)", "The toy breaks, the values stay."],
        ["Final Result", "An object built on the shelf.", "A performance/show recorded on video.", "We create memories and evidence of growth."],
        ["Sustainability", "A lot of plastic/waste in each kit.", "Focus on paper/cardboard and reuse.", "Less environmental guilt for the parent."],
        ["'Wow' Factor", "The final object (if it turns out well).", "The audience reaction (immediate).", "Instant positive social reinforcement."],
        ["Learning Curve", "Complex engineering instructions.", "Step-by-step performance scripts.", "Less technical frustration, more social success."],
        ["Longevity", "Used once and forgotten.", "The trick can be done for a lifetime.", "Permanent skill vs Temporary toy."]
    ]

    print("Writing Differentiators to Differentials sheet...")
    # Clean area first? No, precise overwrite.
    # Assuming Header at A1 or similar. Let's write block starting A4.
    
    start_row = 5
    print(f"Writing {len(differentiators)} rows of Differentiatiors Batch...")
    
    service.spreadsheets().values().update(
        spreadsheetId=SHEET_ID, 
        range=f"'Differentials'!A{start_row}", 
        valueInputOption='USER_ENTERED', 
        body={'values': differentiators}
    ).execute()

    print("--- DIFFERENTIATORS WRITTEN SUCCESSFULLY (BATCH) ---")

if __name__ == '__main__':
    main()
