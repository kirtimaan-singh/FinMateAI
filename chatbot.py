%%writefile FinMateAI/app.py
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

# Set up native Streamlit config layout
st.set_page_config(page_title="FinMate AI", layout="wide")

# Safe HTML styling injector using standard raw components
st.components.v1.html(
    """
    <style>
    body { background-color: #0B0F19; color: #FFFFFF; }
    h1, h2, h3, h4, h5, h6 { color: #00D09C !important; }
    </style>
    """,
    height=0
)

# Application Context/Session Management System Initialization
if 'income' not in st.session_state: st.session_state.income = 75000
if 'rent' not in st.session_state: st.session_state.rent = 15000
if 'food' not in st.session_state: st.session_state.food = 8000
if 'fun' not in st.session_state: st.session_state.fun = 5000
if 'util' not in st.session_state: st.session_state.util = 4000
if 'misc' not in st.session_state: st.session_state.misc = 3000
if 'chat_history' not in st.session_state: st.session_state.chat_history = []

# Sidebar Navigation Panel
st.sidebar.title("💚 FinMate AI")
st.sidebar.markdown("*Your Intelligent Wealth Companion*")
page = st.sidebar.radio("Navigate Workspace", [
    "📊 Home Dashboard", "🤖 AI Financial Assistant", "💳 Budget Planner", 
    "📈 SIP & Investment Engine", "🏠 Loan EMI Analyzer", "🎯 Goal & FIRE Planner", 
    "💼 Portfolio & Risk Center", "📑 Performance Reports"
])

# Global Aggregation Variable Set
total_expenses = st.session_state.rent + st.session_state.food + st.session_state.fun + st.session_state.util + st.session_state.misc
calculated_savings = st.session_state.income - total_expenses
savings_ratio = (calculated_savings / st.session_state.income) * 100 if st.session_state.income > 0 else 0
health_score, health_status = get_financial_health_score(savings_ratio, 25)

# ----------------- PAGE 1: HOME DASHBOARD -----------------
if page == "📊 Home Dashboard":
    st.title("Welcome back to FinMate AI Dashboard")
    st.markdown("💡 *Daily Financial Tip: Automated investing eliminates behavioral biases. Set up your recurring SIPs early in the month!*")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Monthly Net Income", f"₹{st.session_state.income:,}")
    with col2: st.metric("Tracked Outflows", f"₹{total_expenses:,}", delta=f"-{(total_expenses/st.session_state.income)*100:.1f}% Allocation", delta_color="inverse")
    with col3: st.metric("Projected Savings", f"₹{calculated_savings:,}", delta=f"{savings_ratio:.1f}% Saved")
    with col4: st.metric("Financial Health Index", f"{health_score}/100", f"Status: {health_status}")
    
    st.write("---")
    col_left, col_right = st.columns(2)
    with col_left:
        st.subheader("Current Expense Architecture")
        labels = ['Rent', 'Food', 'Entertainment', 'Utilities', 'Miscellaneous']
        values = [st.session_state.rent, st.session_state.food, st.session_state.fun, st.session_state.util, st.session_state.misc]
        fig = px.pie(names=labels, values=values, hole=0.4, color_discrete_sequence=px.colors.sequential.Mint)
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white')
        st.plotly_chart(fig, use_container_width=True)
        
    with col_right:
        st.subheader("Dynamic Milestones Progress")
        categories = ['Emergency Fund Reserve', 'Core Wealth Portfolio', 'Retirement Index Target']
        progress = [85, 45, 22]
        fig_bar = px.bar(x=progress, y=categories, orientation='h', range_x=[0, 100], color_discrete_sequence=['#00D09C'])
        fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white')
        st.plotly_chart(fig_bar, use_container_width=True)

# ----------------- PAGE 2: AI FINANCIAL ASSISTANT -----------------
elif page == "🤖 AI Financial Assistant":
    st.title("🤖 FinMate Intelligent AI Consultant")
    st.write("Ask any financial question covering allocations, optimization strategies, compound interest mechanisms, or debt planning.")
    
    # Fallback layout to bypass red TypeError chunk asset load errors on Localtunnel
    user_query = st.text_input("Enter your transaction, budget strategy, or wealth query and press Enter:")
    if user_query:
        response = query_finmate_ai(user_query)
        st.write("---")
        st.markdown(f"**You:** {user_query}")
        st.markdown(f"**FinMate AI:** {response}")
        st.write("---")

