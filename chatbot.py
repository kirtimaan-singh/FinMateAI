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

# 1. Page Frame Layout Initial Configuration
st.set_page_config(
    page_title="FinMateAI",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. ⏰ Dynamic Server-Side Live Clock System
now = datetime.now()
current_hour = now.hour
current_day_str = now.strftime("%A, %d %B %Y")
current_time_str = now.strftime("%I:%M %p")

if 5 <= current_hour < 12:
    greeting_msg = "Good morning"
elif 12 <= current_hour < 17:
    greeting_msg = "Good afternoon"
elif 17 <= current_hour < 21:
    greeting_msg = "Good evening"
else:
    greeting_msg = "Good afternoon" 

# 3. 🎨 Premium Visible Typography Institutional UI Engine
st.markdown("""
    <style>
    /* Global Container Workspace Background Reset */
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: #FFFFFF !important;
        background-image: linear-gradient(180deg, rgba(245,247,246,0.3) 0%, #FFFFFF 100%) !important;
        color: #1F2937 !important;
        font-family: "Times New Roman", Times, serif !important;
    }
    
    /* Rigid Typography Scaling Rules */
    h1, h2, h3, h4, h5, h6, p, label, span, div, button, input, select {
        font-family: "Times New Roman", Times, serif !important;
    }
    
    .dashboard-title-box h1 {
        font-size: 36px !important;
        font-weight: 700 !important;
        color: #1F2937 !important;
        margin-bottom: 2px !important;
    }
    
    .section-title-header {
        font-size: 22px !important;
        font-weight: 700 !important;
        color: #1F2937 !important;
        margin-top: 10px !important;
        margin-bottom: 14px !important;
    }

    /* System Layout Toolbar Override Controls */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    div[data-testid="stDeployButton"] {display: none;}
    
    /* Dark Forest Green Sidebar UI Configuration */
    section[data-testid="stSidebar"] {
        background-color: #143D30 !important;
        background-image: linear-gradient(180deg, #163E32 0%, #0C261E 100%) !important;
        border-right: none !important;
    }
    
    .sidebar-corporate-branding {
        padding: 24px 16px;
        font-size: 28px !important;
        font-weight: 700 !important;
        color: #FFFFFF !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        margin-bottom: 24px;
        letter-spacing: -0.5px;
    }
    
    .sidebar-corporate-branding span {
        color: #00D09C !important;
    }

    /* FIXED: Enforced High-Contrast White Sidebar Radio Item Structure */
    section[data-testid="stSidebar"] .stRadio > label,
    section[data-testid="stSidebar"] div[data-testid="stWidgetLabel"] {
        display: none !important;
    }
    
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
        background-color: transparent !important;
        color: #FFFFFF !important; /* Forces absolute visibility */
        border-radius: 10px !important;
        padding: 12px 20px !important;
        margin-bottom: 4px !important;
        border: none !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
    }
    
    /* Enforces child components like strings inside label to remain white */
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label * {
        color: #FFFFFF !important;
    }
    
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: #FFFFFF !important;
    }
    
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label[data-checked="true"] {
        background-color: #235143 !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
    }
    
    /* Sidebar Premium Sinking Sider Box */
    .premium-promo-card {
        background-color: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 14px;
        padding: 20px;
        margin-top: 60px;
        color: #FFFFFF;
    }

    /* Floating White Metric Dynamic Layout Blocks */
    .dashboard-kpi-card {
        background-color: #FFFFFF !important;
        border: 1px solid #ECEFF1 !important;
        border-radius: 14px !important;
        padding: 20px !important;
        box-shadow: 0px 2px 12px rgba(0, 0, 0, 0.015) !important;
        transition: all 0.25s ease;
    }
    
    .dashboard-kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0px 8px 24px rgba(0, 0, 0, 0.03) !important;
    }
    
    .kpi-label { color: #78909C; font-size: 13px; font-weight: 500; }
    .kpi-value { color: #1F2937; font-size: 24px; font-weight: 700; margin-top: 4px; }
    .kpi-delta { font-size: 12px; font-weight: 600; margin-top: 4px; }

    /* Products Cards Layout Structures */
    .tool-matrix-box {
        background: #FFFFFF;
        border: 1px solid #ECEFF1;
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 16px;
        transition: all 0.25s ease;
    }
    
    .tool-matrix-box:hover {
        box-shadow: 0px 8px 24px rgba(0, 0, 0, 0.03);
    }
    
    .tool-header-row { display: flex; align-items: center; gap: 12px; margin-bottom: 6px; }
    .tool-avatar-icon { font-size: 24px; }
    .tool-title-text { font-size: 16px !important; font-weight: 700 !important; color: #1F2937 !important; }
    .tool-body-desc { font-size: 13px !important; color: #78909C !important; line-height: 1.45; }
    
    /* Custom Styled UI System Form Wrappers */
    div[data-testid="stForm"], .stAlert {
        background-color: #FFFFFF !important;
        border: 1px solid #ECEFF1 !important;
        border-radius: 14px !important;
        box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.01) !important;
    }
    
    /* Institutional Primary UI Buttons Layout Mapping */
    .stButton>button {
        background-color: #FFFFFF !important;
        color: #1F2937 !important;
        font-weight: 600 !important;
        font-size: 15px !important;
        border-radius: 10px !important;
        border: 1px solid #ECEFF1 !important;
        padding: 12px 20px !important;
        text-align: left !important;
        width: 100%;
        transition: all 0.2s ease;
    }
    
    .stButton>button:hover {
        background-color: #F8F9FA !important;
        border-color: #CFD8DC !important;
    }
    
    /* Input UI Form Field Enforcements */
    input, select, textarea {
        background-color: #FFFFFF !important;
        color: #1F2937 !important;
        border: 1px solid #ECEFF1 !important;
        border-radius: 10px !important;
    }
    
    hr { border-top: 1px solid #ECEFF1 !important; }

    /* Top Horizontal Corporate Navigation Component Layout Grid */
    .header-navbar-strip {
        background-color: #FFFFFF;
        border-bottom: 1px solid #ECEFF1;
        padding: 16px 24px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 24px;
    }
    
    .navbar-logo-area { font-size: 24px; font-weight: 700; color: #143D30; letter-spacing: -0.5px; }
    .navbar-right-widget-tray { font-size: 14px; color: #546E7A; font-weight: 500; }
    
    /* Right side sub-greeting weather indicator segment layout */
    .dynamic-time-subcard {
        text-align: right;
        font-size: 13px;
        color: #78909C;
    }
    </style>
""", unsafe_allow_html=True)

# Top Premium Navigation Bar Layout Strip
st.markdown("""
    <div class="header-navbar-strip">
        <div class="navbar-logo-area">FinMateAI <span style='color:#00D09C; font-size:16px;'>✦</span></div>
        <div style="font-size:14px; color:#90A4AE; width:40%;">🔍 &nbsp;Search anything...</div>
        <div class="navbar-right-widget-tray">
            🔔<sup><span style='color:#00D09C;'>●</span></sup> &nbsp;&nbsp;&nbsp;&nbsp; 
            <span style="background:#E0F2F1; color:#004D40; padding:6px 12px; border-radius:20px; font-weight:700;">K</span> 
            &nbsp; Kirtimaan Singh ▾
        </div>
    </div>
""", unsafe_allow_html=True)
# Left Navigation Bar Custom Header Branding Integration
st.sidebar.markdown("""
    <div class="sidebar-corporate-branding">FinMateAI<span>✦</span></div>
""", unsafe_allow_html=True)

# ----------------- LAYER CONTEXT INITIALIZATION SYSTEM -----------------
if 'income' not in st.session_state: st.session_state.income = 85000
if 'rent' not in st.session_state: st.session_state.rent = 18000
if 'food' not in st.session_state: st.session_state.food = 10550
if 'fun' not in st.session_state: st.session_state.fun = 8000
if 'util' not in st.session_state: st.session_state.util = 6000
if 'misc' not in st.session_state: st.session_state.misc = 6000
if 'chat_history' not in st.session_state: st.session_state.chat_history = []

# Institutional Left Sidebar Item Tree List configuration
page = st.sidebar.radio("Navigation Workspace Router", [
    "Dashboard", "AI Finance Coach", "Budget Planner", 
    "SIP Calculator", "EMI Calculator", "Goal Planner", 
    "Investments", "Reports", "Learn Finance", "Settings"
])

# Left sidebar dynamic promo component card module injection
st.sidebar.markdown("""
    <div class="premium-promo-card">
        <span style="color:#00D09C; font-weight:700; font-size:14px;">👑 Go Premium</span><br/>
        <span style="font-size:12px; color:#B0BEC5; display:block; margin-top:4px; margin-bottom:12px;">Unlock advanced insights and exclusive tools.</span>
        <div style="background:#FFFFFF; color:#143D30; text-align:center; padding:8px; border-radius:8px; font-weight:700; font-size:13px; cursor:pointer;">Upgrade Now</div>
    </div>
""", unsafe_allow_html=True)

# Underlying Logical Equations Engine Framework Execution
total_expenses = st.session_state.rent + st.session_state.food + st.session_state.fun + st.session_state.util + st.session_state.misc
calculated_savings = st.session_state.income - total_expenses
savings_ratio = (calculated_savings / st.session_state.income) * 100 if st.session_state.income > 0 else 0
health_score, health_status = get_financial_health_score(savings_ratio, 25)

# ----------------- PAGE ROUTER CONDITIONS -----------------
if page == "Dashboard":
    
    # Header Welcome Row Grid Layout
    left_title_col, right_time_col = st.columns([3, 1])
    with left_title_col:
        st.markdown("<div class='dashboard-title-box'><h1>Welcome back, Kirtimaan!</h1></div>", unsafe_allow_html=True)
        st.markdown("<p style='color: #78909C; font-size: 15px; margin-top:-10px;'>Here's your financial overview for today.</p>", unsafe_allow_html=True)
    with right_time_col:
        st.markdown(f"""
            <div class="dynamic-time-subcard">
                {current_day_str}<br/>
                ☀️ &nbsp;{greeting_msg}! &nbsp;<b>{current_time_str}</b>
            </div>
        """, unsafe_allow_html=True)
        
    st.write(" ")
    
    # Row 1: Horizontal Grid Analytics Performance Cards Layout Block
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.markdown(f"""
            <div class="dashboard-kpi-card">
                <div class="kpi-label">👛 Total Balance</div>
                <div class="kpi-value">₹2,45,680</div>
                <div class="kpi-delta" style="color:#00D09C;">↗ 4.35% <span style="color:#90A4AE; font-weight:normal;">from last month</span></div>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
            <div class="dashboard-kpi-card">
                <div class="kpi-label">💼 Monthly Income</div>
                <div class="kpi-value">₹{st.session_state.income:,}</div>
                <div class="kpi-delta" style="color:#78909C;">This month</div>
            </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
            <div class="dashboard-kpi-card">
                <div class="kpi-label">📉 Monthly Expenses</div>
                <div class="kpi-value">₹{total_expenses:,}</div>
                <div class="kpi-delta" style="color:#78909C;">This month</div>
            </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
            <div class="dashboard-kpi-card">
                <div class="kpi-label">💰 Monthly Savings</div>
                <div class="kpi-value">₹{calculated_savings:,}</div>
                <div class="kpi-delta" style="color:#00D09C;">{savings_ratio:.1f}% <span style="color:#90A4AE; font-weight:normal;">of income</span></div>
            </div>
        """, unsafe_allow_html=True)
    with c5:
        st.markdown(f"""
            <div class="dashboard-kpi-card">
                <div class="kpi-label">🛡️ Financial Health Score</div>
                <div class="kpi-value" style="color:#1B5E20;">{health_score} <span style="font-size:14px; color:#90A4AE; font-weight:500;">/100</span></div>
                <div class="kpi-delta" style="color:#1B5E20;">Status: {health_status}</div>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br/>", unsafe_allow_html=True)
    
    # Split Grid: Main Tools Row Matrix vs Right Action Tray Panel
    main_body_left, side_panel_right = st.columns([3, 1])
    
    with main_body_left:
        st.markdown("<div class='section-title-header'>Our Products & Tools</div>", unsafe_allow_html=True)
        
        # Tools Grid Layout Setup Row 1
        tc1, tc2, tc3 = st.columns(3)
        with tc1:
            st.markdown("""
                <div class="tool-matrix-box">
                    <div class="tool-header-row"><span class="tool-avatar-icon">💳</span><span class="tool-title-text">Budget Planner</span></div>
                    <div class="tool-body-desc">Plan and track your monthly budget easily without spreadsheets layout confusion.</div>
                </div>
            """, unsafe_allow_html=True)
        with tc2:
            st.markdown("""
                <div class="tool-matrix-box">
                    <div class="tool-header-row"><span class="tool-avatar-icon">📈</span><span class="tool-title-text">SIP Calculator</span></div>
                    <div class="tool-body-desc">Calculate your compounded long-term investment equity yields values quickly.</div>
                </div>
            """, unsafe_allow_html=True)
        with tc3:
            st.markdown("""
                <div class="tool-matrix-box">
                    <div class="tool-header-row"><span class="tool-avatar-icon">🏠</span><span class="tool-title-text">EMI Calculator</span></div>
                    <div class="tool-body-desc">Calculate loan amortizations tenure structure values before talking to banks.</div>
                </div>
            """, unsafe_allow_html=True)
            
        # Tools Grid Layout Setup Row 2
        tc4, tc5, tc6 = st.columns(3)
        with tc4:
            st.markdown("""
                <div class="tool-matrix-box">
                    <div class="tool-header-row"><span class="tool-avatar-icon">🎯</span><span class="tool-title-text">Goal Planner</span></div>
                    <div class="tool-body-desc">Set strategic milestones timelines allocations and track asset development indices.</div>
                </div>
            """, unsafe_allow_html=True)
        with tc5:
            st.markdown("""
                <div class="tool-matrix-box">
                    <div class="tool-header-row"><span class="tool-avatar-icon">💼</span><span class="tool-title-text">Investments</span></div>
                    <div class="tool-body-desc">Explore institutional diversification avenues and rebalance risks setups.</div>
                </div>
            """, unsafe_allow_html=True)
        with tc6:
            st.markdown("""
                <div class="tool-matrix-box">
                    <div class="tool-header-row"><span class="tool-avatar-icon">🛑</span><span class="tool-title-text">Debt Manager</span></div>
                    <div class="tool-body-desc">Accelerate card repayments frameworks via the structured math parameters.</div>
                </div>
            """, unsafe_allow_html=True)
            
        st.write("---")
        
        # At a Glance Metric Charts Block Segment
        st.markdown("<div class='section-title-header'>At a Glance Summary Metrics</div>", unsafe_allow_html=True)
        ag1, ag2, ag3 = st.columns(3)
        with ag1: st.metric("Total Active Investments", "₹1,75,000", "+6.21% Growth")
        with ag2: st.metric("Total Liabilities Payload", "₹1,20,000", "-2.15% Reduced", delta_color="inverse")
        with ag3: st.metric("Liquid Emergency Reserve", "₹75,000", "6 Months Coverage Plan")
        
        st.write("---")
        
        # Recent Analytical Insights Rows
        st.markdown("<div class='section-title-header'>Recent Insights</div>", unsafe_allow_html=True)
        st.success(f"💡 Automated Allocations Check: You successfully saved {savings_ratio:.0f}% of your disposable base income this month. Excellent!")
        st.info("📊 Leverage Index: Your aggregate home loan liabilities payload is safely under 30% of total cash inflows.")
        st.warning("📈 Compound Action Item: Expand monthly systematic investment allocations by ₹5,000 to maximize returns.")
        
    with side_panel_right:
        st.markdown("<div class='section-title-header'>Daily Finance Tip</div>", unsafe_allow_html=True)
        st.success("💬 *\"The best investment you can make is in yourself. The more you learn, the more you earn.\"* — Warren Buffett")
        
        st.markdown("<br/>", unsafe_allow_html=True)
        
        st.markdown("<div class='section-title-header'>Quick Actions</div>", unsafe_allow_html=True)
        st.button("➕ &nbsp; Add New Expense Outflow")
        st.button("🚀 &nbsp; Start a New Recurring SIP")
        st.button("🔍 &nbsp; Check Portfolio Loan Eligibility")
        st.button("📑 &nbsp; Download Statement Report")

# ----------------- PAGE 2: AI FINANCE COACH -----------------
elif page == "AI Finance Coach":
    st.markdown("<div class='dashboard-title-box'><h1>🤖 AI Finance Coach</h1></div>", unsafe_allow_html=True)
    st.write("---")
    
    with st.form(key="chat_input_form", clear_on_submit=True):
        user_query = st.text_input("Ask any query regarding budgeting, SIP structures, or debt configuration maps:")
        submit_button = st.form_submit_button(label="Send Message")
        
    if submit_button and user_query:
        response = query_finmate_ai(user_query)
        st.session_state.chat_history.append((user_query, response))
        
    for q, r in st.session_state.chat_history:
        st.write("---")
        st.markdown(f"👤 **You:** {q}")
        st.markdown(f"🤖 **Coach:** {r}")

# ----------------- PAGE 3: BUDGET PLANNER -----------------
elif page == "Budget Planner":
    st.markdown("<div class='dashboard-title-box'><h1>💳 Budget Planner</h1></div>", unsafe_allow_html=True)
    st.write("---")
    col_inputs, col_outputs = st.columns([1, 1])
    with col_inputs:
        st.subheader("Modify Core Parameters")
        st.session_state.income = st.number_input("Monthly Income Balance", value=st.session_state.income, step=5000)
        st.session_state.rent = st.number_input("Fixed Housing Outflow / Rent", value=st.session_state.rent, step=1000)
        st.session_state.food = st.number_input("Groceries & Food Supplies", value=st.session_state.food, step=1000)
        st.session_state.fun = st.number_input("Entertainment / Lifestyle Outflows", value=st.session_state.fun, step=500)
        st.session_state.util = st.number_input("Utilities & Connectivity", value=st.session_state.util, step=500)
        st.session_state.misc = st.number_input("Other Unplanned Expenses", value=st.session_state.misc, step=500)
        
    with col_outputs:
        st.subheader("Optimization Analysis Metrics")
        sav, pct, recs = get_budget_recommendations(st.session_state.income, {
            'Rent': st.session_state.rent, 'Food': st.session_state.food,
            'Entertainment': st.session_state.fun, 'Utilities': st.session_state.util,
            'Miscellaneous': st.session_state.misc
        })
        st.metric("Disposable Surplus Available to Invest", f"₹{sav:,}", f"{pct:.1f}% Savings Rate")
        st.write("### Tactical Adjustments Adjuster Engine Logs:")
        for rec in recs: st.info(rec)

# ----------------- PAGE 4: SIP CALCULATOR -----------------
elif page == "SIP Calculator":
    st.markdown("<div class='dashboard-title-box'><h1>📈 SIP Calculator</h1></div>", unsafe_allow_html=True)
    st.write("---")
    c1, c2, c3 = st.columns(3)
    with c1: monthly_sip = st.slider("Target Monthly SIP Allocation (₹)", 1000, 100000, 10000, step=1000)
    with c2: expected_return = st.slider("Expected Annual Return Percentage (%)", 5.0, 22.0, 12.0, step=0.5)
    with c3: horizon_years = st.slider("Investment Horizon Time Span (Years)", 1, 40, 15)
    
    invested, wealth, total_value = calculate_sip(monthly_sip, expected_return, horizon_years)
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1: st.metric("Principal Investment Outlay", f"₹{invested:,}")
    with col_m2: st.metric("Total Returns Earned", f"₹{wealth:,}")
    with col_m3: st.metric("Total Wealth Value Target", f"₹{total_value:,}")

# ----------------- PAGE 5: EMI CALCULATOR -----------------
elif page == "EMI Calculator":
    st.markdown("<div class='dashboard-title-box'><h1>🏠 EMI Calculator</h1></div>", unsafe_allow_html=True)
    st.write("---")
    l_col, r_col = st.columns(2)
    with l_col:
        p = st.number_input("Target Loan Core Principal (₹)", value=500000, step=50000)
        r = st.slider("Annual Pricing Rate Matrix (%)", 4.0, 24.0, 9.5, step=0.1)
        t = st.slider("Target Repayment Duration Horizon (Years)", 1, 30, 7)
        emi, interest, total_pay = calculate_emi(p, r, t)
    with r_col:
        st.metric("Equated Monthly Installment (EMI)", f"₹{emi:,}")
        st.metric("Accumulated Cost Interest Payload", f"₹{interest:,}")
        st.metric("Total Lifecycle Comprehensive Outlay", f"₹{total_pay:,}")

# ----------------- PAGES FALLBACK LOGIC -----------------
else:
    st.markdown(f"<div class='dashboard-title-box'><h1>💼 {page} Hub</h1></div>", unsafe_allow_html=True)
    st.write("---")
    st.info("System integration parameters are actively configured. Navigate sections safely using the green panel options.")
