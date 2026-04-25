# 🏦 AI Problem Solving – Loan Approval Prediction

> **AI Problem Solving Assignment** | Classification using Machine Learning

---

## 📌 Problem Description

A bank wants to automate its loan approval process. Given applicant details such as income, credit score, employment status, and loan amount, this system predicts whether a loan should be **Approved** or **Rejected** using machine learning classification algorithms.

---

## 🧠 Algorithms Used

| Algorithm | Purpose |
|---|---|
| **Logistic Regression** | Primary classifier (linear decision boundary) |
| **Decision Tree** | Interpretable rule-based classifier |
| **Random Forest** | Ensemble method for higher accuracy |

All models are evaluated with:
- Test Accuracy
- ROC-AUC Score
- 5-Fold Cross-Validation
- Confusion Matrix
- Classification Report (Precision, Recall, F1)

---

## 📂 Folder Structure

```
loan_approval/
├── loan_approval.py       # Main ML pipeline
├── generate_dataset.py    # Synthetic dataset generator
├── loan_dataset.csv       # Auto-generated dataset (1000 rows)
├── plots/
│   ├── confusion_matrices.png
│   ├── roc_curves.png
│   ├── feature_importances.png
│   └── model_comparison.png
└── requirements.txt
```

---

## 🗃️ Dataset

### Features (Input Variables – min. 4 required)

| Feature | Type | Description |
|---|---|---|
| `Age` | Numeric | Applicant's age (22–65) |
| `Annual_Income` | Numeric | Annual income in ₹ / $ |
| `Credit_Score` | Numeric | CIBIL / FICO score (300–850) |
| `Loan_Amount` | Numeric | Requested loan amount |
| `Loan_Term_Months` | Numeric | Repayment duration |
| `Employment_Status` | Categorical | Employed / Self-Employed / Unemployed / Retired |
| `Num_Dependents` | Numeric | Number of dependents |
| `Existing_Loans` | Numeric | Number of active loans |

### Target Variable

| Variable | Values |
|---|---|
| `Loan_Status` | `Approved` / `Rejected` |

> Dataset is synthetically generated with realistic approval logic. You can also supply your own CSV from [Kaggle – Loan Approval Dataset](https://www.kaggle.com/datasets/architsharma01/loan-approval-prediction-dataset).

---

## ⚙️ Execution Steps

### 1. Install dependencies
```bash
pip install pandas numpy scikit-learn matplotlib seaborn
```

### 2. Run with synthetic data (default)
```bash
python loan_approval.py
```

### 3. Run with your own CSV file
```bash
python loan_approval.py --csv your_dataset.csv
```

### 4. Interactive console prediction
```bash
python loan_approval.py --interactive
```

### 5. Generate dataset only
```bash
python generate_dataset.py
```

---

## 📊 Sample Output

```
═══════════════════════════════════════════════════════════
  🏦  BANK LOAN APPROVAL PREDICTION SYSTEM
═══════════════════════════════════════════════════════════

📊  Generating synthetic loan dataset …
    Shape: (1000, 9)

✅  Missing values handled.

🔷  Logistic Regression
    Test Accuracy     : 87.50%
    ROC-AUC Score     : 0.9312
    CV Accuracy (5-fold): 86.88% ± 1.23%

    Classification Report:
              precision    recall  f1-score
    Rejected     0.88      0.91      0.89
    Approved     0.87      0.83      0.85

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  SAMPLE TEST APPLICANTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  👤 High Earner, Great Credit
     → ✅ APPROVED  (confidence: 96.3%)

  👤 Low Income, Poor Credit
     → ❌ REJECTED  (confidence: 91.7%)

  👤 Mid Income, Average Credit
     → ✅ APPROVED  (confidence: 73.2%)

  👤 Unemployed, High Loan Ask
     → ❌ REJECTED  (confidence: 88.5%)

  👤 Retiree, Low Loan
     → ✅ APPROVED  (confidence: 82.1%)
```

---

## 📈 Data Preprocessing Steps

1. **Missing Value Handling** – Numeric columns filled with median; categorical with mode
2. **Label Encoding** – Categorical variables (`Employment_Status`) encoded to integers
3. **Feature Scaling** – StandardScaler applied to normalise all numeric features
4. **Train-Test Split** – 80% training / 20% testing with stratification

---

## 👥 Team Members

| Name | Roll No |
|---|---|
| Member 1 | XXXXXX |
| Member 2 | XXXXXX |

---

## 📚 References

- [Scikit-learn Documentation](https://scikit-learn.org/)
- [Kaggle – Loan Approval Datasets](https://www.kaggle.com/datasets/architsharma01/loan-approval-prediction-dataset)
- [Logistic Regression – StatQuest](https://www.youtube.com/watch?v=yIYKR4sgzI8)