# ----------------- PAGE 3: BUDGET PLANNER -----------------
elif page == "💳 Budget Planner":
    st.title("💳 Smart Expense Engineering Studio")
    
    col_inputs, col_outputs = st.columns([1, 1])
    with col_inputs:
        st.subheader("Modify Core Parameters")
        st.session_state.income = st.number_input("Monthly Disposable Base Income", value=st.session_state.income, step=5000)
        st.session_state.rent = st.number_input("Fixed Rent / Housing Outflow", value=st.session_state.rent, step=1000)
        st.session_state.food = st.number_input("Groceries & Food Supplies", value=st.session_state.food, step=1000)
        st.session_state.fun = st.number_input("Discretionary Entertainment / Lifestyle", value=st.session_state.fun, step=500)
        st.session_state.util = st.number_input("Utilities, Gadgets & Connectivity", value=st.session_state.util, step=500)
        st.session_state.misc = st.number_input("Unplanned Miscellaneous Outflows", value=st.session_state.misc, step=500)
        
    with col_outputs:
        st.subheader("Optimization Analysis Metrics")
        sav, pct, recs = get_budget_recommendations(st.session_state.income, {
            'Rent': st.session_state.rent, 'Food': st.session_state.food,
            'Entertainment': st.session_state.fun, 'Utilities': st.session_state.util,
            'Miscellaneous': st.session_state.misc
        })
        st.metric("Disposable Surplus Capital Available", f"₹{sav:,}", f"{pct:.1f}% Net Savings Rate")
        
        st.write("### Tactical Adjustments Engine")
        for rec in recs:
            st.info(rec)

# ----------------- PAGE 4: SIP & INVESTMENT ENGINE -----------------
elif page == "📈 SIP & Investment Engine":
    st.title("📈 Systematic Investment Wealth Generator")
    
    c1, c2, c3 = st.columns(3)
    with c1: monthly_sip = st.slider("Target Monthly SIP Allocation (₹)", 1000, 100000, 10000, step=1000)
    with c2: expected_return = st.slider("Expected Long-Term Return Multiplier (%)", 5.0, 22.0, 12.0, step=0.5)
    with c3: horizon_years = st.slider("Investment Compounding Horizon (Years)", 1, 40, 15)
    
    invested, wealth, total_value = calculate_sip(monthly_sip, expected_return, horizon_years)
    
    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1: st.metric("Principal Investment Outlay", f"₹{invested:,}")
    with col_m2: st.metric("Compounded Return Growth Created", f"₹{wealth:,}")
    with col_m3: st.metric("Total Projected Portfolio Net Value", f"₹{total_value:,}")
    
    st.write("### Multi-Tiered Projection Simulator (Alternative Commitments)")
    benchmarks = [5000, 10000, 20000]
    sim_data = []
    for b in benchmarks:
        _, _, val = calculate_sip(b, expected_return, horizon_years)
        sim_data.append({"Monthly Allocation": f"₹{b:,}", "Final Wealth Value": val})
    
    df_sim = pd.DataFrame(sim_data)
    fig_sim = px.bar(df_sim, x="Monthly Allocation", y="Final Wealth Value", color="Final Wealth Value", color_continuous_scale='Mint')
    fig_sim.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white')
    st.plotly_chart(fig_sim, use_container_width=True)

# ----------------- PAGE 5: LOAN EMI ANALYZER -----------------
elif page == "🏠 Loan EMI Analyzer":
    st.title("🏠 Strategic Debt & EMI Structuring Terminal")
    
    l_col, r_col = st.columns(2)
    with l_col:
        p = st.number_input("Target Loan Principal Amount (₹)", value=500000, step=50000)
        r = st.slider("Annual Pricing Rate Percentage (%)", 4.0, 24.0, 9.5, step=0.1)
        t = st.slider("Target Repayment Tenure Structure (Years)", 1, 30, 7)
        
        emi, interest, total_pay = calculate_emi(p, r, t)
    with r_col:
        st.metric("Equated Monthly Installment (EMI Obligation)", f"₹{emi:,}")
        st.metric("Accumulated Interest Payload Cost", f"₹{interest:,}")
        st.metric("Total Comprehensive Lifecycle Capital Outlay", f"₹{total_pay:,}")
        
    fig_emi = px.pie(names=['Principal Core Component', 'Accumulated Interest Burden'], values=[p, interest], color_discrete_sequence=['#00D09C', '#FF4B4B'])
    fig_emi.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white')
    st.plotly_chart(fig_emi, use_container_width=True)

