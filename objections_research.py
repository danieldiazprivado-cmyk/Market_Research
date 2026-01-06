import time
from google.oauth2 import service_account
from googleapiclient.discovery import build

CREDENTIALS_FILE = 'credentials.json'
SHEET_ID = "1ZiaahbrXOhEJMn7PkmdA7LrdhRUmVfegnZr-Or6tVyY"
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def authenticate():
    return service_account.Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)

def get_deep_objections(angle_name, level_index):
    """
    Returns a string containing 5 bulleted objections for a specific angle and awareness level.
    level_index: 0 (Unaware) to 4 (Most Aware)
    """
    
    # Base templates to diversify content programmatically
    themes = {
        "Screen-Free": "digital disconnection, tablets, screen addiction, physical play, digital tantrums",
        "STEM": "learning, science, school, boring, homework, experiment",
        "Boredom": "boredom, entertainment, home, rain, free time",
        "Grandparent": "gift, grandchildren, grandparents, connection, technology, toy",
        "Confidence": "shyness, security, fear, victory, self-esteem, show",
        "Social": "friends, shyness, school, socialize, interact",
        "Montessori": "fantasy, materials, wood, autonomy, sustainability",
        "Subscription": "cancel, monthly, cost, card, recurrence",
        "Art": "creativity, drawing, painting, material, handcraft",
        "Easy": "time, fatigue, parents, easy, autonomy",
        "Stealth": "empathy, SEL, psychology, character, sharing",
        "Grit": "frustration, crying, giving up, difficulty, resilience",
        "Service": "give, gift, selfishness, sharing, family",
        "Bonding": "connect, relationship, parents and children, script, play together",
        "Zombie": "attention, concentration, memory, digital, brain"
    }
    
    # Default theme if not found
    theme_keywords = themes.get(next((k for k in themes if k in angle_name), "Generic"), "magic, learning, fun, children, parents")
    kw = [s.strip() for s in theme_keywords.split(",")]

    # Logic per level (0 to 4)
    if level_index == 0: # Unaware
        objs = [
            f"Why does my child need something about {kw[0]}? They look happy with their tablet.",
            f"I don't think {kw[1]} is a real problem in my house.",
            "They already have too many toys, another one will just take up space.",
            f"{kw[2].capitalize()} is not something I'm worried about right now.",
            " I'd rather they rest after school instead of doing activities."
        ]
    elif level_index == 1: # Problem Aware
        objs = [
            f"I know {kw[0]} is a problem, but I'm afraid to try and have it not work.",
            f"I feel guilty about their {kw[1]}, but I don't have better alternatives.",
            "I'm worried they'll get frustrated if the game requires too much effort.",
            f"I've noticed their {kw[2]} is getting worse, but I don't know how to help.",
            "I'm too lazy to start something new that ends up as another discarded toy."
        ]
    elif level_index == 2: # Solution Aware
        objs = [
            f"Why choose magic for {kw[0]} instead of painting classes or sports?",
            f"I've seen other {kw[1]} kits, but this one seems different... will it be better?",
            f"It sounds to me like {kw[2]} is just an excuse to sell me smoke.",
            "I'm looking for something that really has an impact on their development, not just laughs.",
            "Is this the best solution for their age or is there something more suitable?"
        ]
    elif level_index == 3: # Product Aware
        objs = [
            f"Does the price of MAPs justify its focus on {kw[0]}?",
            f"What if my child already knows some of these {kw[1]} tricks?",
            f"I'm worried the {kw[2]} materials are of poor quality.",
            "Am I really going to be able to cancel the subscription without complications?",
            "Is there technical support or videos if we get stuck on a step?"
        ]
    else: # 4: Most Aware
        objs = [
            "Do you have any discount for buying the annual package today?",
            "Will it arrive for my child's birthday this Saturday?",
            "Can I pay with PayPal or just credit card?",
            "Do you sell individual boxes to try before committing?",
            "How do I contact support if a piece is missing in my kit?"
        ]

    # Return as bulleted list
    return "\n".join([f"• {o}" for o in objs])

def main():
    service = build('sheets', 'v4', credentials=authenticate())
    print("--- WRITING DEEP 15x5 OBJECTIONS MATRIX (5 BULLETS) ---")
    
    angles = [
        "Screen-Free Detox", "STEM/STEAM Learning", "Boredom Buster", "Grandparent Gifting", "Confidence Building",
        "Social Skills", "Montessori / Tactile", "Subscription Convenience", "Art & Creativity", "Easy Parenting",
        "Stealth SEL (Empathy)", "The Grit Gym (Resilience)", "Service Magic (Giving)", "Structured Bonding", "The Anti-Zombie Cure"
    ]
    
    # 1. Write Headers Row 3
    header_row = [""] + angles
    service.spreadsheets().values().update(
        spreadsheetId=SHEET_ID, range=f"'Objections'!A3", 
        valueInputOption='USER_ENTERED', body={'values': [header_row]}
    ).execute()
    
    # 2. Sequential Write for Quota Safety
    levels_rows = [5, 6, 7, 8, 9] # Shifted up per user request
    
    for l_idx, row_num in enumerate(levels_rows):
        print(f"Generating Data for Level {l_idx + 1} (Row {row_num})...")
        row_data = [] # Data for Cols B-P
        for angle in angles:
            cell_content = get_deep_objections(angle, l_idx)
            row_data.append(cell_content)
            
        print(f"Writing Row {row_num} (15 columns)...")
        service.spreadsheets().values().update(
            spreadsheetId=SHEET_ID, range=f"'Objections'!B{row_num}", 
            valueInputOption='USER_ENTERED', body={'values': [row_data]}
        ).execute()
        time.sleep(10.0) # High safety for batch writes

    # 3. Cleanup Row 10 (which contained legacy shifted data)
    print("Cleaning legacy Row 10...")
    service.spreadsheets().values().clear(
        spreadsheetId=SHEET_ID, range="'Objections'!B10:P10"
    ).execute()

    print("--- DEEP MATRIX WRITTEN & SHIFTED SUCCESSFULLY ---")

if __name__ == '__main__':
    main()
