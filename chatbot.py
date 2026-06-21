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

# 1. Page Configuration (Sidebar ko force expand rakhne ke liye)
st.set_page_config(
    page_title="FinMate AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. ⏰ Dynamic Date, Time & Greeting Engine
now = datetime.now()
current_hour = now.hour
current_day_str = now.strftime("%A, %d %B %Y")
current_time_str = now.strftime("%I:%M %p")

if 5 <= current_hour < 12:
    greeting_msg = "Good Morning"
elif 12 <= current_hour < 17:
    greeting_msg = "Good Afternoon"
elif 17 <= current_hour < 21:
    greeting_msg = "Good Evening"
else:
    greeting_msg = "Good Night"

# 3. 🎨 Premium UI Stylesheet (Toolbar visibility enabled)
st.markdown("""
    <style>
    /* Global Background and Typography */
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: #F5F7F6 !important;
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

    /* NOTE: We removed visibility:hidden for headers so that Three Dots and Sidebar toggle are visible */
    div[data-testid="stDeployButton"] {display: none;}
    
    /* Dark Green Sidebar Layout */
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
    }
    
    .brand-sub-text {
        color: #00D09C !important;
        font-size: 12px !important;
        display: block;
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
        font-size: 18px !important;
        font-weight: 600 !important;
    }
    
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label[data-checked="true"] {
        background-color: #1B5E20 !important;
        color: #FFFFFF !important;
    }

    div[data-testid="stMetric"] {
        background-color: #FFFFFF !important;
        border-radius: 16px !important;
        padding: 24px !important;
        box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.02) !important;
    }
    
    .premium-tool-card {
        background: #FFFFFF;
        border: 1px solid rgba(0, 0, 0, 0.04);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
    }
    
    .top-header-navbar {
        background-color: #FFFFFF;
        padding: 14px 32px;
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 32px;
    }
    
    .header-left-brand { font-size: 22px; font-weight: 700; color: #1b5e20; }
    .header-right-meta { font-size: 15px; color: #44475B; font-weight: 500; }
    </style>
""", unsafe_allow_html=True)

# 5. Sidebar Branding Custom Injector
st.sidebar.markdown("""
    <div class="sidebar-brand-wrapper">
        <div class="brand-main-text">📈 FINMATE AI</div>
        <div class="brand-sub-text">Your Intelligent Financial Companion</div>
    </div>
""", unsafe_allow_html=True)

# 6. Session State Engine Initialization
if 'income' not in st.session_state: st.session_state.income = 75000
if 'rent' not in st.session_state: st.session_state.rent = 15000
if 'food' not in st.session_state: st.session_state.food = 8000
if 'fun' not in st.session_state: st.session_state.fun = 5000
if 'util' not in st.session_state: st.session_state.util = 4000
if 'misc' not in st.session_state: st.session_state.misc = 3000
if 'chat_history' not in st.session_state: st.session_state.chat_history = []

# Navigation Radio Options
page = st.sidebar.radio("Navigate Workspace", [
    "Dashboard", "AI Finance Coach", "Budget Planner", 
    "SIP Calculator", "EMI Calculator", "Goal Planner", 
    "Investments", "Reports"
])

# Global Financial Math Logic Variables
total_expenses = st.session_state.rent + st.session_state.food + st.session_state.fun + st.session_state.util + st.session_state.misc
calculated_savings = st.session_state.income - total_expenses
savings_ratio = (calculated_savings / st.session_state.income) * 100 if st.session_state.income > 0 else 0
health_score, health_status = get_financial_health_score(savings_ratio, 25)

# ----------------- PAGE 1: HOME DASHBOARD -----------------
if page == "Dashboard":
    st.markdown("<div class='dashboard-main-title'>Welcome back, Kirtimaan!</div>", unsafe_allow_html=True)
    st.markdown("<p style='color: #6B7280; font-size: 18px; margin-bottom: 28px;'>Here's your financial overview for today.</p>", unsafe_allow_html=True)
    
    # Premium Upper Analytics Metric Cards
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1: st.metric("Monthly Income", f"₹{st.session_state.income:,}")
    with col2: st.metric("Expenses", f"₹{total_expenses:,}")
    with col3: st.metric("Savings", f"₹{calculated_savings:,}")
    with col4: st.metric("Investments", f"₹{int(calculated_savings * 0.53):,}")
    with col5: st.metric("Financial Health Score", f"{health_score}/100", f"Status: {health_status}")
    
    st.markdown("<div class='section-headline'>Recent Insights</div>", unsafe_allow_html=True)
    ins_c1, ins_c2, ins_c3, ins_c4 = st.columns(4)
    with ins_c1: st.success("📈 You saved 53% this month.")
    with ins_c2: st.info("✨ Your expenses are under control.")
    with ins_c3: st.warning("⚠️ Increase SIP by ₹2,000.")
    with ins_c4: st.success("🎯 You are on track to reach your goal.")
        
    st.write("---")
    
    # Products & Tools Cards Section Grid Layout
    st.markdown("<div class='section-headline'>Our Products & Tools</div>", unsafe_allow_html=True)
    p_col1, p_col2, p_col3 = st.columns(3)
    with p_col1:
        st.markdown("""
            <div class="premium-tool-card">
                <div class="tool-card-icon">💳</div>
                <div class="tool-card-title">Budget Planner</div>
                <div class="tool-card-desc">Track exactly where your money goes every single month and optimize your monthly utility habits instantly.</div>
            </div>
        """, unsafe_allow_html=True)
    with p_col2:
        st.markdown("""
            <div class="premium-tool-card">
                <div class="tool-card-icon">📈</div>
                <div class="tool-card-title">SIP Calculator</div>
                <div class="tool-card-desc">See how small investments grow over time into large wealth using standard compounding equations.</div>
            </div>
        """, unsafe_allow_html=True)
    with p_col3:
        st.markdown("""
            <div class="premium-tool-card">
                <div class="tool-card-icon">🏠</div>
                <div class="tool-card-title">EMI Calculator</div>
                <div class="tool-card-desc">Check out exactly how much your monthly loan installment options will look like before talking to banks.</div>
            </div>
        """, unsafe_allow_html=True)

    p_col4, p_col5, p_col6 = st.columns(3)
    with p_col4:
        st.markdown("""
            <div class="premium-tool-card">
                <div class="tool-card-icon">🎯</div>
                <div class="tool-card-title">Goal Planner</div>
                <div class="tool-card-desc">Map out specific allocations for buying your dream home, vehicle assets, or emergency backup funds.</div>
            </div>
        """, unsafe_allow_html=True)
    with p_col5:
        st.markdown("""
            <div class="premium-tool-card">
                <div class="tool-card-icon">💼</div>
                <div class="tool-card-title">Investments</div>
                <div class="tool-card-desc">Where should you invest your money? Evaluate risk setups based on conservative or aggressive allocations.</div>
            </div>
        """, unsafe_allow_html=True)
    with p_col6:
        st.markdown("""
            <div class="premium-tool-card">
                <div class="tool-card-icon">🛑</div>
                <div class="tool-card-title">Debt Manager</div>
                <div class="tool-card-desc">Organize multiple liabilities using accelerated paydown structures like the Avalanche methodology.</div>
            </div>
        """, unsafe_allow_html=True)

    st.write("---")
    
    # Analytics Charts Interface
    col_left, col_right = st.columns(2)
    with col_left:
        st.markdown("<div class='section-headline'>Where are you spending your money?</div>", unsafe_allow_html=True)
        labels = ['Rent & Housing', 'Groceries & Food', 'Fun & Lifestyle', 'Connectivity/Utilities', 'Unplanned Extras']
        values = [st.session_state.rent, st.session_state.food, st.session_state.fun, st.session_state.util, st.session_state.misc]
        fig = px.pie(names=labels, values=values, hole=0.6, color_discrete_sequence=px.colors.sequential.Greens_r)
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#1F2937', margin=dict(t=20,b=20,l=20,r=20))
        st.plotly_chart(fig, use_container_width=True)
        
    with col_right:
        st.markdown("<div class='section-headline'>Your Progress Tracker</div>", unsafe_allow_html=True)
        categories = ['Emergency Fund Reserve', 'Core Wealth Portfolio', 'Retirement Index Target']
        progress = [85, 45, 22]
        fig_bar = px.bar(x=progress, y=categories, orientation='h', range_x=[0, 100], color_discrete_sequence=['#1B5E20'])
        fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#1F2937', margin=dict(t=20,b=20,l=20,r=20))
        st.plotly_chart(fig_bar, use_container_width=True)

    st.write("---")
    
    # Quick Actions Framework Matrix Button Rows
    st.markdown("<div class='section-headline'>Quick Actions</div>", unsafe_allow_html=True)
    q_c1, q_c2, q_c3, q_c4 = st.columns(4)
    with q_c1: st.button("➕ Add Expense")
    with q_c2: st.button("🚀 Start SIP")
    with q_c3: st.button("📑 Download Report")
    with q_c4: st.button("🔍 Check Loan Eligibility")
    
    st.write("---")
    st.markdown("<div class='section-headline'>Daily Finance Tip</div>", unsafe_allow_html=True)
    st.info("💬 *\"The best investment you can make is in yourself.\"*")

# ----------------- PAGE 2: AI FINANCE COACH -----------------
elif page == "AI Finance Coach":
    st.markdown("<div class='dashboard-main-title'>🤖 AI Finance Coach</div>", unsafe_allow_html=True)
    st.markdown("<p class='normal-body-text'>Ask any question about balancing your cash flow, managing loans, or understanding compound interest.</p>", unsafe_allow_html=True)
    
    # Stabilized Form block layout structure
    with st.form(key="chat_input_form", clear_on_submit=True):
        user_query = st.text_input("Ask a question in plain English (e.g., 'Where should you invest your money?'):")
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
    st.markdown("<div class='dashboard-main-title'>💳 Budget Planner</div>", unsafe_allow_html=True)
    st.write("---")
    col_inputs, col_outputs = st.columns([1, 1])
    with col_inputs:
        st.markdown("<div class='section-headline'>Enter your numbers:</div>", unsafe_allow_html=True)
        st.session_state.income = st.number_input("Monthly Income", value=st.session_state.income, step=5000)
        st.session_state.rent = st.number_input("Rent / Housing Cost", value=st.session_state.rent, step=1000)
        st.session_state.food = st.number_input("Groceries & Food", value=st.session_state.food, step=1000)
        st.session_state.fun = st.number_input("Entertainment & Fun", value=st.session_state.fun, step=500)
        st.session_state.util = st.number_input("Utilities & Internet", value=st.session_state.util, step=500)
        st.session_state.misc = st.number_input("Other Extra Expenses", value=st.session_state.misc, step=500)
        
    with col_outputs:
        st.markdown("<div class='section-headline'>Your Budget Analysis</div>", unsafe_allow_html=True)
        sav, pct, recs = get_budget_recommendations(st.session_state.income, {
            'Rent': st.session_state.rent, 'Food': st.session_state.food,
            'Entertainment': st.session_state.fun, 'Utilities': st.session_state.util,
            'Miscellaneous': st.session_state.misc
        })
        st.metric("Money Left to Save or Invest", f"₹{sav:,}", f"{pct:.1f}% Savings Rate")
        st.write("### Recommendations for You:")
        for rec in recs:
            st.info(rec)

# ----------------- PAGE 4: SIP CALCULATOR -----------------
elif page == "SIP Calculator":
    st.markdown("<div class='dashboard-main-title'>📈 SIP Calculator</div>", unsafe_allow_html=True)
    st.write("---")
    c1, c2, c3 = st.columns(3)
    with c1: monthly_sip = st.slider("Monthly SIP Investment amount (₹)", 1000, 100000, 10000, step=1000)
    with c2: expected_return = st.slider("Expected Annual Return (%)", 5.0, 22.0, 12.0, step=0.5)
    with c3: horizon_years = st.slider("Investment Horizon Time (Years)", 1, 40, 15)
    
    invested, wealth, total_value = calculate_sip(monthly_sip, expected_return, horizon_years)
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1: st.metric("Total Money Put In", f"₹{invested:,}")
    with col_m2: st.metric("Total Returns Earned", f"₹{wealth:,}")
    with col_m3: st.metric("Total Wealth Value", f"₹{total_value:,}")
    
    st.write("### Multi-Tiered Projection Simulator (Alternative Commitments)")
    benchmarks = [5000, 10000, 20000]
    sim_data = []
    for b in benchmarks:
        _, _, val = calculate_sip(b, expected_return, horizon_years)
        sim_data.append({"Monthly Allocation": f"₹{b:,}", "Final Wealth Value": val})
    
    df_sim = pd.DataFrame(sim_data)
    fig_sim = px.bar(df_sim, x="Monthly Allocation", y="Final Wealth Value", color="Final Wealth Value", color_continuous_scale='Greens')
    fig_sim.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#1F2937')
    st.plotly_chart(fig_sim, use_container_width=True)

# ----------------- PAGE 5: EMI CALCULATOR -----------------
elif page == "EMI Calculator":
    st.markdown("<div class='dashboard-main-title'>🏠 EMI Calculator</div>", unsafe_allow_html=True)
    st.write("---")
    l_col, r_col = st.columns(2)
    with l_col:
        p = st.number_input("Total Loan Amount (₹)", value=500000, step=50000)
        r = st.slider("Interest Rate Percentage (%)", 4.0, 24.0, 9.5, step=0.1)
        t = st.slider("Loan Duration Timeline (Years)", 1, 30, 7)
        emi, interest, total_pay = calculate_emi(p, r, t)
    with r_col:
        st.metric("Your Monthly EMI Payout", f"₹{emi:,}")
        st.metric("Total Loan Interest Cost", f"₹{interest:,}")
        st.metric("Total Payout Amount", f"₹{total_pay:,}")
        
    fig_emi = px.pie(names=['Loan Principal Base', 'Extra Interest Cost Burden'], values=[p, interest], color_discrete_sequence=['#1B5E20', '#EF4444'])
    fig_emi.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#1F2937')
    st.plotly_chart(fig_emi, use_container_width=True)

# ----------------- PAGE 6: GOAL PLANNER -----------------
elif page == "Goal Planner":
    st.markdown("<div class='dashboard-main-title'>🎯 Goal Planner</div>", unsafe_allow_html=True)
    st.write("---")
    g_type = st.selectbox("What are you saving up for?", ["Dream House Acquisition", "High Performance EV Car Purchase", "Global Family Vacation", "Children Higher Education Fund"])
    g_target = st.number_input("Target Amount Needed (₹)", value=2500000, step=50000)
    g_time = st.slider("Years left to reach this goal", 1, 25, 8)
    
    monthly_required = calculate_goal_required(g_target, g_time)
    st.success(f"💡 Target Milestone Strategy: To save enough for your **{g_type}**, you need to save **₹{monthly_required:,}** every single month.")

# ----------------- PAGE 7: INVESTMENTS -----------------
elif page == "Investments":
    st.markdown("<div class='dashboard-main-title'>💼 Where should you invest your money?</div>", unsafe_allow_html=True)
    st.write("---")
    risk_appetite = st.selectbox("Choose your personal investing comfort level:", ["Conservative", "Moderate", "Aggressive"])
    target_alloc = get_asset_allocation(risk_appetite)
    
    fig_alloc = px.pie(names=list(target_alloc.keys()), values=list(target_alloc.values()), color_discrete_sequence=px.colors.sequential.Greens_r)
    fig_alloc.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#1F2937')
    st.plotly_chart(fig_alloc, use_container_width=True)
    
    st.markdown("<div class='section-headline'>Audit your current investments tracker:</div>", unsafe_allow_html=True)
    eq = st.slider("Your Current Stock Market / Equity Ratio (%)", 0, 100, 50)
    db = st.slider("Your Current Fixed Income / Debt Ratio (%)", 0, 100, 40)
    gd = st.slider("Your Current Safe Gold Ratio (%)", 0, 100, 10)
    
    if (eq + db + gd) != 100:
        st.error("⚠️ Error Check: The total allocation across your portfolio must equal exactly 100%. Adjust sliders.")
    else:
        audit_results = evaluate_portfolio({"Equity": eq, "Debt": db, "Gold": gd}, risk_appetite)
        for feedback in audit_results:
            st.info(feedback)

# ----------------- PAGE 8: REPORTS -----------------
elif page == "Reports":
    st.markdown("<div class='dashboard-main-title'>📑 Performance Reports Studio</div>", unsafe_allow_html=True)
    st.write("---")
    st.write("Review a clear structural breakdown of your real-time finance setups instantly.")
    
    text_summary = generate_report_summary(st.session_state.income, total_expenses, calculated_savings, health_score)
    st.text_area("Your Financial Diagnostic Matrix Statement Logs", value=text_summary, height=250)
    st.download_button(label="Download Text Statement", data=text_summary, file_name="FinMate_Statement.txt", mime="text/plain")
