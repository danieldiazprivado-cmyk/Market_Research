import os
import time
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# --- CONFIGURATION (MAPs MODE) ---
CREDENTIALS_FILE = 'credentials.json'
SHEET_ID = "1ZiaahbrXOhEJMn7PkmdA7LrdhRUmVfegnZr-Or6tVyY"
SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/spreadsheets'
]

def authenticate():
    """Authenticates using service account credentials."""
    creds = None
    if os.path.exists(CREDENTIALS_FILE):
        creds = service_account.Credentials.from_service_account_file(
            CREDENTIALS_FILE, scopes=SCOPES)
    else:
        raise FileNotFoundError(f"Credentials file {CREDENTIALS_FILE} not found.")
    return creds

def write_data(service_sheets, spreadsheet_id, range_name, values):
    """Writes data to a specific range without clearing (Preserve Design)."""
    try:
        body = {
            'values': values
        }
        service_sheets.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id, range=range_name,
            valueInputOption='USER_ENTERED', body=body).execute()
        # Count cells written
        count = sum(len(row) for row in values)
        print(f"Data written to {range_name}. ({count} cells)")
    except HttpError as error:
        print(f"An error occurred writing to {range_name}: {error}")

def find_cell_coordinates(service, sheet_name, search_text, spreadsheet_id):
    """Finds the A1 notation coordinates of a cell containing search_text."""
    try:
        # Read a large range to scan
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id, range=f"'{sheet_name}'!A1:H50").execute()
        rows = result.get('values', [])
        
        for r_idx, row in enumerate(rows):
            for c_idx, cell in enumerate(row):
                if search_text.upper() in str(cell).upper(): # Loose match for convenience
                    # Convert to A1 notation
                    col_letter = chr(65 + c_idx)
                    row_num = r_idx + 1
                    return col_letter, row_num
        return None, None
    except Exception as e:
        print(f"Error finding '{search_text}': {e}")
        return None, None

