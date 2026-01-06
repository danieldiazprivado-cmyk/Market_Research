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

    /* Style st.expander to look like the premium green headers */
    .stExpander {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        margin-bottom: 20px !important;
    }

    .stExpander > details {
        border: none !important;
        background: transparent !important;
    }

    .stExpander > details > summary {
        background: linear-gradient(135deg, #238636, #2ea043) !important;
        color: white !important;
        padding: 12px !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        text-align: center !important;
        list-style: none !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(35, 134, 54, 0.3) !important;
        margin-bottom: 10px !important;
    }

    .stExpander > details > summary:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 16px rgba(35, 134, 54, 0.5) !important;
    }

    .stExpander > details > summary > span > div > p {
        font-size: 0.85rem !important;
        letter-spacing: 1.5px !important;
        text-transform: uppercase !important;
        margin: 0 !important;
        color: white !important;
    }

    .stExpander > details > summary svg {
        fill: white !important;
    }

    /* Attributes List for Competitors */
    .comp-attribute {
        display: flex;
        justify-content: space-between;
        padding: 12px 0;
        border-bottom: 1px solid rgba(48, 54, 61, 0.5);
    }
    .comp-label {
        color: #8b949e;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        width: 30%;
    }
    .comp-value {
        color: #e6edf3;
        font-size: 0.95rem;
        width: 68%;
        text-align: right;
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
            
            features_list, benefits_list, meaning_list = [], [], []
            for i in range(feat_idx + 1, len(data)):
                row = data[i]
                if not any(row) or "Producer" in str(row[0]): break
                f, b, m = (row[0] if len(row) > 0 else ""), (row[2] if len(row) > 2 else ""), (row[4] if len(row) > 4 else "")
                if f:
                    features_list.append(f)
                    benefits_list.append(b)
                    meaning_list.append(m)

            with col_f:
                with st.expander("🟢 FEATURES", expanded=True):
                    for item in features_list:
                        st.markdown(f'<div class="feature-item">{item}</div>', unsafe_allow_html=True)
            with col_b:
                with st.expander("🟢 BENEFITS", expanded=True):
                    for item in benefits_list:
                        st.markdown(f'<div class="feature-item">{item}</div>', unsafe_allow_html=True)
            with col_m:
                with st.expander("🟢 MEANING", expanded=True):
                    for item in meaning_list:
                        st.markdown(f'<div class="feature-item">{item}</div>', unsafe_allow_html=True)

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

    else:
        st.warning("No data found in 'Product' sheet.")

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
        st.markdown("### ⚔️ INTERACTIVE BENCHMARKING")
        
        # Attribute rows we want to extract
        attributes = [
            "Name", "Social Media", "Product", "Link", "Hook", 
            "Main Marketing Promise", "Unique mechanism", "Unique selling proposition",
            "General marketing statements", "Evidence", "Deliverables / Features",
            "Price and payment terms", "Bonus that includes", "Risk reversal / Guarantees",
            "Additional observations"
        ]
        
        # Build competitor profiles
        competitors = []
        for i in range(5):
            c_idx = i + 2 # Columns C, D, E, F, G
            profile = {}
            for attr in attributes:
                val = find_in_any_col(data, attr, 0, c_idx)
                if attr == "Name" and not val:
                    val = find_in_any_col(data, "Competitor " + str(i+1), 1, 0) # Backwards fallback if name is not found by title
                profile[attr] = val if val else "..."
            
            # Special check for Name if still "..."
            if profile["Name"] == "...":
                # Try finding "Competitor 1" header and looking 1 row down
                for r_idx, row in enumerate(data):
                    if f"Competitor {i+1}" in str(row):
                        profile["Name"] = data[r_idx+1][c_idx] if r_idx+1 < len(data) else f"Comp {i+1}"
                        break
            
            competitors.append(profile)

        # Tab Navigation for Competitors
        comp_tabs = st.tabs([c["Name"] for c in competitors])
        
        for i, tab in enumerate(comp_tabs):
            with tab:
                c = competitors[i]
                col_left, col_right = st.columns([1, 1], gap="large")
                
                with col_left:
                    st.markdown(f"""
                    <div class="glass-card" style="border-top: 4px solid #58a6ff;">
                        <h3 style="color: #58a6ff; font-size: 1.2rem; margin-bottom: 25px;">Profile: {c['Name']}</h3>
                        <div class="comp-attribute"><div class="comp-label">Social</div><div class="comp-value">{c['Social Media']}</div></div>
                        <div class="comp-attribute"><div class="comp-label">Product</div><div class="comp-value">{c['Product']}</div></div>
                        <div class="comp-attribute"><div class="comp-label">Link</div><div class="comp-value"><a href="{c['Link']}" style="color: #58a6ff;">{c['Link']}</a></div></div>
                        <div class="comp-attribute" style="border: none;"><div class="comp-label">Price</div><div class="comp-value" style="color: #7ee787; font-weight: 800; font-size: 1.1rem;">{c['Price and payment terms']}</div></div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("#### ⚡ Marketing Hook & Promise")
                    draw_card("Main Hook", c["Hook"], color="#bc8cff")
                    draw_card("Core Promise", c["Main Marketing Promise"], color="#7ee787")

                with col_right:
                    st.markdown("#### 🛠️ Unique Mechanism & USP")
                    draw_card("Mechanism", c["Unique mechanism"])
                    draw_card("USP", c["Unique selling proposition"])
                    
                    with st.expander("🔍 Strategic Details", expanded=True):
                        st.markdown(f"**Marketing Statements:** {c['General marketing statements']}")
                        st.markdown(f"**Evidence/Proof:** {c['Evidence']}")
                        st.markdown(f"**Deliverables:** {c['Deliverables / Features']}")
                        st.markdown(f"**Bonus:** {c['Bonus that includes']}")
                        st.markdown(f"**Guarantees:** {c['Risk reversal / Guarantees']}")
                        st.markdown(f"**Observations:** *{c['Additional observations']}*")

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
st.sidebar.markdown("<br><p style='text-align: center; color: #484f58; font-size: 0.6rem; letter-spacing: 2px;'>MARKET RESEARCH PROTOCOL V5.2<br>POWERED BY ANTIGRAVITY AI</p>", unsafe_allow_html=True)
