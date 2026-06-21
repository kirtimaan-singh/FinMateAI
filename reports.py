import pandas as pd

def generate_report_summary(income, expenses, savings, health_score):
    summary = f"""
    === FINMATE AI MONTHLY FINANCIAL SUMMARY ===
    Report Base Income: ₹{income:,}
    Tracked Outflows: ₹{expenses:,}
    Calculated Net Savings: ₹{savings:,}
    Algorithmic Health Score: {health_score}/100
    ===========================================
    Advice Note: Maintain tracking structures weekly to stay disciplined.
    """
    return summary
