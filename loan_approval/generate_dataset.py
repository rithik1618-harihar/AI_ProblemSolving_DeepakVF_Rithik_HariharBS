"""
generate_dataset.py
Generates a synthetic loan approval dataset with realistic distributions.
Minimum 4 input variables + 1 target variable (Approved/Rejected).
"""

import pandas as pd
import numpy as np

def generate_loan_dataset(n_samples=1200, random_state=42, save_path="loan_dataset.csv"):
    np.random.seed(random_state)

    # --- Feature Generation ---
    age             = np.random.randint(22, 65, n_samples)
    annual_income   = np.random.randint(20000, 200000, n_samples)
    credit_score    = np.random.randint(300, 850, n_samples)
    loan_amount     = np.random.randint(5000, 500000, n_samples)
    loan_term       = np.random.choice([12, 24, 36, 48, 60, 120], n_samples)
    employment_status = np.random.choice(
        ["Employed", "Self-Employed", "Unemployed", "Retired"],
        n_samples, p=[0.55, 0.25, 0.12, 0.08]
    )
    num_dependents  = np.random.randint(0, 6, n_samples)
    existing_loans  = np.random.randint(0, 5, n_samples)

    # --- Approval Logic (rule-based with noise) ---
    score = np.zeros(n_samples)
    score += (credit_score - 300) / 550 * 40        # credit score  → up to +40
    score += np.clip(annual_income / 200000, 0, 1) * 25  # income        → up to +25
    score -= (loan_amount / annual_income) * 10     # debt ratio    → penalty
    score += np.where(employment_status == "Employed", 10,
             np.where(employment_status == "Self-Employed", 5,
             np.where(employment_status == "Retired", 3, -10)))
    score -= existing_loans * 3
    score -= num_dependents * 1
    score += np.random.normal(0, 5, n_samples)      # realistic noise

    # Normalise score to get ~40-45% approval rate (realistic for banks)
    threshold = np.percentile(score, 58)          # top 42% get approved
    approved  = (score >= threshold).astype(int)

    df = pd.DataFrame({
        "Age":               age,
        "Annual_Income":     annual_income,
        "Credit_Score":      credit_score,
        "Loan_Amount":       loan_amount,
        "Loan_Term_Months":  loan_term,
        "Employment_Status": employment_status,
        "Num_Dependents":    num_dependents,
        "Existing_Loans":    existing_loans,
        "Loan_Status":       np.where(approved == 1, "Approved", "Rejected"),
    })

    df.to_csv(save_path, index=False)
    print(f"✅  Dataset saved → {save_path}  ({n_samples} rows)")
    print(f"    Approved : {approved.sum()}  |  Rejected : {n_samples - approved.sum()}")
    return df


if __name__ == "__main__":
    generate_loan_dataset()
