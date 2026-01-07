def make_decision(score):
    if score >= 70:
        return "MATCHED"
    elif score >= 40:
        return "PARTIALLY MATCHED"
    else:
        return "NOT MATCHED"