def main():
    creds = authenticate()
    service_sheets = build('sheets', 'v4', credentials=creds)
    print("--- STARTING MAGIC EXPLORERS PROTOCOL (MARKET RESEARCH) ---")

    # Wrapper for cleaner calls
    def find_coords(sheet, text):
        return find_cell_coordinates(service_sheets, sheet, text, SHEET_ID)

    # --- COMPETITOR DATA DICTIONARY (MAPs) ---
    competitor_data_map = {
        "Name": ["KiwiCo", "Lovevery", "Mel Science", "Marvin's Magic", "Little Passports"],
        "Social Media": ["@kiwico_inc", "@lovevery", "@melscience", "@marvinsmagic", "@littlepassports"],
        "Product": ["Monthly STEAM Boxes", "Development Kits (Play Kits)", "Chemistry/Physics VR Experiments", "Trick Sets (Pranks)", "Global Adventure Kits"],
        "Link": ["kiwico.com", "lovevery.com", "melscience.com", "marvinsmagic.com", "littlepassports.com"],
        "Hook": ["'Innovation for future leaders'.", "'Purposeful play for every stage'.", "'Real science, not just toys'.", "'Professional tricks made easy'.", "'The world in your mailbox'."],
        "Main Marketing Promise": ["Inspire young creativity with hands-on projects.", "Support precise brain development by age.", "Make science education cool and profound.", "Become the soul of the party now.", "Waken the child's global curiosity."],
        "Unique mechanism": ["'Maker' Projects (Do it yourself).", "Neuroscience applied to toy design.", "Combines physical + Virtual Reality (app).", "Visual tricks of immediate impact.", "Travel narrative (Suitcase, Passport)."],
        "Unique selling proposition": ["The largest library of STEAM projects.", "Premium wood/safety aesthetics.", "Immersive laboratory experience.", "Legacy of professional magic simplified.", "Geography + Cultural fun."],
        "General marketing statements": ["Serious learning that feels like play.", "Give your child the best start possible.", "Safe and explosive experiments at home.", "Magic recommended by real magicians.", "Travel the world without leaving home."],
        "Evidence": ["Millions of boxes sent, massive reviews.", "Experts/Doctors on the design team.", "Viral videos of chemical reactions.", "Sold in top toy stores (Hamleys).", "Education awards (Parents' Choice)."],
        "Statement of benefits": ["Kids building, not consuming screens.", "Peace of mind that they are playing with 'the right thing'.", "Deep understanding of complex concepts.", "Instant confidence when surprising others.", "Knowledge of the world and cultural empathy."],
        "Deliverables / Features": ["Monthly box with materials + magazine.", "Montessori toys made of sustainable wood.", "Chemical set + VR Goggles + Mobile App.", "Box with props (cards, wands, etc).", "Initial suitcase + monthly envelopes."],
        "Price and payment terms": ["$$ (Flexible subscription).", "$$$$ (High ticket, pay per kit).", "$$$ (Expensive due to technology).", "$ (One-time purchase, variable).", "$$ (Standard subscription)."],
        "Bonus that includes": ["Kiwi magazine and extra DIY videos.", "Detailed guides for parents.", "Live classes with scientists.", "Secret online video tutorials.", "Access to online games in their zone."],
        "Risk reversal / Guarantees": ["Cancel anytime.", "Guaranteed safe/non-toxic materials.", "Try it, experimental safety.", "Wonder guarantee.", "Easy cancellation."],
        "Additional observations": ["Giant leader, but sometimes 'industrial'.", "Very rigid in ages, little fantasy.", "Very focused on screens/apps (Digital).", "Focus on 'Trickster' (Prank) vs Values.", "More passive reading/activity than active."]
    }
    
    # --- PRODUCER / PRODUCT DATA (MAPs) ---
    product_name_text = "MAPs (Magic Activity Packs) by Magic Explorers"
    
    product_producer_text = "Magic Explorers is a unique organization founded by Professional Magicians and Educators. Their mission is not to create 'stage magicians', but to use the fascinating art of magic as a vehicle for human development (Social Emotional Learning - SEL). Unlike traditional magic kits that focus on the 'trick' or 'deception', Magic Explorers focuses on the learning PROCESS, using magic to teach the '3 Keys of Magic': Make it Fun, Think of Others, and Give your Best."
    product_producer = [[product_producer_text]]
    
    product_history_text = "Born from award-winning face-to-face programs (camps, after-school), Magic Explorers saw the need to bring this transformative experience home. Children spent too much time on screens (passive consumption). The founders designed the MAPs as a 'hybrid' solution: high-quality physical materials to build and manipulate, backed by a values structure. It's not a toy, it's an 'Adventure in a box' that turns parents into heroes and children into confident presenters."
    product_history = [[product_history_text]]
    
    product_keywords_str = "magic activity packs, kids magic tricks, social emotional learning kits, screen free activities for kids, confidence building games, steam magic box, educational magic set, empathy games for children, magic explorers maps, grit and resilience activities"
    product_keywords = [[product_keywords_str]]

    product_ingredients_full = [
        ["The 3 Keys of Magic", "Values System.", "Teaches Empathy (Think of others) and Resilience (Give your best).", "The child doesn't just learn a trick, they learn to be a better person."],
        ["'No-Digital' Focus", "Active Disconnection.", "Physical manipulation of objects, cards, and art.", "Real break from screen overstimulation."],
        ["Step-by-Step Scripts", "Communication Structure.", "Pre-written scripts so the child knows what to say.", "Eliminates stage fright by giving them the exact words."],
        ["Artistic Component (Craft)", "Personalization.", "The child colors, cuts, or assembles their own tricks.", "Sense of belonging: 'I made this magic'."],
        ["Secret Videos", "Hybrid Support.", "Video tutorials only accessible with a password.", "Sense of exclusivity and belonging to a club."],
        ["Process Focus", "Growth Mindset.", "Practice is rewarded, not just the final result.", "Teaches that effort brings rewards (Grit)."],
        ["Inclusiveness", "Universal Design.", "Tricks designed for small hands and diverse abilities.", "Any child can be the star, without high technical barriers."],
        ["Paper/Cardboard Materials", "Sustainability/Simplicity.", "Less cheap plastic, more tactile creativity.", "Feels like an art project with a magical ending."]
    ]
    
    # Prepare Columns
    ingredients_A = [[item[0]] for item in product_ingredients_full]
    ingredients_C = [[item[2]] for item in product_ingredients_full]
    ingredients_E = [[item[3]] for item in product_ingredients_full]

    # --- EXECUTION ---

    print("--- 1. POPULATING PRODUCT TAB (MAPs) ---")
    
    # A. Product Name
    n_col, n_row = find_coords("Product", "Product/Service Name")
    if n_col and n_row:
        write_data(service_sheets, SHEET_ID, f"Product!{n_col}{n_row + 1}", [[product_name_text]])

    # B. Producer Info
    p_col, p_row = find_coords("Product", "Producer Information")
    if p_col and p_row:
        write_data(service_sheets, SHEET_ID, f"Product!{p_col}{p_row + 1}", product_producer)

    # C. History
    h_col, h_row = find_coords("Product", "Product/Service History")
    if h_col and h_row:
        write_data(service_sheets, SHEET_ID, f"Product!{h_col}{h_row + 1}", product_history)

    # D. Keywords
    k_col, k_row = find_coords("Product", "Product Keywords")
    if k_col and k_row:
        write_data(service_sheets, SHEET_ID, f"Product!{k_col}{k_row + 1}", product_keywords)

    # E. Ingredients Table
    feat_col, feat_row = find_coords("Product", "Features")
    if feat_col and feat_row:
        write_data(service_sheets, SHEET_ID, f"Product!{feat_col}{feat_row + 1}", ingredients_A)

    ben_col, ben_row = find_coords("Product", "Benefits")
    if ben_col and ben_row:
        write_data(service_sheets, SHEET_ID, f"Product!{ben_col}{ben_row + 1}", ingredients_C)

    mean_col, mean_row = find_coords("Product", "MEANING")
    if mean_col and mean_row:
        write_data(service_sheets, SHEET_ID, f"Product!{mean_col}{mean_row + 1}", ingredients_E)

    print("--- 2. POPULATING COMPETITORS TAB (MAPs) ---")
    
    # NEW CONTIGUOUS MAPPING (C, D, E, F, G)
    target_cols = ['C', 'D', 'E', 'F', 'G']

    for header_key, values_list in competitor_data_map.items():
        col_found, row_found = find_coords("Competitors", header_key)
        if col_found and row_found:
            print(f"Aligning '{header_key}' at Row {row_found}")
            for i, val in enumerate(values_list):
                if i < len(target_cols):
                    write_data(service_sheets, SHEET_ID, f"Competitors!{target_cols[i]}{row_found}", [[val]])
                    time.sleep(0.2) 
        else:
             print(f"WARNING: '{header_key}' row not found.")

    print("--- 3. WRITING ANALYSIS (INSIDE BOXES) ---")
    
    # PES
    pes_items = [
        ("PROBLEM (Market Gaps)", "The market offers two extremes: passive plastic toys (quick trash) or hard-skills educational kits (Science/Engineering) that can feel like homework. The fun 'soft skill' is missing: Empathy, Confidence, and Communication."),
        ("ENEMY", "Digital 'Zombie-fication'. Children isolated on tablets, consuming content passively, losing the ability to interact face-to-face and handle the frustration of the real world."),
        ("SOLUTION", "MAPs uses MAGIC not as an end, but as a medium. It's a 'Trojan Horse' of fun that delivers critical life skills (Grit, Empathy) without the child realizing they are learning.")
    ]
    
    # Assuming the boxes are around Row 24
    pes_col, pes_row = find_coords("Competitors", "PROBLEM (Market Gaps)")
    start_pes_row = pes_row if pes_row else 24

    for i, (label, text) in enumerate(pes_items):
        curr = start_pes_row + i * 2 # They seem to be alternating rows or taking 2 rows based on previous sheet audit
        # Wait, let me check the sheet audit row numbers.
        # Row 24: PROBLEM
        # Row 26: ENEMY
        # Row 27: SOLUCIÓN (Spanish in template? I'll use it if find_coords works)
        pass

    # Actually, I'll just hardcode row writes based on the check_headers output
    # Row 24: PROBLEM (Market Gaps)
    # Row 26: ENEMY
    # Row 27: SOLUTION
    # Row 29: GENERAL CONCLUSION

    write_data(service_sheets, SHEET_ID, "Competitors!B24", [[pes_items[0][1]]])
    write_data(service_sheets, SHEET_ID, "Competitors!B26", [[pes_items[1][1]]])
    write_data(service_sheets, SHEET_ID, "Competitors!B27", [[pes_items[2][1]]])

    # Conclusion
    conc_text = "While KiwiCo and Lovevery dominate the hardware (toy/material) and Mel Science hard knowledge, Magic Explorers conquers the HUMAN SOFTWARE (Character). We win by becoming the most fun parent-child 'connection' tool, promising not a smarter child, but a HAPPIER and more CONFIDENT child."
    
    write_data(service_sheets, SHEET_ID, "Competitors!B29", [[conc_text]])

    print("Cleaning 10s for Quota recovery...")
    time.sleep(10)
    print("--- 4. NUCLEAR CLEANUP (PREVENTIVE) ---")
    cleanup_ranges = [
        "Competitors!H1:H100",  # Separator 3
        "Competitors!J1:J100",  # Separator 4
        "Competitors!C24:Z35"   # Floating Text Zone
    ]
    
    try:
        service_sheets.spreadsheets().values().batchClear(
            spreadsheetId=SHEET_ID,
            body={'ranges': cleanup_ranges}
        ).execute()
        print("Batch Cleanup Executed Successfully.")
    except Exception as e:
        print(f"Cleanup Error: {e}")

    print("--- PROTOCOL FINISHED ---")

if __name__ == '__main__':
    main()
