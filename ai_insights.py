import requests

def get_financial_health_score(savings_ratio, debt_to_income, profile_completed=True):
    score = 40
    if savings_ratio >= 20: score += 20
    elif savings_ratio >= 10: score += 10
    
    if debt_to_income <= 30: score += 20
    elif debt_to_income <= 45: score += 10
    
    if profile_completed: score += 20
    
    if score >= 80: status = "Excellent"
    elif score >= 60: status = "Good"
    elif score >= 40: status = "Average"
    else: status = "Poor"
    
    return score, status

def query_finmate_ai(prompt, fallback_context=""):
    prompt = prompt.lower()
    if "sip" in prompt or "crore" in prompt:
        return "To target standard growth goals like ₹1 Crore over 15 years, a monthly compounding SIP of roughly ₹20,000 to ₹25,000 at a 12% expected return is generally optimal."
    if "budget" in prompt or "earn" in prompt:
        return "Adhering to the 50/30/20 allocation standard (50% Essential Needs, 30% Lifestyle Wants, 20% Financial Savings) is an excellent automated blueprint."
    if "debt" in prompt or "repay" in prompt:
        return "Prioritize liquidating higher-interest unsecured debts (like Credit Cards) using the Avalanche method before aggressively indexing heavy capital into long-term investments."
    return f"Based on your profile matrix: consistency beats timing. Make sure to hold a liquid emergency reserve spanning 6 months of absolute expenses before scaling equity configurations."
