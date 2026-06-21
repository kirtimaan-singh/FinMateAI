import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from calculators import calculate_sip, calculate_emi, calculate_retirement, calculate_fire
from budget import get_budget_recommendations
from goals import calculate_goal_required
from portfolio import get_asset_allocation, evaluate_portfolio
from ai_insights import get_financial_health_score, query_finmate_ai
from reports import generate_report_summary

# Set up page configurations and remove default margins
st.set_page_config(page_title="FinMateAI", layout="wide")

# High-Fidelity UI Custom Style Sheets (Inspired by Groww, Zerodha & INDmoney)
st.markdown("""
    <style>
    /* Global Background, Typography, and Layout Structural Overrides */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: #F5F7F6 !important;
        /* Subtle architectural vector wave background pattern */
        background-image: radial-gradient(circle at 80% 20%, rgba(27, 94, 32, 0.03) 0%, transparent 40%),
                          linear-gradient(180deg, rgba(255,255,255,0.6) 0%, rgba(245,247,246,1) 100%) !important;
        color: #1F2937 !important;
        font-family: "Times New Roman", Times, serif !important;
    }
    
    /* Enforce Serif Style Typography Globally across elements */
    h1, h2, h3, h4, h5, h6, p, label, span, div, button, input, select {
        font-family: "Times New Roman", Times, serif !important;
    }
    
    h1, h2, h3 {
        color: #1F2937 !important;
        font-weight: 700 !important;
    }

    /* Hide Default Streamlit Branding Elements (Menu, Deploy button, Footer) */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    div[data-testid="stDeployButton"] {display: none;}
    
    /* Premium Dark Green Sidebar Custom Layout Injection */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0B3D2E 0%, #14532D 100%) !important;
        border-right: none !important;
        box-shadow: 4px 0px 24px rgba(0, 61, 46, 0.15) !important;
    }
    
    /* Logo Container and Text Formatting */
    .sidebar-logo-container {
        padding: 24px 12px;
        text-align: left;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 20px;
    }
    
    .sidebar-logo-text {
        color: #FFFFFF !important;
        font-size: 24px !important;
        font-weight: 700 !important;
        letter-spacing: -0.5px;
    }
    
    .sidebar-logo-sub {
        color: #00D09C !important;
        font-size: 11px !important;
        letter-spacing: 1px;
        text-transform: uppercase;
        display: block;
        margin-top: 2px;
    }

    /* Sidebar Navigation List Controls */
    section[data-testid="stSidebar"] .stRadio > label {
        display: none !important;
    }
    
    section[data-testid="stSidebar"] div[data-testid="stWidgetLabel"] {
        display: none !important;
    }
    
    section[data-testid="stSidebar"] label[data-testid="stWidgetLabel"] {
        display: none !important;
    }
    
    /* Custom Sidebar Item Hover Actions */
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
        background-color: transparent !important;
        color: rgba(255, 255, 255, 0.75) !important;
        border-radius: 8px !important;
        padding: 10px 16px !important;
        margin-bottom: 6px !important;
        border: none !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        font-size: 15px !important;
    }
    
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
        background-color: rgba(255, 255, 255, 0.08) !important;
        color: #FFFFFF !important;
        transform: translateX(4px);
    }
    
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label[data-checked="true"] {
        background-color: #1B5E20 !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1) !important;
    }

    /* Premium Light Fintech Component Display Metrics */
    div[data-testid="stMetric"] {
        background-color: #FFFFFF !important;
        border: 1px solid rgba(0, 0, 0, 0.04) !important;
        border-radius: 16px !important;
        padding: 24px !important;
        box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.02) !important;
        transition: all 0.3s ease !important;
    }
    
    div[data-testid="stMetric"]:hover {
        transform: translateY(-4px);
        box-shadow: 0px 12px 30px rgba(0, 0, 0, 0.05) !important;
        border-color: rgba(27, 94, 32, 0.1) !important;
    }
    
    div[data-testid="stMetricLabel"] {
        color: #6B7280 !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        text-transform: none !important;
    }
    
    div[data-testid="stMetricValue"] {
        color: #1F2937 !important;
        font-size: 28px !important;
        font-weight: 700 !important;
        margin-top: 6px !important;
    }
    
    /* Institutional Premium Product Card Grids */
    .product-card {
        background: #FFFFFF;
        border: 1px solid rgba(0, 0, 0, 0.04);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.02);
        transition: all 0.3s ease;
    }
    
    .product-card:hover {
        transform: translateY(-4px);
        box-shadow: 0px 12px 30px rgba(27, 94, 32, 0.06);
        border-color: rgba(27, 94, 32, 0.15);
    }
    
    .product-icon {
        font-size: 28px;
        margin-bottom: 12px;
        display: inline-block;
    }
    
    .product-title {
        font-size: 18px !important;
        font-weight: 700 !important;
        color: #1F2937 !important;
        margin-bottom: 6px;
    }
    
    .product-desc {
        font-size: 14px !important;
        color: #6B7280 !important;
        line-height: 1.4;
    }
    
    /* Custom Styled UI System Forms and Alerts */
    div[data-testid="stForm"], .stAlert {
        background-color: #FFFFFF !important;
        border: 1px solid rgba(0, 0, 0, 0.04) !important;
        border-radius: 16px !important;
        box-shadow: 0px 4px 25px rgba(0, 0, 0, 0.02) !important;
        padding: 28px !important;
    }
    
    /* Flat Institutional Flat Premium Buttons */
    .stButton>button {
        background-color: #1B5E20 !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        font-size: 15px !important;
        border-radius: 10px !important;
        border: none !important;
        padding: 12px 28px !important;
        transition: all 0.2s ease !important;
        box-shadow: 0px 4px 12px rgba(27, 94, 32, 0.15) !important;
    }
    
    .stButton>button:hover {
        background-color: #2E7D32 !important;
        transform: translateY(-1px);
        box-shadow: 0px 6px 16px rgba(46, 125, 50, 0.25) !important;
    }
    
    /* Input element fields architecture alignment */
    input, select, textarea {
        background-color: #FFFFFF !important;
        color: #1F2937 !important;
        border: 1px solid #E5E7EB !important;
        border-radius: 10px !important;
        padding: 10px !important;
    }
    
    input:focus, select:focus {
        border-color: #1B5E20 !important;
        box-shadow: 0 0 0 1px #1B5E20 !important;
    }
    
    hr {
        border-top: 1px solid #E5E7EB !important;
        margin: 28px 0 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Custom Institutional Logo Branding Injector inside the Dark Green Sidebar
st.sidebar.markdown("""
    <div class="sidebar-logo-container">
        <div class="sidebar-logo-text">📈 FinMateAI</div>
        <div class="sidebar-logo-sub">Wealth Growth Engine</div>
    </div>
""", unsafe_allow_html=True)

# Application Context/Session Management System Initialization
if 'income' not in st.session_state: st.session_state.income = 75000
if 'rent' not in st.session_state: st.session_state.rent = 15000
if 'food' not in st.session_state: st.session_state.food = 8000
if 'fun' not in st.session_state: st.session_state.fun = 5000
if 'util' not in st.session_state: st.session_state.util = 4000
if 'misc' not in st.session_state: st.session_state.misc = 3000
if 'chat_history' not in st.session_state: st.session_state.chat_history = []

# Sidebar Navigation Panel - Using Beginner-Friendly Simplified Language Standard
page = st.sidebar.radio("Navigate Workspace", [
    "Dashboard", "AI Finance Coach", "Budget Planner", 
    "SIP Calculator", "EMI Calculator", "Goal Planner", 
    "Investments", "Reports"
])

# Global Aggregation Variable Set
total_expenses = st.session_state.rent + st.session_state.food + st.session_state.fun + st.session_state.util + st.session_state.misc
calculated_savings = st.session_state.income - total_expenses
savings_ratio = (calculated_savings / st.session_state.income) * 100 if st.session_state.income > 0 else 0
health_score, health_status = get_financial_health_score(savings_ratio, 25)

# ----------------- PAGE 1: DASHBOARD -----------------
if page == "Dashboard":
    st.markdown("<h1 style='margin-bottom: 4px;'>Welcome Back</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #6B7280; font-size: 16px; margin-bottom: 32px;'>Here's your money summary for today.</p>", unsafe_allow_html=True)
    
    # Premium Responsive Analytics Top Cards
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1: st.metric("Monthly Income", f"₹{st.session_state.income:,}")
    with col2: st.metric("Expenses", f"₹{total_expenses:,}")
    with col3: st.metric("Savings", f"₹{calculated_savings:,}")
    with col4: st.metric("Investments", f"₹{int(calculated_savings * 0.6):,}")
    with col5: st.metric("Financial Health Score", f"{health_score}/100", f"Status: {health_status}")
    
    st.write("---")
    
    # Insights Section Layout Block
    st.subheader("Smart Insights")
    ins_c1, ins_c2, ins_c3 = st.columns(3)
    with ins_c1:
        st.info(f"✨ You saved {savings_ratio:.0f}% of your total take-home income this month.")
    with ins_c2:
        st.warning("⚠️ How much of your income goes toward loans? Your debt payouts are currently slightly elevated.")
    with ins_c3:
        st.success("📈 Wealth builder action: Increase your automated monthly SIP by ₹2,000 to reach goals faster.")
        
    st.write("---")
    
    # Products & Tools Sections Layout (Groww Card Matrix Style Layout)
    st.subheader("Products & Tools")
    p_col1, p_col2, p_col3 = st.columns(3)
    with p_col1:
        st.markdown("""
            <div class="product-card">
                <div class="product-icon">💳</div>
                <div class="product-title">Budget Planner</div>
                <div class="product-desc">Track exactly where your money goes every single month and optimize your monthly utility habits instantly.</div>
            </div>
        """, unsafe_allow_html=True)
    with p_col2:
        st.markdown("""
            <div class="product-card">
                <div class="product-icon">📈</div>
                <div class="product-title">SIP Calculator</div>
                <div class="product-desc">See how small investments grow over time into large wealth using standard compounding equations.</div>
            </div>
        """, unsafe_allow_html=True)
    with p_col3:
        st.markdown("""
            <div class="product-card">
                <div class="product-icon">🏠</div>
                <div class="product-title">EMI Calculator</div>
                <div class="product-desc">Check out exactly how much your monthly loan installment options will look like before talking to banks.</div>
            </div>
        """, unsafe_allow_html=True)

    p_col4, p_col5, p_col6 = st.columns(3)
    with p_col4:
        st.markdown("""
            <div class="product-card">
                <div class="product-icon">🎯</div>
                <div class="product-title">Goal Planner</div>
                <div class="product-desc">Map out specific allocations for buying your dream home, vehicle assets, or emergency backup funds.</div>
            </div>
        """, unsafe_allow_html=True)
    with p_col5:
        st.markdown("""
            <div class="product-card">
                <div class="product-icon">💼</div>
                <div class="product-title">Investment Planner</div>
                <div class="product-desc">Where should you invest your money? Evaluate risk setups based on conservative or aggressive allocations.</div>
            </div>
        """, unsafe_allow_html=True)
    with p_col6:
        st.markdown("""
            <div class="product-card">
                <div class="product-icon">🛑</div>
                <div class="product-title">Debt Manager</div>
                <div class="product-desc">Organize multiple liabilities using accelerated paydown structures like the Avalanche methodology.</div>
            </div>
        """, unsafe_allow_html=True)

    st.write("---")
    
    # Modern Analytics Charts Matrix Block
    col_left, col_right = st.columns(2)
    with col_left:
        st.subheader("Where are you spending your money?")
        labels = ['Rent & Housing', 'Groceries & Food', 'Fun & Lifestyle', 'Connectivity/Utilities', 'Unplanned Extras']
        values = [st.session_state.rent, st.session_state.food, st.session_state.fun, st.session_state.util, st.session_state.misc]
        fig = px.pie(names=labels, values=values, hole=0.6, color_discrete_sequence=px.colors.sequential.Plotly3)
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#1F2937', margin=dict(t=20,b=20,l=20,r=20))
        st.plotly_chart(fig, use_container_width=True)
        
    with col_right:
        st.subheader("Your Progress Tracker")
        categories = ['Emergency Fund Reserve', 'Core Wealth Portfolio', 'Retirement Index Target']
        progress = [85, 45, 22]
        fig_bar = px.bar(x=progress, y=categories, orientation='h', range_x=[0, 100], color_discrete_sequence=['#1B5E20'])
        fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#1F2937', margin=dict(t=20,b=20,l=20,r=20))
        st.plotly_chart(fig_bar, use_container_width=True)

    st.write("---")
    
    # Quick Actions Framework and Daily Financial Quotes Component
    qa_col, tip_col = st.columns([2, 1])
    with qa_col:
        st.subheader("Quick Actions")
        q_c1, q_c2, q_c3, q_c4 = st.columns(4)
        with q_c1: st.button("➕ Add Expense")
        with q_c2: st.button("🚀 Start SIP")
        with q_c3: st.button("📑 Download Report")
        with q_c4: st.button("🔍 Check Loan Eligibility")
    with tip_col:
        st.subheader("Daily Money Tip")
        st.info("💬 *\"The best investment you can make is in yourself.\"*")

# ----------------- PAGE 2: AI FINANCE COACH -----------------
elif page == "AI Finance Coach":
    st.title("🤖 AI Finance Coach")
    st.write("Ask any question about balancing your cash flow, managing loans, or understanding compound interest.")
    
    user_query = st.text_input("Ask a question in plain English (e.g., 'Where should you invest your money?'):")
    if user_query:
        response = query_finmate_ai(user_query)
        st.write("---")
        st.markdown(f"**You:** {user_query}")
        st.markdown(f"**Coach:** {response}")
        st.write("---")

# ----------------- PAGE 3: BUDGET PLANNER -----------------
elif page == "Budget Planner":
    st.title("💳 Budget Planner")
    col_inputs, col_outputs = st.columns([1, 1])
    with col_inputs:
        st.subheader("Enter your numbers:")
        st.session_state.income = st.number_input("Monthly Income", value=st.session_state.income, step=5000)
        st.session_state.rent = st.number_input("Rent / Housing Cost", value=st.session_state.rent, step=1000)
        st.session_state.food = st.number_input("Groceries & Food", value=st.session_state.food, step=1000)
        st.session_state.fun = st.number_input("Entertainment & Fun", value=st.session_state.fun, step=500)
        st.session_state.util = st.number_input("Utilities & Internet", value=st.session_state.util, step=500)
        st.session_state.misc = st.number_input("Other Extra Expenses", value=st.session_state.misc, step=500)
        
    with col_outputs:
        st.subheader("Your Budget Analysis")
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
    st.title("📈 SIP Calculator")
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
    st.title("🏠 EMI Calculator")
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
    st.title("🎯 Goal Planner")
    g_type = st.selectbox("What are you saving up for?", ["Dream House Acquisition", "High Performance EV Car Purchase", "Global Family Vacation", "Children Higher Education Fund"])
    g_target = st.number_input("Target Amount Needed (₹)", value=2500000, step=50000)
    g_time = st.slider("Years left to reach this goal", 1, 25, 8)
    
    monthly_required = calculate_goal_required(g_target, g_time)
    st.success(f"💡 Target Milestone Strategy: To save enough for your **{g_type}**, you need to save **₹{monthly_required:,}** every single month.")

# ----------------- PAGE 7: INVESTMENTS -----------------
elif page == "Investments":
    st.title("💼 Where should you invest your money?")
    risk_appetite = st.selectbox("Choose your personal investing comfort level:", ["Conservative", "Moderate", "Aggressive"])
    target_alloc = get_asset_allocation(risk_appetite)
    
    fig_alloc = px.pie(names=list(target_alloc.keys()), values=list(target_alloc.values()), color_discrete_sequence=px.colors.sequential.Greens_r)
    fig_alloc.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#1F2937')
    st.plotly_chart(fig_alloc, use_container_width=True)
    
    st.subheader("Audit your current investments tracker:")
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
    st.title("📑 Performance Reports Studio")
    st.write("Review a clear structural breakdown of your real-time finance setups instantly.")
    
    text_summary = generate_report_summary(st.session_state.income, total_expenses, calculated_savings, health_score)
    st.text_area("Your Financial Diagnostic Matrix Statement Logs", value=text_summary, height=250)
    st.download_button(label="Download Text Statement", data=text_summary, file_name="FinMate_Statement.txt", mime="text/plain")
    
