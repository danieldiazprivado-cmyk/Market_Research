import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import base64
import time

# --- CONFIGURATION ---
SHEET_ID = '1ncuDVNuqAoAYChYdJgHeYX3bXyZdURksqw5SVYVD5z4'
CREDENTIALS_FILE = 'credentials.json'
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="MAPs | Market Research Protocol",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- PREMIUM DARK CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Outfit:wght@300;400;600&display=swap');
    
    /* Reset and Global Styles */
    .stApp {
        background-color: #0d1117 !important;
        color: #e6edf3 !important;
    }
    
    [data-testid="stHeader"] {
        background: rgba(13, 17, 23, 0.8) !important;
        backdrop-filter: blur(10px);
    }

    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    h1, h2, h3, h4 {
        font-family: 'Orbitron', sans-serif;
        color: #58a6ff !important;
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #010409 !important;
        border-right: 1px solid #30363d;
    }
    
    /* Card Component */
    .glass-card {
        background-color: #161b22 !important;
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #30363d;
        margin-bottom: 20px;
        color: #e6edf3;
        box-shadow: 0 4px 20px rgba(0,0,0,0.5);
    }
    
    .card-title {
        color: #58a6ff;
        font-weight: 700;
        font-size: 0.75rem;
        letter-spacing: 1.2px;
        text-transform: uppercase;
        margin-bottom: 12px;
        border-left: 3px solid #58a6ff;
        padding-left: 10px;
    }

    .card-content {
        font-size: 0.95rem;
        line-height: 1.6;
        color: #c9d1d9;
    }

    /* Gradient Header */
    .gradient-header {
        background: linear-gradient(90deg, #58a6ff, #bc8cff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.5rem;
        margin-bottom: 30px;
        font-family: 'Orbitron', sans-serif;
    }

    /* Table/DF Customization */
    .stDataFrame, .stTable {
        background: #161b22 !important;
        border: 1px solid #30363d !important;
        border-radius: 8px !important;
    }

    /* Column Spacing */
    [data-testid="column"] {
        padding: 10px;
    }

    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- AUTH & DATA FETCH ---
@st.cache_resource
def get_gspread_client():
    if "gcp_service_account" in st.secrets:
        creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=SCOPES)
    else:
        creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
    return gspread.authorize(creds)

@st.cache_data(ttl=300)
def fetch_raw_values(sheet_name):
    client = get_gspread_client()
    sh = client.open_by_key(SHEET_ID)
    return sh.worksheet(sheet_name).get_all_values()

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='font-size: 1.1rem; color: #58a6ff;'>💎 RESEARCH PROTOCOL</h2>", unsafe_allow_html=True)
    menu = st.radio(
        "",
        ["🏠 Product", "⚔️ Competitors", "🎯 Sales Angles", "🧠 Awareness", "💎 Differentials", "🛑 Objections", "👥 Cohorts"],
        index=0
    )
    st.divider()
    search_query = st.text_input("🔍 Filter Analysis", placeholder="Type keywords...")

menu_clean = menu.split(" ")[1] if " " in menu else menu

# --- HELPERS ---
def draw_card(title, content, color="#58a6ff"):
    # Ensure content is string and not empty
    content_str = str(content) if content else "..."
    st.markdown(f"""
    <div class="glass-card">
        <div class="card-title" style="border-left-color: {color}; color: {color};">{title}</div>
        <div class="card-content">{content_str}</div>
    </div>
    """, unsafe_allow_html=True)

# --- NAVIGATION LOGIC ---
if menu_clean == "Product":
    st.markdown("<div class='gradient-header'>PRODUCT STRATEGY</div>", unsafe_allow_html=True)
    data = fetch_raw_values("Product")
    
    if len(data) > 33:
        # MAPS Data extraction using audit row/col structure
        # Column B is Index 0 (After dropna? No, we used get_all_values, so A=0, B=1, ...)
        # Actually in get_all_values, Column A=0, B=1, C=2, D=3, E=4
        p_name = data[3][1] if len(data[3]) > 1 else "N/A" # Row 4, Col B
        features = data[7][1] if len(data[7]) > 1 else "N/A" # Row 8, Col B
        benefits = data[7][2] if len(data[7]) > 2 else "N/A" # Row 8, Col C
        meaning = data[7][4] if len(data[7]) > 4 else "N/A" # Row 8, Col E
        producer = data[25][1] if len(data[25]) > 1 else "N/A" # Row 26, Col B
        history = data[29][1] if len(data[29]) > 1 else "N/A" # Row 30, Col B
        keywords = data[33][1] if len(data[33]) > 1 else "N/A" # Row 34, Col B

        c1, c2 = st.columns(2, gap="large")
        with c1:
            st.markdown("### 🏢 Core Identity")
            draw_card("Product Name", p_name)
            draw_card("Unique Promise (Features)", features, color="#7ee787")
            draw_card("Main Benefits", benefits, color="#bc8cff")
            draw_card("Brand Meaning", meaning, color="#ff7b72")
        with c2:
            st.markdown("### 📜 Background")
            draw_card("History & Origin", history)
            draw_card("Market Keywords", keywords)
            draw_card("Producer Information", producer)

