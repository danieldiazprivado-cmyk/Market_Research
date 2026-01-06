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
    print("--- WRITING VOICE-OF-CUSTOMER MATRIX (MAPs) ---")
    
    # 10 CURRENT ANGLES (Market)
    current_market_data = [
        {
            "angle": "Screen-Free Detox",
            "unaware": "I notice my child gets more irritable after being on the tablet, but it's the only thing that entertains them.",
            "problem": "I'm abusing the 'digital babysitter'. I feel guilty seeing them zombified, but I need time for myself.",
            "solution": "I'm looking for something that entertains them JUST LIKE a screen, but without blue light. Something 'addictive' in a good way.",
            "product": "Can MAPs really compete with Fortnite? Won't my child get bored in 5 minutes?",
            "most_aware": "Do you have any trial pack to see if they like it before I subscribe?"
        },
        {
            "angle": "STEM/STEAM Learning",
            "unaware": "School is fine, but I feel something more practical is missing... more creativity.",
            "problem": "My child thinks science and math are boring. They are losing interest in learning.",
            "solution": "I need to disguise learning as play. Something 'maker' where they build and understand the why of things.",
            "product": "How does a card trick teach 'physics'? Is it magic or science explained?",
            "most_aware": "Does it align with the third-grade school curriculum?"
        },
        {
            "angle": "Boredom Buster / Rainy Day",
            "unaware": "I hate rainy days... they get unbearable locked in the house.",
            "problem": "We always end up watching TV because I don't have the energy to invent new games every afternoon.",
            "solution": "I need an 'emergency button' in the pantry. A box I can pull out and guarantee 2 hours of peace.",
            "product": "Do MAPs come ready to use or do I have to get extra materials? (Scissors, glue, etc.)",
            "most_aware": "How long does shipping take if I order today for the rainy weekend?"
        },
        {
            "angle": "Grandparent Gifting",
            "unaware": "I don't know what to give my grandchildren anymore, they have too many plastic toys they don't use.",
            "problem": "I want to be the cool grandma, but I also want them to learn something. I don't want to give trash.",
            "solution": "I'm looking for a meaningful gift, something we can do together when they visit me.",
            "product": "Are the instructions in large print? Is it easy for me to understand and teach it to them?",
            "most_aware": "Can I put a personalized note in the gift box?"
        },
        {
            "angle": "Confidence Building",
            "unaware": "My child is very shy, it's hard for them to raise their hand in class.",
            "problem": "They hide behind my legs when we greet people. I'm worried about their lack of security.",
            "solution": "I don't want therapy, I want something fun that gives them 'small wins' to make them feel capable.",
            "product": "How does magic help with shyness? Won't they be more embarrassed if the trick goes wrong?",
            "most_aware": "Do you have testimonials from other parents with shy children?"
        },
        {
            "angle": "Social Skills",
            "unaware": "They have a hard time making friends at recess, they play alone almost always.",
            "problem": "They don't know how to 'break the ice'. They lack that spark to connect with other children.",
            "solution": "They need a social tool. Something that gives them an excuse to approach and be interesting.",
            "product": "Do the tricks require an audience? Can they use them to impress their classmates on Monday?",
            "most_aware": "Are there tricks to do in a group or are they all individual?"
        },
        {
            "angle": "Montessori / Tactile Play",
            "unaware": "Everything is tactile on smooth screens now... I feel they lose manual dexterity.",
            "problem": "Their handwriting is bad and they struggle to cut. They lack fine motor skills.",
            "solution": "I want real manual activities. Paper, folding, building, manipulating three-dimensional objects.",
            "product": "Are the materials durable? My child is a bit rough with their hands.",
            "most_aware": "Do you use sustainable/recyclable materials or is it a lot of plastic?"
        },
        {
            "angle": "Subscription Convenience",
            "unaware": "I forget to buy activities and end up improvising poorly.",
            "problem": "The mental load of 'entertaining the kids' exhausts me. I want to delegate that.",
            "solution": "I want a magic box to arrive every month and I don't have to think about anything. Automate the fun.",
            "product": "Is it easy to cancel if we go on vacation? Do the boxes pile up?",
            "most_aware": "Is it cheaper if I pay the full year in advance?"
        },
        {
            "angle": "Art & Creativity",
            "unaware": "They like to draw, but get frustrated if it's not perfect.",
            "problem": "They think they are 'not creative' because they don't draw well. They need to see creativity in another way.",
            "solution": "I'm looking for projects where art has a use. Decoration of their own wand or painting their cards.",
            "product": "Do MAPs include the colors/crayons or just the templates?",
            "most_aware": "Is there an option to buy refills for the art consumables?"
        },
        {
            "angle": "Easy Parenting",
            "unaware": "I come home dead from work and I just want to rest, not play pirates.",
            "problem": "I feel like a bad parent for not playing with them, but I'm exhausted.",
            "solution": "I need a 'script'. Something that tells me what to do and say to connect with them in 15 mins effortlessly.",
            "product": "Are the explanatory videos for the child or for me? Can I leave them alone with the box?",
            "most_aware": "Do you have a guide for estimated times per activity?"
        }
    ]

    # 5 NEW DISRUPTIVE ANGLES (MAPs)
    new_disruptive_data = [
        {
            "angle": "Stealth SEL (Empathy)",
            "unaware": "My child is a good kid, but sometimes they are a bit selfish, they don't think about how others feel.",
            "problem": "It's hard to teach 'empathy' with sermons. It goes in one ear and out the other.",
            "solution": "I need a game where 'thinking about the other' is the only way to win. Practical empathy, not theoretical.",
            "product": "How does a magic trick teach empathy? (Ah, you have to see from the audience's perspective?)",
            "most_aware": "Is this endorsed by child psychologists?"
        },
        {
            "angle": "The Grit Gym (Resilience)",
            "unaware": "As soon as something doesn't work out at first, they throw the toy and cry. They have zero tolerance for frustration.",
            "problem": "I'm afraid they'll grow up giving up in the face of any difficulty.",
            "solution": "I need a safe 'Frustration Gym'. Where failing is a fun part of the process.",
            "product": "Are the tricks hard? Will they get more frustrated or does the system help them keep trying?",
            "most_aware": "Are there progressive difficulty levels in the boxes?"
        },
        {
            "angle": "Service Magic (Giving)",
            "unaware": "They always ask: 'buy me, give me, I want'. I feel we are raising consumers.",
            "problem": "I want them to experience the joy of GIVING, not just receiving.",
            "solution": "I'm looking for an activity where the final goal is to give an experience or a moment to someone else.",
            "product": "Is the focus 'deceiving' people or 'making them smile'? I like the service approach.",
            "most_aware": "Do you have any activity where the child prepares a show for the family?"
        },
        {
            "angle": "Structured Bonding",
            "unaware": "I want to connect with my child, but sometimes we have nothing to talk about. There are awkward silences.",
            "problem": "Our relationship is becoming transactional: 'do your homework, brush your teeth'.",
            "solution": "I need a shared project. Something where we are partners, with a common fun goal.",
            "product": "Is it a solitary activity or does it require mom/dad? (I'm looking for the latter).",
            "most_aware": "Are there defined roles for the parent and the child in the instructions?"
        },
        {
            "angle": "The Anti-Zombie Cure",
            "unaware": "Their eyes look glassy when they watch YouTube. It's as if their brain turns off.",
            "problem": "It scares me the long-term effect of so much mental passivity. I need to 'turn on' their brain.",
            "solution": "I need 'Active Recall'. That they have to memorize, sequence, and execute complex steps.",
            "product": "Does memorizing the trick steps help with their concentration at school?",
            "most_aware": "Do you have studies on attention improvement with this method?"
        }
    ]

    # COMBINE ALL DATA
    all_angles = current_market_data + new_disruptive_data
    start_row = 4
    
    print(f"Preparing data for 15 rows of VoC Matrix...")
    
    batch_values = []
    for data in all_angles:
        # Each row is [Angle, Most Aware, Product, Solution, Problem, Unaware]
        row = [
            data['angle'],
            data['most_aware'],
            data['product'],
            data['solution'],
            data['problem'],
            data['unaware']
        ]
        batch_values.append(row)
        
    print("Writing Batch Data to Awareness Levels sheet...")
    service.spreadsheets().values().update(
        spreadsheetId=SHEET_ID, 
        range=f"'Awareness Levels'!A{start_row}", 
        valueInputOption='USER_ENTERED', 
        body={'values': batch_values}
    ).execute()

    print("--- VoC MATRIX WRITTEN SUCCESSFULLY (BATCH) ---")

if __name__ == '__main__':
    main()
