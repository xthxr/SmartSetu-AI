import numpy as np

def calculate_credit_score(transactions, consistency, supplier_verified, testimonials, max_txn):
    supplier_val = 100 if str(supplier_verified).strip().lower() == "yes" else 0
    testimonial_score = (testimonials / 10) * 100
    normalized_txn = (transactions / max_txn) * 100 if max_txn > 0 else 0

    score = (
        0.4 * normalized_txn +
        0.3 * consistency +
        0.2 * supplier_val +
        0.1 * testimonial_score
    )

    return round(min(100, max(0, score)), 2)

def calculate_risk_score(expenses, avg_income):
    if avg_income == 0:
        return 100
    variance = np.std(expenses)
    return round((variance / avg_income) * 100, 2)

def get_risk_level(score):
    if score < 20:
        return "Low Risk"
    elif score <= 50:
        return "Medium Risk"
    else:
        return "High Risk"
