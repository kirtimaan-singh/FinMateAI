def calculate_goal_required(target_amount, timeline_years, expected_return=10):
    months = timeline_years * 12
    i = (expected_return / 100) / 12
    if i == 0: return target_amount / months
    monthly_needed = target_amount / ((((1 + i)**months - 1) / i) * (1 + i))
    return round(monthly_needed, 2)
