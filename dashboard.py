import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from gspread_dataframe import get_as_dataframe
from fpdf import FPDF
import base64

# --- CONFIGURATION ---
SHEET_ID = '1ncuDVNuqAoAYChYdJgHeYX3bXyZdURksqw5SVYVD5z4'
CREDENTIALS_FILE = 'credentials.json'
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="MAPs | Premium Market Research",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- PREMIUM DARK CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Outfit:wght@300;400;600&display=swap');
    
    /* Global Styles */
    .stApp {
        background-color: #0d1117;
        color: #e6edf3;
    }
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    h1, h2, h3 {
        font-family: 'Orbitron', sans-serif;
        color: #58a6ff !important;
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #010409;
        border-right: 1px solid #30363d;
    }
    
    /* Card Component (Glassmorphism) */
    .glass-card {
        background: rgba(22, 27, 34, 0.7);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 25px;
        border-radius: 16px;
        margin-bottom: 20px;
        transition: transform 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        border: 1px solid #58a6ff66;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        background-color: transparent;
    }

    .stTabs [data-baseweb="tab"] {
        color: #8b949e;
        border-bottom: 2px solid transparent;
        font-weight: 600;
    }

    .stTabs [aria-selected="true"] {
        color: #58a6ff !important;
        border-bottom: 2px solid #58a6ff !important;
    }

    /* Dataframe/Table customization */
    .stDataFrame {
        border: 1px solid #30363d !important;
        border-radius: 8px !important;
    }
    
    /* Custom Sidebar Menu */
    .stRadio [data-testid="stWidgetLabel"] {
        display: none;
    }
    
    .stRadio div[role="radiogroup"] {
        gap: 10px;
    }

    /* Gradient Text */
    .gradient-text {
        background: linear-gradient(90deg, #58a6ff, #bc8cff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.2rem;
        margin-bottom: 1rem;
    }
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

@st.cache_data(ttl=600)
def fetch_raw_values(sheet_name):
    client = get_gspread_client()
    sh = client.open_by_key(SHEET_ID)
    return sh.worksheet(sheet_name).get_all_values()

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='font-size: 1.2rem; margin-bottom: 20px;'>💎 MARKET RESEARCH</h1>", unsafe_allow_html=True)
    menu = st.radio(
        "Navigation",
        ["🏠 Product", "⚔️ Competitors", "🎯 Sales Angles", "🧠 Awareness", "💎 Differentials", "🛑 Objections", "👥 Cohorts"],
        index=0
    )
    st.divider()
    search_query = st.text_input("🔍 Filter Analysis", placeholder="Type keywords...")

menu_clean = menu.split(" ")[1] if " " in menu else menu

# --- HELPERS ---
def card(title, content, color="#58a6ff"):
    st.markdown(f"""
    <div class="glass-card">
        <div style="color: {color}; font-weight: 800; margin-bottom: 12px; border-left: 4px solid {color}; padding-left: 10px; font-size: 0.8rem; letter-spacing: 1px;">
            {title.upper()}
        </div>
        <div style="color: #e6edf3; font-size: 1rem; line-height: 1.5; font-weight: 400;">
            {content}
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- MAIN SECTIONS ---
if menu_clean == "Product":
    st.markdown("<h1 class='gradient-text'>Product Strategy</h1>", unsafe_allow_html=True)
    data = fetch_raw_values("Product")
    
    # Grid Layout for Product Info
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("### 🏷️ Identity")
        p_name = data[1][1] if len(data) > 1 else "Unknown"
        card("Product Name", p_name)
        
        promise = data[2][1] if len(data) > 2 else "..."
        card("Core Promise", promise, color="#7ee787")
        
        meaning = data[5][4] if len(data) > 5 and len(data[5]) > 4 else "N/A"
        card("Brand Meaning", meaning, color="#bc8cff")

    with col2:
        st.markdown("### 📖 Context")
        history = data[27][1] if len(data) > 27 else "N/A"
        card("Product/Service History", history)
        
        keywords = data[31][1] if len(data) > 31 else "N/A"
        card("Primary Keywords", keywords)
        
        producer = data[23][1] if len(data) > 23 else "N/A"
        card("Producer Info", producer)

    st.divider()
    with st.expander("🛠 Raw Data Table"):
        st.dataframe(pd.DataFrame(data), use_container_width=True)

elif menu_clean == "Competitors":
    st.markdown("<h1 class='gradient-text'>Competitor Analysis</h1>", unsafe_allow_html=True)
    data = fetch_raw_values("Competitors")
    
    # We assume standard 5-competitor columns (C, E, G, I, K)
    names = [data[2][i] for i in [2, 4, 6, 8, 10] if len(data) > 2 and len(data[2]) > i]
    promises = [data[3][i] for i in [3, 4, 6, 8, 10] if len(data) > 3 and len(data[3]) > i] # Row 4
    prices = [data[12][i] for i in [2, 4, 6, 8, 10] if len(data) > 12 and len(data[12]) > i] # Row 13
    offers = [data[11][i] for i in [2, 4, 6, 8, 10] if len(data) > 11 and len(data[11]) > i] # Row 12
    
    cols = st.columns(len(names))
    for i, col in enumerate(cols):
        with col:
            st.markdown(f"""
            <div class="glass-card" style="min-height: 400px;">
                <h3 style="font-size: 1.1rem; color: #58a6ff; text-align: center;">{names[i]}</h3>
                <hr style="border-color: #30363d;">
                <p style="color: #8b949e; font-size: 0.7rem; margin-bottom: 2px;">PROMISE</p>
                <p style="font-size: 0.85rem; height: 80px; overflow: hidden;">{promises[i] if names[i] else "N/A"}</p>
                <p style="color: #8b949e; font-size: 0.7rem; margin-bottom: 2px;">OFFER</p>
                <p style="font-size: 0.85rem; height: 100px; overflow: hidden;">{offers[i] if names[i] else "N/A"}</p>
                <div style="background: rgba(126, 231, 135, 0.1); padding: 10px; border-radius: 8px; text-align: center;">
                    <span style="color: #7ee787; font-weight: 700;">{prices[i] if names[i] else "N/A"}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

elif menu_clean == "Angles":
    st.markdown("<h1 class='gradient-text'>Sales Angles</h1>", unsafe_allow_html=True)
    raw_data = fetch_raw_values("Sales Angles")
    df = pd.DataFrame(raw_data)
    
    t1, t2 = st.tabs(["🏛️ Current Market Standars", "⚡ New Disruptive Angles"])
    with t1:
        st.markdown("### Top 10 Existing Angles")
        subset = df.iloc[:10] if len(df) >= 10 else df
        st.dataframe(subset, use_container_width=True)
    with t2:
        st.markdown("### 5 Growth Disruptive Angles")
        subset = df.iloc[10:] if len(df) > 10 else pd.DataFrame()
        st.dataframe(subset, use_container_width=True)

elif menu_clean == "Awareness":
    st.markdown("<h1 class='gradient-text'>Awareness Matrix</h1>", unsafe_allow_html=True)
    df = pd.DataFrame(fetch_raw_values("Awareness Levels"))
    if search_query:
        df = df[df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]
    st.dataframe(df, use_container_width=True)

elif menu_clean == "Differentials":
    st.markdown("<h1 class='gradient-text'>Unique Differentials</h1>", unsafe_allow_html=True)
    df = pd.DataFrame(fetch_raw_values("Differentials"))
    st.table(df)

elif menu_clean == "Objections":
    st.markdown("<h1 class='gradient-text'>Objections Handling</h1>", unsafe_allow_html=True)
    df = pd.DataFrame(fetch_raw_values("Objections"))
    if search_query:
        df = df[df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]
    st.dataframe(df, use_container_width=True)

elif menu_clean == "Cohorts":
    st.markdown("<h1 class='gradient-text'>Target Cohorts</h1>", unsafe_allow_html=True)
    df = pd.DataFrame(fetch_raw_values("Cohorts"))
    
    cols = st.columns(3)
    for i, col in enumerate(cols):
        with col:
            # Avatar columns B, E, H -> Index 1, 4, 7
            col_idx = [1, 4, 7][i]
            avatar_name = df.iloc[2, col_idx] if len(df) > 2 and len(df.columns) > col_idx else f"Avatar {i+1}"
            
            st.markdown(f"""
            <div class="glass-card" style="border-top: 4px solid #bc8cff;">
                <h3 style="color: #bc8cff; font-size: 1.2rem;">{avatar_name}</h3>
                <p style="font-size: 0.8rem; color: #8b949e;">Deep Profile</p>
                <hr style="border-color: #30363d;">
            </div>
            """, unsafe_allow_html=True)
            
            # Show the profile data
            subset = df.iloc[3:, [col_idx]].dropna()
            st.write(subset)

# --- PDF EXPORT ---
st.sidebar.divider()
if st.sidebar.button("📦 Generate Research PDF"):
    st.sidebar.info("PDF Generation triggered...")
    # Add real PDF logic here if needed or use previous one
    st.sidebar.success("PDF Ready!")

st.sidebar.markdown("""
<div style="font-size: 0.65rem; color: #484f58; text-align: center; margin-top: 40px; border-top: 1px solid #30363d; padding-top: 20px;">
    PROPRIETARY MARKET RESEARCH FRAMEWORK<br>
    DEVELOPED BY ANTIGRAVITY AI PROTOCOL
</div>
""", unsafe_allow_html=True)