elif menu_clean == "Competitors":
    st.markdown("<div class='gradient-header'>GLOBAL COMPETITORS</div>", unsafe_allow_html=True)
    data = fetch_raw_values("Competitors")
    
    # Analysis Boxes Row 24(Index 23), 26(25), 27(26), 29(28)
    if len(data) > 28:
        st.markdown("### 🔍 Strategic Gap Analysis")
        col1, col2, col3 = st.columns(3)
        with col1: draw_card("Problem (Market Gaps)", data[23][1] if len(data[23]) > 1 else "...")
        with col2: draw_card("Enemy (Friction)", data[25][1] if len(data[25]) > 1 else "...", color="#ff7b72")
        with col3: draw_card("Solution", data[26][1] if len(data[26]) > 1 else "...", color="#7ee787")
        
        st.markdown("### 🎯 conclusion general")
        draw_card("Market Summary", data[28][1] if len(data[28]) > 1 else "...", color="#bc8cff")

    st.divider()
    st.markdown("### ⚔️ Detailed Benchmarking")
    # Competitor Names in Row 5 (Index 4), Columns C, D, E, F, G (Index 2-6)
    if len(data) > 4:
        comp_names = [data[4][i] for i in range(2, 7) if len(data[4]) > i]
        comp_promises = []
        comp_prices = []
        
        # Row 11: Promise (Index 10), Row 13: Price (Index 12)
        if len(data) > 10: comp_promises = [data[10][i] for i in range(2, 7) if len(data[10]) > i]
        if len(data) > 12: comp_prices = [data[12][i] for i in range(2, 7) if len(data[12]) > i]
        
        cols = st.columns(len(comp_names))
        for i, col in enumerate(cols):
            with col:
                name = comp_names[i] if i < len(comp_names) and comp_names[i] else f"Competitor {i+1}"
                promise = comp_promises[i] if i < len(comp_promises) and comp_promises[i] else "No data"
                price = comp_prices[i] if i < len(comp_prices) and comp_prices[i] else "N/A"
                
                st.markdown(f"""
                <div class="glass-card" style="min-height: 250px; text-align: center; border-top: 3px solid #58a6ff;">
                    <h4 style="color: #58a6ff; margin-bottom: 20px;">{name}</h4>
                    <p style="font-size: 0.75rem; color: #8b949e; margin-bottom: 5px;">PROMISE</p>
                    <p style="font-size: 0.8rem; height: 80px; overflow: hidden; color: #c9d1d9;">{promise}</p>
                    <div style="background: rgba(126, 231, 135, 0.1); padding: 5px; border-radius: 6px; margin-top: 15px;">
                        <span style="color: #7ee787; font-weight: 700; font-size: 0.9rem;">{price}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

elif menu_clean == "Angles":
    st.markdown("<div class='gradient-header'>SALES ANGLES</div>", unsafe_allow_html=True)
    raw_data = fetch_raw_values("Sales Angles")
    df = pd.DataFrame(raw_data)
    t1, t2 = st.tabs(["🏛️ Market Standards", "⚡ Disruptive Angles"])
    with t1: st.dataframe(df.iloc[:10], use_container_width=True)
    with t2: st.dataframe(df.iloc[10:], use_container_width=True)

elif menu_clean == "Awareness":
    st.markdown("<div class='gradient-header'>AWARENESS MATRIX</div>", unsafe_allow_html=True)
    df = pd.DataFrame(fetch_raw_values("Awareness Levels"))
    st.dataframe(df, use_container_width=True)

elif menu_clean == "Objections":
    st.markdown("<div class='gradient-header'>OBJECTIONS MATRIX</div>", unsafe_allow_html=True)
    df = pd.DataFrame(fetch_raw_values("Objections"))
    st.dataframe(df, use_container_width=True)

elif menu_clean == "Cohorts":
    st.markdown("<div class='gradient-header'>TARGET COHORTS</div>", unsafe_allow_html=True)
    data = fetch_raw_values("Cohorts")
    df = pd.DataFrame(data)
    cols = st.columns(3)
    # Mapping columns B, E, H (Index 1, 4, 7)
    for i, col in enumerate(cols):
        with col:
            idx = [1, 4, 7][i]
            # Avatar Name in Row 3 (Index 2)
            title = df.iloc[2, idx] if len(df) > 2 and idx < len(df.columns) else f"Avatar {i+1}"
            st.markdown(f"""
            <div class="glass-card" style="border-top: 4px solid #bc8cff;">
                <h3 style="color: #bc8cff; font-size: 1.1rem; margin-bottom: 15px;">{title}</h3>
                <hr style="border-color: #30363d;">
            </div>
            """, unsafe_allow_html=True)
            # Show the profile data
            st.dataframe(df.iloc[3:, [idx]].dropna(), use_container_width=True)

# --- FOOTER ---
st.divider()
if st.sidebar.button("📥 EXPORT PDF REPORT"):
    st.toast("Generating Research Document...")
    time.sleep(1)
    st.sidebar.success("Ready! (Simulation)")

st.sidebar.markdown("<br><br><br><p style='text-align: center; color: #484f58; font-size: 0.65rem;'>MAPs RESEARCH PROTOCOL V2.5<br>DEVELOPED BY ANTIGRAVITY AI</p>", unsafe_allow_html=True)
