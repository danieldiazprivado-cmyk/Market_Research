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
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Outfit:wght@300;400;600;700&display=swap');
    
    /* Reset and Global Styles */
    .stApp {
        background: radial-gradient(circle at top right, #1b212c, #0d1117) !important;
        color: #e6edf3 !important;
    }
    
    [data-testid="stHeader"] {
        background: rgba(13, 17, 23, 0.4) !important;
        backdrop-filter: blur(12px);
    }

    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    h1, h2, h3, h4 {
        font-family: 'Orbitron', sans-serif;
        text-transform: uppercase;
        letter-spacing: 3px;
        font-weight: 700;
    }

    /* Sidebar - Modern & Elegant */
    [data-testid="stSidebar"] {
        background-color: #010409 !important;
        border-right: 1px solid rgba(48, 54, 61, 0.8);
    }
    
    /* Better Sidebar Radio titles */
    [data-testid="stSidebar"] div[role="radiogroup"] label {
        background: transparent !important;
        border: none !important;
        padding: 10px 15px !important;
        margin: 5px 0 !important;
        border-radius: 8px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }

    [data-testid="stSidebar"] div[role="radiogroup"] label p {
        color: #8b949e !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        letter-spacing: 1px;
    }

    [data-testid="stSidebar"] div[role="radiogroup"] label:hover {
        background: rgba(88, 166, 255, 0.1) !important;
    }

    [data-testid="stSidebar"] div[role="radiogroup"] label:aria-selected="true" p,
    [data-testid="stSidebar"] div[role="radiogroup"] label[data-checked="true"] p {
        color: #58a6ff !important;
        font-weight: 700 !important;
    }

    /* Focus on active item */
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] {
        font-size: 0.8rem !important;
        color: #58a6ff !important;
        text-transform: uppercase;
        margin-bottom: 20px;
    }

    /* Main Content Styling */
    .glass-card {
        background: rgba(22, 27, 34, 0.6) !important;
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        padding: 28px;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        margin-bottom: 24px;
        color: #e6edf3;
        transition: all 0.4s ease;
        box-shadow: 0 8px 32px rgba(0,0,0,0.4);
    }
    
    .glass-card:hover {
        border: 1px solid rgba(88, 166, 255, 0.3);
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.6);
    }

    .feature-header {
        background: linear-gradient(135deg, #238636, #2ea043);
        color: white;
        padding: 12px;
        border-radius: 8px;
        text-align: center;
        font-weight: 700;
        margin-bottom: 20px;
        font-size: 0.85rem;
        letter-spacing: 1.5px;
        box-shadow: 0 4px 12px rgba(35, 134, 54, 0.3);
    }

    .feature-item {
        background: rgba(48, 54, 61, 0.2);
        border: 1px solid rgba(48, 54, 61, 0.5);
        padding: 16px;
        border-radius: 12px;
        margin-bottom: 12px;
        min-height: 90px;
        display: flex;
        align-items: center;
        font-size: 0.9rem;
        color: #c9d1d9;
        transition: border 0.3s ease;
    }

    .feature-item:hover {
        border-color: #58a6ff;
    }

    .card-title {
        color: #58a6ff;
        font-weight: 700;
        font-size: 0.8rem;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 16px;
        border-left: 4px solid #58a6ff;
        padding-left: 12px;
    }

    .card-content {
        font-size: 1rem;
        line-height: 1.7;
        color: #c9d1d9;
        font-weight: 400;
    }

    .gradient-header {
        background: linear-gradient(90deg, #58a6ff, #bc8cff, #58a6ff);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        font-size: 3rem;
        margin-bottom: 40px;
        font-family: 'Orbitron', sans-serif;
        animation: shine 5s linear infinite;
    }

    @keyframes shine {
        to { background-position: 200% center; }
    }

    .stDataFrame {
        background: #161b22 !important;
        border: 1px solid #30363d !important;
        border-radius: 12px !important;
    }

    /* Custom Scrollbar */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: #0d1117; }
    ::-webkit-scrollbar-thumb { background: #30363d; border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: #58a6ff; }
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
    st.markdown("<h4 style='font-size: 1rem; color: #58a6ff; margin-bottom: 25px;'>💎 STRATEGIC PROTOCOL</h4>", unsafe_allow_html=True)
    menu = st.radio("", ["🏠 Product", "⚔️ Competitors", "🎯 Sales Angles", "🧠 Awareness Matrix", "💎 Differentials", "🛑 Objections", "👥 Targeted Cohorts"], index=0)
    st.divider()
    search_query = st.text_input("🔍 Filter Analysis", placeholder="Type keywords...")

menu_clean = menu.split(" ")[1] if " " in menu else menu

# --- HELPERS ---
def draw_card(title, content, color="#58a6ff"):
    content_str = str(content).strip() if content and str(content).strip() else "..."
    st.markdown(f"""
    <div class="glass-card">
        <div class="card-title" style="border-left-color: {color}; color: {color};">{title}</div>
        <div class="card-content">{content_str}</div>
    </div>
    """, unsafe_allow_html=True)

def find_data_under(data, search_text, col_idx=0, offset=1):
    for i, row in enumerate(data):
        if len(row) > col_idx and search_text.lower() in str(row[col_idx]).lower():
            if i + offset < len(data):
                val = data[i+offset][col_idx] if len(data[i+offset]) > col_idx else ""
                return val
    return ""

def find_in_any_col(data, txt, offset_row=0, offset_col=0):
    for i, row in enumerate(data):
        for j, cell in enumerate(row):
            if txt.lower() in str(cell).lower():
                target_row = i + offset_row
                target_col = j + offset_col
                if target_row < len(data) and target_col < len(data[target_row]):
                    return data[target_row][target_col]
    return ""

# --- NAVIGATION LOGIC ---
if menu_clean == "Product":
    st.markdown("<div class='gradient-header'>PRODUCT STRATEGY</div>", unsafe_allow_html=True)
    data = fetch_raw_values("Product")
    
    if data:
        p_name = find_data_under(data, "Product/Service Name", 0, 1)
        st.markdown(f"#### 📍 PRODUCT NAME: <span style='color: #e6edf3;'>{p_name}</span>", unsafe_allow_html=True)
        st.divider()

        st.markdown("### ⚙️ CORE MECHANISM")
        feat_idx = -1
        for i, row in enumerate(data):
            if "Features" in str(row): feat_idx = i; break
        
        if feat_idx != -1:
            col_f, col_b, col_m = st.columns(3, gap="medium")
            with col_f: st.markdown('<div class="feature-header">FEATURES</div>', unsafe_allow_html=True)
            with col_b: st.markdown('<div class="feature-header">BENEFITS</div>', unsafe_allow_html=True)
            with col_m: st.markdown('<div class="feature-header">MEANING</div>', unsafe_allow_html=True)

            for i in range(feat_idx + 1, len(data)):
                row = data[i]
                if not any(row) or "Producer" in str(row[0]): break
                f, b, m = (row[0] if len(row) > 0 else ""), (row[2] if len(row) > 2 else ""), (row[4] if len(row) > 4 else "")
                if f:
                    with col_f: st.markdown(f'<div class="feature-item">{f}</div>', unsafe_allow_html=True)
                    with col_b: st.markdown(f'<div class="feature-item">{b}</div>', unsafe_allow_html=True)
                    with col_m: st.markdown(f'<div class="feature-item">{m}</div>', unsafe_allow_html=True)

        st.divider()
        st.markdown("### 🏷️ STRATEGIC CONTEXT")
        history = find_data_under(data, "Product/Service History", 0, 1)
        keywords = find_data_under(data, "Product Keywords", 0, 1)
        producer = find_data_under(data, "Producer Information", 0, 1)

        c_low1, c_low2 = st.columns(2, gap="large")
        with c_low1: draw_card("History & Origin", history)
        with c_low2:
            draw_card("Producer Information", producer)
            draw_card("Market Keywords", keywords)

elif menu_clean == "Competitors":
    st.markdown("<div class='gradient-header'>GLOBAL COMPETITORS</div>", unsafe_allow_html=True)
    data = fetch_raw_values("Competitors")
    if data:
        st.markdown("### 🔍 STRATEGIC GAP ANALYSIS")
        p, e, s, conc = find_in_any_col(data, "PROBLEM", 0, 1), find_in_any_col(data, "ENEMY", 0, 1), find_in_any_col(data, "SOLUTION", 0, 1), find_in_any_col(data, "CONCLUSION", 0, 1)
        col1, col2, col3 = st.columns(3)
        with col1: draw_card("Problem (Market Gaps)", p)
        with col2: draw_card("Enemy (Friction)", e, color="#ff7b72")
        with col3: draw_card("Solution", s, color="#7ee787")
        draw_card("General Conclusion", conc, color="#bc8cff")

        st.divider()
        st.markdown("### ⚔️ DETAILED BENCHMARKING")
        names_row = -1
        for i, row in enumerate(data):
            if "Competitor 1" in str(row): names_row = i; break
        if names_row != -1:
            cols = st.columns(5)
            for i in range(5):
                with cols[i]:
                    c_idx = i + 2
                    name = data[names_row+1][c_idx] if len(data) > names_row+1 and len(data[names_row+1]) > c_idx else f"Comp {i+1}"
                    promise = find_in_any_col(data, "Main Marketing Promise", 0, c_idx)
                    price = find_in_any_col(data, "Price and payment terms", 0, c_idx)
                    st.markdown(f"""
                    <div class="glass-card" style="min-height: 280px; text-align: center; border-bottom: 4px solid #58a6ff;">
                        <h4 style="color: #58a6ff; font-size: 0.9rem; margin-bottom: 20px;">{name if name else '...'}</h4>
                        <p style="font-size: 0.7rem; color: #8b949e; letter-spacing: 1px;">PROMISE</p>
                        <p style="font-size: 0.85rem; height: 90px; overflow: hidden; color: #c9d1d9;">{promise if promise else '...'}</p>
                        <div style="background: rgba(126, 231, 135, 0.1); padding: 8px; border-radius: 8px; margin-top: 15px;">
                            <span style="color: #7ee787; font-weight: 800;">{price if price else 'N/A'}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

elif menu_clean == "Angles":
    st.markdown("<div class='gradient-header'>SALES ANGLES</div>", unsafe_allow_html=True)
    df = pd.DataFrame(fetch_raw_values("Sales Angles"))
    t1, t2 = st.tabs(["🏛️ Market Standards", "⚡ Disruptive Angles"])
    with t1: st.dataframe(df.iloc[:10], use_container_width=True)
    with t2: st.dataframe(df.iloc[10:], use_container_width=True)

elif menu_clean in ["Awareness", "Matrix"]:
    st.markdown("<div class='gradient-header'>AWARENESS MATRIX</div>", unsafe_allow_html=True)
    df = pd.DataFrame(fetch_raw_values("Awareness Levels"))
    st.dataframe(df, use_container_width=True)

elif menu_clean == "Objections":
    st.markdown("<div class='gradient-header'>OBJECTIONS MATRIX</div>", unsafe_allow_html=True)
    df = pd.DataFrame(fetch_raw_values("Objections"))
    st.dataframe(df, use_container_width=True)

elif menu_clean in ["Cohorts", "Targeted"]:
    st.markdown("<div class='gradient-header'>TARGETED COHORTS</div>", unsafe_allow_html=True)
    data = fetch_raw_values("Cohorts")
    if data:
        df = pd.DataFrame(data)
        cols = st.columns(3)
        for i, col in enumerate(cols):
            with col:
                idx = [1, 4, 7][i]
                title = df.iloc[2, idx] if len(df) > 2 and idx < len(df.columns) else f"Avatar {i+1}"
                st.markdown(f"<div class='glass-card' style='border-top: 4px solid #bc8cff; text-align: center;'><h3 style='color: #bc8cff; font-size: 1.1rem;'>{title}</h3></div>", unsafe_allow_html=True)
                st.dataframe(df.iloc[3:, [idx]].dropna(), use_container_width=True)

st.sidebar.divider()
if st.sidebar.button("📥 EXPORT STRATEGY PDF"):
    st.toast("Protocol Initialized... Exporting Data...")
st.sidebar.markdown("<br><p style='text-align: center; color: #484f58; font-size: 0.6rem; letter-spacing: 2px;'>MARKET RESEARCH PROTOCOL V5.0<br>POWERED BY ANTIGRAVITY AI</p>", unsafe_allow_html=True)
