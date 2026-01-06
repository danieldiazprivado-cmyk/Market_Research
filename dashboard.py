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

    [data-testid="stSidebar"] {
        background-color: #010409 !important;
        border-right: 1px solid #30363d;
    }
    
    .glass-card {
        background-color: #161b22 !important;
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #30363d;
        margin-bottom: 20px;
        color: #e6edf3;
        box-shadow: 0 4px 20px rgba(0,0,0,0.5);
    }
    
    .feature-header {
        background: #238636;
        color: white;
        padding: 10px;
        border-radius: 4px;
        text-align: center;
        font-weight: 800;
        margin-bottom: 15px;
        font-size: 0.9rem;
    }

    .feature-item {
        background: rgba(48, 54, 61, 0.3);
        border: 1px solid #30363d;
        padding: 12px;
        border-radius: 6px;
        margin-bottom: 10px;
        min-height: 80px;
        display: flex;
        align-items: center;
        font-size: 0.85rem;
        color: #c9d1d9;
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

    .gradient-header {
        background: linear-gradient(90deg, #58a6ff, #bc8cff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.5rem;
        margin-bottom: 30px;
        font-family: 'Orbitron', sans-serif;
    }

    .stDataFrame {
        border: 1px solid #30363d !important;
        border-radius: 8px !important;
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

@st.cache_data(ttl=300)
def fetch_raw_values(sheet_name):
    client = get_gspread_client()
    sh = client.open_by_key(SHEET_ID)
    return sh.worksheet(sheet_name).get_all_values()

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='font-size: 1.1rem; color: #58a6ff;'>💎 RESEARCH PROTOCOL</h2>", unsafe_allow_html=True)
    menu = st.radio("", ["🏠 Product", "⚔️ Competitors", "🎯 Sales Angles", "🧠 Awareness", "💎 Differentials", "🛑 Objections", "👥 Cohorts"], index=0)
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
        
        # Identity Header
        st.markdown(f"### 📍 PRODUCT NAME: {p_name}")
        st.divider()

        # 3-COLUMN MECHANISM (MATCHING GOOGLE SHEET)
        st.markdown("### ⚙️ CORE MECHANISM")
        
        # Find Features row
        feat_idx = -1
        for i, row in enumerate(data):
            if "Features" in str(row): 
                feat_idx = i
                break
        
        if feat_idx != -1:
            col_f, col_b, col_m = st.columns(3, gap="medium")
            
            with col_f: st.markdown('<div class="feature-header">FEATURES</div>', unsafe_allow_html=True)
            with col_b: st.markdown('<div class="feature-header">BENEFITS</div>', unsafe_allow_html=True)
            with col_m: st.markdown('<div class="feature-header">MEANING</div>', unsafe_allow_html=True)

            # Collect items
            for i in range(feat_idx + 1, len(data)):
                row = data[i]
                if not any(row) or "Producer" in str(row[0]): break
                
                f = row[0] if len(row) > 0 else ""
                b = row[2] if len(row) > 2 else ""
                m = row[4] if len(row) > 4 else ""
                
                if f:
                    with col_f: st.markdown(f'<div class="feature-item">{f}</div>', unsafe_allow_html=True)
                    with col_b: st.markdown(f'<div class="feature-item">{b}</div>', unsafe_allow_html=True)
                    with col_m: st.markdown(f'<div class="feature-item">{m}</div>', unsafe_allow_html=True)

        st.divider()
        st.markdown("### 🏷️ Strategic Context")
        history = find_data_under(data, "Product/Service History", 0, 1)
        keywords = find_data_under(data, "Product Keywords", 0, 1)
        producer = find_data_under(data, "Producer Information", 0, 1)

        c_low1, c_low2 = st.columns(2)
        with c_low1:
            draw_card("History & Origin", history)
        with c_low2:
            draw_card("Producer Information", producer)
            draw_card("Market Keywords", keywords)

    else:
        st.warning("No data found in 'Product' sheet.")

elif menu_clean == "Competitors":
    st.markdown("<div class='gradient-header'>GLOBAL COMPETITORS</div>", unsafe_allow_html=True)
    data = fetch_raw_values("Competitors")
    
    if data:
        st.markdown("### 🔍 Strategic Gap Analysis")
        p = find_in_any_col(data, "PROBLEM", 0, 1)
        e = find_in_any_col(data, "ENEMY", 0, 1)
        s = find_in_any_col(data, "SOLUTION", 0, 1)
        conc = find_in_any_col(data, "CONCLUSION", 0, 1)
        
        col1, col2, col3 = st.columns(3)
        with col1: draw_card("Problem (Market Gaps)", p)
        with col2: draw_card("Enemy (Friction)", e, color="#ff7b72")
        with col3: draw_card("Solution", s, color="#7ee787")
        draw_card("General Conclusion", conc, color="#bc8cff")

        st.divider()
        st.markdown("### ⚔️ Detailed Benchmarking")
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
                    <div class="glass-card" style="min-height: 250px; text-align: center; border-top: 3px solid #58a6ff;">
                        <h4 style="color: #58a6ff; font-size: 1rem;">{name if name else '...'}</h4>
                        <p style="font-size: 0.7rem; color: #8b949e;">PROMISE</p>
                        <p style="font-size: 0.8rem; height: 80px; overflow: hidden;">{promise if promise else '...'}</p>
                        <div style="background: rgba(126, 231, 135, 0.1); padding: 5px; border-radius: 6px;">
                            <span style="color: #7ee787; font-weight: 700;">{price if price else 'N/A'}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

elif menu_clean == "Angles":
    st.markdown("<div class='gradient-header'>SALES ANGLES</div>", unsafe_allow_html=True)
    df = pd.DataFrame(fetch_raw_values("Sales Angles"))
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
    if data:
        df = pd.DataFrame(data)
        cols = st.columns(3)
        for i, col in enumerate(cols):
            with col:
                idx = [1, 4, 7][i]
                title = df.iloc[2, idx] if len(df) > 2 and idx < len(df.columns) else f"Avatar {i+1}"
                st.markdown(f"<div class='glass-card' style='border-top: 4px solid #bc8cff;'><h3 style='color: #bc8cff; font-size: 1.1rem;'>{title}</h3></div>", unsafe_allow_html=True)
                st.dataframe(df.iloc[3:, [idx]].dropna(), use_container_width=True)

st.sidebar.divider()
if st.sidebar.button("📥 EXPORT PDF REPORT"):
    st.toast("Generating Research Document...")
st.sidebar.markdown("<br><p style='text-align: center; color: #484f58; font-size: 0.6rem;'>MAPs RESEARCH PROTOCOL V4.0</p>", unsafe_allow_html=True)
