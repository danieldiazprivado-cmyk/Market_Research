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
    page_title="MAPs | Market Research Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- CUSTOM CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    .main {
        background-color: #f8f9fa;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
        font-weight: 600;
    }

    .stTabs [aria-selected="true"] {
        background-color: #e9ecef;
        border-bottom: 2px solid #007bff;
    }

    .cohort-card {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border-top: 5px solid #007bff;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# --- AUTH & DATA FETCH ---
@st.cache_resource
def get_gspread_client():
    # Try Streamlit Secrets first (for Cloud Deployment)
    if "gcp_service_account" in st.secrets:
        creds = Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=SCOPES
        )
    # Fallback to local file (for local development)
    else:
        creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
    
    return gspread.authorize(creds)

def fetch_data(sheet_name):
    client = get_gspread_client()
    sh = client.open_by_key(SHEET_ID)
    worksheet = sh.worksheet(sheet_name)
    df = get_as_dataframe(worksheet, evaluate_formulas=True).dropna(how='all').dropna(axis=1, how='all')
    return df

# --- SIDEBAR ---
st.sidebar.title("🔍 Navigation")
menu = st.sidebar.radio(
    "Select Research Section",
    ["Product", "Competitors", "Sales Angles", "Awareness Levels", "Differentials", "Objections", "Cohorts"]
)

st.sidebar.divider()
search_query = st.sidebar.text_input("🔦 Search Keywords", placeholder="Type to filter...")

# --- PDF EXPORT ---
def create_pdf(content_dict):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(40, 10, "Market Research Summary - MAPs")
    pdf.ln(20)
    
    for section, df in content_dict.items():
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(40, 10, section)
        pdf.ln(10)
        pdf.set_font("Helvetica", "", 10)
        # Add basic table info (Top 5 rows for summary)
        for index, row in df.head(5).iterrows():
            text = " | ".join([str(val) for val in row.values if pd.notna(val)])
            pdf.multi_cell(0, 10, text[:200]) # Truncate for fit
        pdf.ln(10)
    
    return pdf.output(dest='S')

# --- MAIN CONTENT ---
st.title(f"📊 {menu} Analysis")

if menu == "Product":
    df = fetch_data("Product")
    if search_query:
        df = df[df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]
    
    st.dataframe(df, use_container_width=True)

elif menu == "Competitors":
    df = fetch_data("Competitors")
    if search_query:
        df = df[df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]
    
    st.table(df) # Competitors look better as a static table

elif menu == "Sales Angles":
    df = fetch_data("Sales Angles")
    tab1, tab2 = st.tabs(["Market Standard", "Disruptive"])
    
    with tab1:
        st.subheader("Current Market Angles")
        # Assuming Market Standard is first part of the sheet
        st.table(df.iloc[:10] if len(df) >= 10 else df)
        
    with tab2:
        st.subheader("New Disruptive Angles")
        st.table(df.iloc[10:] if len(df) > 10 else pd.DataFrame(columns=["No data"]))

elif menu == "Awareness Levels":
    df = fetch_data("Awareness Levels")
    if search_query:
        df = df[df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]
    st.dataframe(df, use_container_width=True)

elif menu == "Differentials":
    df = fetch_data("Differentials")
    st.table(df)

elif menu == "Objections":
    df = fetch_data("Objections")
    if search_query:
        df = df[df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]
    
    # Objections usually have a matrix structure
    st.dataframe(df, use_container_width=True)

elif menu == "Cohorts":
    df = fetch_data("Cohorts")
    # Layout Cohorts in Columns
    cols = st.columns(3)
    
    # Adjust indexing based on how Cohorts are structured (usually Columns B, E, H)
    # We'll assume the DF has mapped these correctly
    for i, col_idx in enumerate([0, 1, 2]):
        if i < len(cols):
            with cols[i]:
                st.markdown(f"""
                <div class="cohort-card">
                    <h3>Avatar {i}</h3>
                    <p>Detailed profile from Google Sheets</p>
                </div>
                """, unsafe_allow_html=True)
                # Show subset of data
                if len(df.columns) > i:
                    st.write(df.iloc[:, [i]])

# --- FOOTER & EXPORT ---
st.divider()
if st.button("📥 Download PDF Summary"):
    # Collect data for PDF (Simple summary)
    summary_data = {
        "Product": fetch_data("Product"),
        "Sales Angles": fetch_data("Sales Angles")
    }
    pdf_bytes = create_pdf(summary_data)
    b64 = base64.b64encode(pdf_bytes).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="Market_Research_Survey.pdf">Click here to download</a>'
    st.markdown(href, unsafe_allow_html=True)

st.caption("Powered by Antigravity AI | Market Research Protocol v1.0")
