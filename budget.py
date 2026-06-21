import streamlit as st

def get_budget_recommendations(income, expenses_dict):
    total_expenses = sum(expenses_dict.values())
    savings = income - total_expenses
    savings_pct = (savings / income) * 100 if income > 0 else 0
    
    recommendations = []
    if savings_pct < 20:
        recommendations.append("⚠️ Your savings rate is below the recommended 20%. Try optimizing entertainment or miscellaneous costs.")
    else:
        recommendations.append("✅ Excellent job! You are maintaining a strong savings rate.")
        
    needs = expenses_dict.get('Rent', 0) + expenses_dict.get('Food', 0) + expenses_dict.get('Utilities', 0)
    wants = expenses_dict.get('Entertainment', 0) + expenses_dict.get('Transportation', 0) + expenses_dict.get('Miscellaneous', 0)
    
    needs_pct = (needs / income) * 100 if income > 0 else 0
    wants_pct = (wants / income) * 100 if income > 0 else 0
    
    recommendations.append(f"📊 50/30/20 Rule Analysis: Your Needs: {needs_pct:.1f}%, Wants: {wants_pct:.1f}%, Savings: {savings_pct:.1f}%")
    return savings, savings_pct, recommendations
