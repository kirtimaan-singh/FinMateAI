def get_asset_allocation(profile_type):
    allocations = {
        "Conservative": {"Equity": 30, "Debt": 60, "Gold": 10},
        "Moderate": {"Equity": 60, "Debt": 30, "Gold": 10},
        "Aggressive": {"Equity": 80, "Debt": 10, "Gold": 10}
    }
    return allocations.get(profile_type, allocations["Moderate"])

def evaluate_portfolio(current_portfolio, profile_type):
    target = get_asset_allocation(profile_type)
    suggestions = []
    for asset, target_pct in target.items():
        curr_pct = current_portfolio.get(asset, 0)
        diff = curr_pct - target_pct
        if diff > 15:
            suggestions.append(f"⚠️ Overexposed to {asset}. Consider rebalancing toward under-allocated segments.")
        elif diff < -15:
            suggestions.append(f"📉 Underexposed to {asset}. Increase allocations here to meet your strategic path.")
    if not suggestions:
        suggestions.append("🌟 Your portfolio aligns beautifully with your risk targets!")
    return suggestions
