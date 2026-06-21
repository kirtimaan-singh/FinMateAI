import numpy as np

def calculate_sip(monthly_investment, rate, years):
    i = (rate / 100) / 12
    n = years * 12
    total_investment = monthly_investment * n
    future_value = monthly_investment * (((1 + i)**n - 1) / i) * (1 + i)
    wealth_created = future_value - total_investment
    return round(total_investment, 2), round(wealth_created, 2), round(future_value, 2)

def calculate_emi(principal, rate, tenure_years):
    r = (rate / 100) / 12
    n = tenure_years * 12
    if r == 0: return principal / n, 0, principal
    emi = principal * r * ((1 + r)**n) / (((1 + r)**n) - 1)
    total_repayment = emi * n
    total_interest = total_repayment - principal
    return round(emi, 2), round(total_interest, 2), round(total_repayment, 2)

def calculate_retirement(current_age, retirement_age, monthly_expenses, inflation=6, returns=12):
    years_to_retire = retirement_age - current_age
    adjusted_expenses = monthly_expenses * ((1 + (inflation/100)) ** years_to_retire)
    target_corpus = adjusted_expenses * 12 * 25
    
    i = (returns / 100) / 12
    n = years_to_retire * 12
    if n <= 0: return 0, 0
    monthly_savings = target_corpus / ((((1 + i)**n - 1) / i) * (1 + i))
    return round(target_corpus, 2), round(monthly_savings, 2)

def calculate_fire(current_age, annual_expenses, current_savings, monthly_investment, expected_return=12):
    target_corpus = annual_expenses * 25
    shortfall = target_corpus - current_savings
    if shortfall <= 0:
        return 0, target_corpus
    
    i = expected_return / 100 / 12
    months = 0
    balance = current_savings
    while balance < target_corpus and months < 600:
        balance = balance * (1 + i) + monthly_investment
        months += 1
    return round(months / 12, 1), round(target_corpus, 2)
