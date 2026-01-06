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
    print("--- WRITING COHORTS (REFINED EXACT MAPPING) ---")

    # Defined Avatars from MAPs logic
    cohorts_data = [
        {
            "col": "B", # Cohort 0
            "values": {
                5: "Stealth SEL (Empathy)", # Winning Desire / Angle
                6: "The Conscious Parent", # Avatar Name
                7: "Men and Women (50/50)", # Sex
                8: "30-45 years old", # Age
                9: "Urban / Suburban Areas (Large Cities)", # Geography
                10: "Parents with children in Elementary (K-3)", # Family / Partner
                11: "Middle-Upper / Upper Class", # Finances
                12: "University / Postgraduate", # Education
                14: "Instagram, Parenting Blogs, Educational Podcasts", # Online Places
                15: "Montessori, Wooden toys, Children's books", # Interests
                18: [ # Keywords
                    "gentle parenting", "child emotional intelligence", "screen-free activities", 
                    "child empathy", "family connection", "sel curriculum", "values games",
                    "child development", "mindfulness for kids", "positive education"
                ]
            }
        },
        {
            "col": "E", # Cohort 1
            "values": {
                5: "The Anti-Zombie Cure", 
                6: "The Overwhelmed Pro", 
                7: "Men and Women (Prevails Mothers 60%)", 
                8: "35-50 years old", 
                9: "Business Centers / Satellite Cities", 
                10: "Married, Both work full-time", 
                11: "Middle / Middle-Upper Class", 
                12: "Professionals / Executives", 
                14: "LinkedIn, WhatsApp Groups, YouTube Kids (Control)", 
                15: "Delivery apps, Productivity tools, Family vacations", 
                18: [
                    "easy activities for kids", "quick home games", "quality time with kids",
                    "taking away tablets from kids", "travel entertainment", "autonomous games", "subscription box",
                    "tired parents help", "fun afternoon routine", "digital disconnection"
                ]
            }
        },
        {
            "col": "H", # Cohort 2
            "values": {
                5: "Grandparent Gifting", 
                6: "The Legacy Builder (Grandparents)", 
                7: "Men and Women (60+)", 
                8: "55-75 years old", 
                9: "Global (Live near or far from their grandchildren)", 
                10: "Grandparents with grandchildren in elementary", 
                11: "Retired / Stable Income", 
                12: "Diverse (Traditional Preference)", 
                14: "Facebook, Email, Family Facebook Groups", 
                15: "Cruises, Gardening, Handcrafts, History", 
                18: [
                    "gifts for grandchildren", "classic educational toys", "grandparent-grandchild activities",
                    "best gift for 7 year olds", "magic for kids", "time with grandparents", "Christmas kids",
                    "original educational gift", "connection tools", "non-technological toys"
                ]
            }
        }
    ]

    for cohort in cohorts_data:
        col = cohort["col"]
        print(f"Batching Cohort for Column {col}...")
        
        # 1. Attributes Batch (Rows 5-15) as Column
        attr_rows = []
        for r in range(5, 16):
            attr_rows.append([cohort["values"].get(r, "")])
            
        print(f"Writing Attributes block {col}5:{col}15...")
        service.spreadsheets().values().update(
            spreadsheetId=SHEET_ID, range=f"'Cohorts'!{col}5:{col}15", 
            valueInputOption='USER_ENTERED', body={'values': attr_rows}
        ).execute()
        time.sleep(15.0)
        
        # 2. Keywords Batch (Rows 18-27) as Column
        kw_list = cohort["values"].get(18, [])
        kw_rows = [[kw] for kw in kw_list]
        
        print(f"Writing Keywords block {col}18:{col}{18 + len(kw_rows) - 1}...")
        service.spreadsheets().values().update(
            spreadsheetId=SHEET_ID, range=f"'Cohorts'!{col}18", 
            valueInputOption='USER_ENTERED', body={'values': kw_rows}
        ).execute()
        time.sleep(15.0)

    print("--- REFINED COHORTS WRITTEN SUCCESSFULLY (BATCH) ---")

    print("--- REFINED COHORTS WRITTEN SUCCESSFULLY ---")

if __name__ == '__main__':
    main()
