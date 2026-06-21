import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
from calculators import calculate_sip, calculate_emi, calculate_retirement, calculate_fire
from budget import get_budget_recommendations
from goals import calculate_goal_required
from portfolio import get_asset_allocation, evaluate_portfolio
from ai_insights import get_financial_health_score, query_finmate_ai
from reports import generate_report_summary

# Set up page configurations and remove default margins
st.set_page_config(page_title="FinMate AI", layout="wide", initial_sidebar_state="expanded")

# ⏰ DYNAMIC DATE, TIME & GREETING ENGINE
# This runs automatically to pull the exact current day, date, time, and greeting whenever the app is opened or refreshed.
now = datetime.now()
current_hour = now.hour
current_day_str = now.strftime("%A, %d %B %Y")  # Output format: Monday, 22 June 2026
current_time_str = now.strftime("%I:%M %p")     # Output format: 10:45 PM

# Explicit Greeting Rules Matrix
if 5 <= current_hour < 12:
    greeting_msg = "Good Morning"
elif 12 <= current_hour < 17:
    greeting_msg = "Good Afternoon"
elif 17 <= current_hour < 21:
    greeting_msg = "Good Evening"
else:
    greeting_msg = "Good Night"

# High-Fidelity Premium UI Stylesheets (Inspired by Groww, INDmoney, Zerodha & CRED)
st.markdown("""
    <style>
    /* Global Canvas Architecture & Serif Typography Overrides */
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: #F5F7F6 !important;
        background-image: 
            radial-gradient(circle at 90% 10%, rgba(27, 94, 32, 0.04) 0%, transparent 50%),
            linear-gradient(180deg, rgba(255, 255, 255, 0.8) 0%, rgba(245, 247, 246, 1) 100%),
            url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320" preserveAspectRatio="none" opacity="0.04"><path fill="%231B5E20" d="M0,224L120,202.7C240,181,480,139,720,138.7C960,139,1200,181,1320,202.7L1440,224L1440,320L1320,320C1200,320,960,320,720,320C480,320,240,320,120,320L0,320Z"></path><path fill="%232E7D32" d="M0,160L240,192C480,224,960,288,1200,256L1440,224L1440,320L1200,320C960,320,480,320,240,320L0,320Z"></path></svg>') !important;
        background-size: 100% 100%, 100% 100%, 100% 400px !important;
        background-repeat: no-repeat !important;
        background-position: top center !important;
        color: #1F2937 !important;
        font-family: "Times New Roman", Times, serif !important;
    }
    
    h1, h2, h3, h4, h5, h6, p, label, span, div, button, input, select {
        font-family: "Times New Roman", Times, serif !important;
    }
    
    .dashboard-main-title {
        font-size: 42px !important;
        font-weight: 700 !important;
        color: #1F2937 !important;
        margin-bottom: 2px !important;
    }
    
    .section-headline {
        font-size: 30px !important;
        font-weight: 700 !important;
        color: #1F2937 !important;
        margin-top: 24px !important;
        margin-bottom: 16px !important;
    }
    
    .normal-body-text {
        font-size: 18px !important;
        color: #44475B !important;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    div[data-testid="stDeployButton"] {display: none;}
    
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0B3D2E 0%, #14532D 100%) !important;
        border-right: none !important;
        box-shadow: 4px 0px 24px rgba(0, 61, 46, 0.15) !important;
    }
    
    .sidebar-brand-wrapper {
        padding: 24px 16px;
        text-align: left;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 20px;
    }
    
    .brand-main-text {
        color: #FFFFFF !important;
        font-size: 26px !important;
        font-weight: 700 !important;
        letter-spacing: -0.5px;
    }
    
    .brand-sub-text {
        color: #00D09C !important;
        font-size: 12px !important;
        font-weight: 500;
        letter-spacing: 0.5px;
        display: block;
        margin-top: 2px;
    }

    section[data-testid="stSidebar"] .stRadio > label,
    section[data-testid="stSidebar"] div[data-testid="stWidgetLabel"] {
        display: none !important;
    }
    
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
        background-color: transparent !important;
        color: rgba(255, 255, 255, 0.8) !important;
        border-radius: 8px !important;
        padding: 12px 18px !important;
        margin-bottom: 6px !important;
        border: none !important;
        font-size: 18px !important;
        font-weight: 600 !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
        background-color: rgba(255, 255, 255, 0.08) !important;
        color: #FFFFFF !important;
        transform: translateX(6px);
    }
    
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label[data-checked="true"] {
        background-color: #1B5E20 !important;
        color: #FFFFFF !important;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.12) !important;
    }

    div[data-testid="stMetric"] {
        background-color: #FFFFFF !important;
        border: 1px solid rgba(0, 0, 0, 0.04) !important;
        border-radius: 16px !important;
        padding: 24px !important;
        box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.02) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    
    div[data-testid="stMetric"]:hover {
        transform: translateY(-4px);
        box-shadow: 0px 12px 30px rgba(27, 94, 32, 0.06) !important;
        border-color: rgba(27, 94, 32, 0.15) !important;
    }
    
    div[data-testid="stMetricLabel"] {
        color: #6B7280 !important;
        font-size: 14px !important;
        font-weight: 500 !important;
    }
    
    div[data-testid="stMetricValue"] {
        color: #1F2937 !important;
        font-size: 32px !important;
        font-weight: 700 !important;
        margin-top: 6px !important;
    }
    
    .premium-tool-card {
        background: #FFFFFF;
        border: 1px solid rgba(0, 0, 0, 0.04);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.02);
        transition: all 0.3s ease;
    }
    
    .premium-tool-card:hover {
        transform: translateY(-4px);
        box-shadow: 0px 12px 32px rgba(27, 94, 32, 0.07);
        border-color: rgba(27, 94, 32, 0.18);
    }
    
    .tool-card-icon {
        font-size: 30px;
        margin-bottom: 12px;
        display: inline-block;
    }
    
    .tool-card-title {
        font-size: 20px !important;
        font-weight: 700 !important;
        color: #1F2937 !important;
        margin-bottom: 8px;
    }
    
    .tool-card-desc {
        font-size: 15px !important;
        color: #6B7280 !important;
        line-height: 1.5;
    }
    
    .stButton>button {
        background-color: #1B5E20 !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        border-radius: 10px !important;
        border: none !important;
        padding: 12px 24px !important;
        transition: all 0.25s ease !important;
        box-shadow: 0px 4px 12px rgba(27, 94, 32, 0.15) !important;
        width: 100%;
    }
    
    .stButton>button:hover {
        background-color: #2E7D32 !important;
        transform: translateY(-2px);
        box-shadow: 0px 6px 16px rgba(46, 125, 50, 0.25) !important;
    }
    
    .top-header-navbar {
        background-color: #FFFFFF;
        border: 1px solid rgba(0, 0, 0, 0.04);
        padding: 14px 32px;
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 32px;
        box-shadow: 0px 2px 12px rgba(0, 0, 0, 0.01);
    }
    
    .header-left-brand {
        font-size: 22px;
        font-weight: 700;
        color: #1b5e20;
    }
    
    .header-right-meta {
        font-size: 15px;
        color: #44475B;
        font-weight: 500;
        text-align: right;
    }

    div[data-testid="stForm"], .stAlert {
        background-color: #FFFFFF !important;
        border: 1px solid rgba(0, 0, 0, 0.04) !important;
        border-radius: 16px !important;
        box-shadow: 0px 4px 25px rgba(0, 0, 0, 0.02) !important;
        padding: 28px !important;
    }
    
    input, select, textarea {
        background-color: #FFFFFF !important;
        color: #1F2937 !important;
        border: 1px solid #E5E7EB !important;
        border-radius: 10px !important;
    }
    
    hr {
        border-top: 1px solid #E5E7EB !important;
    }
    </style>
""", unsafe_allow_html=True)

# Top Navbar Layout (Design remains identical, content values are now completely dynamic)
st.markdown(f"""
    <div class="top-header-navbar">
        <div class="header-left-brand">📈 FINMATE AI</div>
        <div class="header-right-meta">
            🔍 &nbsp;&nbsp;&nbsp;&nbsp; 🔔 &nbsp;&nbsp;&nbsp;&nbsp; 👤 &nbsp;&nbsp;
            <b>{greeting_msg}, Kirtimaan</b> &nbsp;|&nbsp; {current_day_str} &nbsp;|&nbsp; {current_time_str}
        </div>
    </div>
""", unsafe_allow_html=True)