# ----------------- PAGE 6: GOAL & FIRE PLANNER -----------------
elif page == "🎯 Goal & FIRE Planner":
    st.title("🎯 Goal Setting & Financial Independence (FIRE) Compass")
    
    tab1, tab2 = st.tabs(["🎯 Milestones Mapping Engine", "🔥 Financial Freedom (FIRE) Path"])
    with tab1:
        g_type = st.selectbox("Define Long Term Milestones Strategy", ["Dream Home Acquisition", "High Performance EV Car Purchase", "Global Vacation Matrix", "Premium Higher Education Sinking Fund"])
        g_target = st.number_input("Target Capital Goal Required (₹)", value=2500000, step=50000)
        g_time = st.slider("Milestone Timeline Target Horizon (Years)", 1, 25, 8)
        
        monthly_required = calculate_goal_required(g_target, g_time)
        st.success(f"💡 To secure your target for **{g_type}**, you must allocate a compounding equivalent monthly savings contribution of **₹{monthly_required:,}**.")
        
    with tab2:
        st.subheader("Financial Independence Retire Early Metric Terminal")
        cur_age = st.number_input("Your Present Age", min_value=18, max_value=100, value=28)
        ann_exp = st.number_input("Annual Household Basic Survival Expenses (₹)", value=400000, step=25000)
        cur_sav = st.number_input("Liquid Capital Investment Base Already Accrued (₹)", value=500000, step=50000)
        m_inv = st.number_input("Active Monthly Compounding Savings Commitment (₹)", value=25000, step=2000)
        
        years_needed, corpus_needed = calculate_fire(cur_age, ann_exp, cur_sav, m_inv)
        
        st.metric("Target Complete Financial Freedom Independence Corpus", f"₹{corpus_needed:,}")
        st.warning(f"⌛ Based on modern compound trajectories, you are approximately **{years_needed} Years** away from cross-indexing complete financial choice independence.")

# ----------------- PAGE 7: PORTFOLIO & RISK CENTER -----------------
elif page == "💼 Portfolio & Risk Center":
    st.title("💼 Quantitative Portfolio Risk Assessment & Diversification Audit")
    
    risk_appetite = st.selectbox("Determine Core Behavioral Risk Tolerance Profile", ["Conservative", "Moderate", "Aggressive"])
    target_alloc = get_asset_allocation(risk_appetite)
    
    st.write(f"### Optimal Strategy Configuration Benchmark: {risk_appetite}")
    fig_alloc = px.pie(names=list(target_alloc.keys()), values=list(target_alloc.values()), color_discrete_sequence=px.colors.sequential.Darkmint)
    fig_alloc.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white')
    st.plotly_chart(fig_alloc, use_container_width=True)
    
    st.subheader("Instant Portfolio Diversification Auditor Engine")
    eq = st.slider("Current Equity Allocation Ratio (%)", 0, 100, 50)
    db = st.slider("Current Fixed Income Debt Ratio (%)", 0, 100, 40)
    gd = st.slider("Current Gold / Commodity Allocation Ratio (%)", 0, 100, 10)
    
    if (eq + db + gd) != 100:
        st.error("⚠️ Error: The total allocated portfolio matrix percentage must sum up to exactly 100%. Adjust sliders.")
    else:
        audit_results = evaluate_portfolio({"Equity": eq, "Debt": db, "Gold": gd}, risk_appetite)
        for feedback in audit_results:
            st.info(feedback)

# ----------------- PAGE 8: PERFORMANCE REPORTS -----------------
elif page == "📑 Performance Reports":
    st.title("📑 Algorithmic Wealth & Performance Statement Generator")
    st.write("Review structured breakdowns of your real-time configurations instantly.")
    
    text_summary = generate_report_summary(st.session_state.income, total_expenses, calculated_savings, health_score)
    st.text_area("Generated Structural Diagnostic Matrix Logs", value=text_summary, height=250)
    
    st.download_button(
        label="Download Plaintext Financial Integrity Statement",
        data=text_summary,
        file_name="FinMate_Financial_Integrity_Statement.txt",
        mime="text/plain"
    )
  
