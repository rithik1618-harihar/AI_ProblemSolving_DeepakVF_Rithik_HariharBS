"""
loan_approval.py
─────────────────────────────────────────────────────────────
Bank Loan Approval Prediction System
Algorithms : Logistic Regression (primary) + Random Forest + Decision Tree
Author     : AI Problem Solving Team
─────────────────────────────────────────────────────────────
Usage:
    python loan_approval.py                    # uses synthetic data
    python loan_approval.py --csv your.csv     # uses your CSV file
    python loan_approval.py --interactive      # manual console input
"""

import argparse
import sys
import os
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")           # non-interactive backend for saving plots
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection    import train_test_split, cross_val_score
from sklearn.preprocessing      import LabelEncoder, StandardScaler
from sklearn.linear_model       import LogisticRegression
from sklearn.ensemble           import RandomForestClassifier
from sklearn.tree               import DecisionTreeClassifier
from sklearn.metrics            import (
    accuracy_score, classification_report,
    confusion_matrix, roc_auc_score, roc_curve
)

# ──────────────────────────────────────────────
# 1. DATA LOADING
# ──────────────────────────────────────────────
def load_data(csv_path=None):
    if csv_path and os.path.exists(csv_path):
        print(f"📂  Loading dataset from: {csv_path}")
        df = pd.read_csv(csv_path)
    else:
        print("📊  Generating synthetic loan dataset …")
        from generate_dataset import generate_loan_dataset
        df = generate_loan_dataset()
    print(f"    Shape: {df.shape}\n")
    return df


# ──────────────────────────────────────────────
# 2. PRE-PROCESSING
# ──────────────────────────────────────────────
def preprocess(df, target_col="Loan_Status"):
    df = df.copy()

    # 2a. Handle missing values
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = df.select_dtypes(include=["object"]).columns.tolist()
    if target_col in cat_cols:
        cat_cols.remove(target_col)

    for c in num_cols:
        df[c] = df[c].fillna(df[c].median())
    for c in cat_cols:
        df[c] = df[c].fillna(df[c].mode()[0])

    print(f"✅  Missing values handled. Numeric cols: {num_cols}")

    # 2b. Encode categorical features
    le = LabelEncoder()
    for c in cat_cols:
        df[c] = le.fit_transform(df[c].astype(str))
        print(f"    Encoded '{c}'")

    # 2c. Encode target (handles both object and pandas StringDtype)
    if pd.api.types.is_string_dtype(df[target_col]) or df[target_col].dtype == object:
        unique_labels = sorted(df[target_col].dropna().unique())
        # Detect Approved/Rejected or generic binary labels
        if "Approved" in unique_labels and "Rejected" in unique_labels:
            df[target_col] = df[target_col].map({"Approved": 1, "Rejected": 0})
        else:
            df[target_col] = le.fit_transform(df[target_col].astype(str))

    X = df.drop(columns=[target_col])
    y = df[target_col]

    # 2d. Feature scaling
    scaler = StandardScaler()
    X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=X.columns)

    print(f"\n📐  Feature matrix shape : {X_scaled.shape}")
    print(f"    Class distribution   : {dict(y.value_counts())}\n")
    return X_scaled, y, scaler, X.columns.tolist()


# ──────────────────────────────────────────────
# 3. TRAIN & EVALUATE
# ──────────────────────────────────────────────
def train_models(X_train, X_test, y_train, y_test):
    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
        "Decision Tree"      : DecisionTreeClassifier(max_depth=6, random_state=42),
        "Random Forest"      : RandomForestClassifier(n_estimators=100, random_state=42),
    }

    results = {}
    print("═" * 60)
    print("  MODEL TRAINING & EVALUATION")
    print("═" * 60)

    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        acc    = accuracy_score(y_test, y_pred)
        try:
            auc = roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])
        except Exception:
            auc = None
        cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring="accuracy")

        results[name] = {
            "model"    : model,
            "accuracy" : acc,
            "auc"      : auc,
            "cv_mean"  : cv_scores.mean(),
            "cv_std"   : cv_scores.std(),
            "y_pred"   : y_pred,
        }

        print(f"\n🔷  {name}")
        print(f"    Test Accuracy     : {acc * 100:.2f}%")
        print(f"    ROC-AUC Score     : {auc:.4f}" if auc else "    ROC-AUC Score     : N/A")
        print(f"    CV Accuracy (5-fold): {cv_scores.mean()*100:.2f}% ± {cv_scores.std()*100:.2f}%")
        print(f"\n    Classification Report:\n")
        cr = classification_report(y_test, y_pred, target_names=["Rejected", "Approved"])
        for line in cr.split("\n"):
            print(f"    {line}")

    return results


# ──────────────────────────────────────────────
# 4. VISUALISATIONS
# ──────────────────────────────────────────────
def save_plots(results, X_test, y_test, feature_names, out_dir="plots"):
    os.makedirs(out_dir, exist_ok=True)
    palette = ["#e63946", "#2a9d8f"]

    # 4a. Confusion matrices
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    fig.suptitle("Confusion Matrices", fontsize=14, fontweight="bold")
    for ax, (name, res) in zip(axes, results.items()):
        cm = confusion_matrix(y_test, res["y_pred"])
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                    xticklabels=["Rejected", "Approved"],
                    yticklabels=["Rejected", "Approved"], ax=ax)
        ax.set_title(f"{name}\nAcc: {res['accuracy']*100:.1f}%")
        ax.set_ylabel("Actual")
        ax.set_xlabel("Predicted")
    plt.tight_layout()
    plt.savefig(f"{out_dir}/confusion_matrices.png", dpi=150)
    plt.close()

    # 4b. ROC curves
    fig, ax = plt.subplots(figsize=(7, 5))
    colors = ["#e63946", "#2a9d8f", "#457b9d"]
    for (name, res), color in zip(results.items(), colors):
        try:
            proba = res["model"].predict_proba(X_test)[:, 1]
            fpr, tpr, _ = roc_curve(y_test, proba)
            ax.plot(fpr, tpr, label=f"{name} (AUC={res['auc']:.3f})", color=color, lw=2)
        except Exception:
            pass
    ax.plot([0,1],[0,1],"k--", lw=1)
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_title("ROC Curves – All Models")
    ax.legend()
    plt.tight_layout()
    plt.savefig(f"{out_dir}/roc_curves.png", dpi=150)
    plt.close()

    # 4c. Feature importances (Random Forest)
    rf = results["Random Forest"]["model"]
    importances = pd.Series(rf.feature_importances_, index=feature_names).sort_values(ascending=True)
    fig, ax = plt.subplots(figsize=(8, 5))
    importances.plot(kind="barh", color="#2a9d8f", ax=ax)
    ax.set_title("Feature Importances (Random Forest)")
    ax.set_xlabel("Importance Score")
    plt.tight_layout()
    plt.savefig(f"{out_dir}/feature_importances.png", dpi=150)
    plt.close()

    # 4d. Model accuracy comparison
    names = list(results.keys())
    accs  = [results[n]["accuracy"]*100 for n in names]
    fig, ax = plt.subplots(figsize=(7, 4))
    bars = ax.bar(names, accs, color=["#e63946","#2a9d8f","#457b9d"], width=0.5)
    for bar, acc in zip(bars, accs):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() - 3,
                f"{acc:.1f}%", ha="center", va="top", color="white", fontweight="bold")
    ax.set_ylim(0, 110)
    ax.set_ylabel("Accuracy (%)")
    ax.set_title("Model Accuracy Comparison")
    plt.tight_layout()
    plt.savefig(f"{out_dir}/model_comparison.png", dpi=150)
    plt.close()

    print(f"\n📊  Plots saved to '{out_dir}/' folder.")


# ──────────────────────────────────────────────
# 5. INTERACTIVE PREDICTION
# ──────────────────────────────────────────────
def interactive_predict(model, scaler, feature_names):
    print("\n" + "═"*60)
    print("  INTERACTIVE LOAN PREDICTION")
    print("═"*60)
    print("Enter applicant details (press Enter to use defaults):\n")

    defaults = {
        "Age"              : 35,
        "Annual_Income"    : 60000,
        "Credit_Score"     : 700,
        "Loan_Amount"      : 50000,
        "Loan_Term_Months" : 36,
        "Employment_Status": 0,   # 0=Employed encoded
        "Num_Dependents"   : 1,
        "Existing_Loans"   : 0,
    }

    inputs = {}
    for feat in feature_names:
        default = defaults.get(feat, 0)
        try:
            val = input(f"  {feat} [{default}]: ").strip()
            inputs[feat] = float(val) if val else float(default)
        except ValueError:
            inputs[feat] = float(default)

    X_new = pd.DataFrame([inputs])
    X_new_scaled = scaler.transform(X_new)
    pred = model.predict(X_new_scaled)[0]
    prob = model.predict_proba(X_new_scaled)[0]

    result = "✅  APPROVED" if pred == 1 else "❌  REJECTED"
    print(f"\n{'─'*40}")
    print(f"  Prediction  : {result}")
    print(f"  Confidence  : Approved={prob[1]*100:.1f}%  Rejected={prob[0]*100:.1f}%")
    print(f"{'─'*40}\n")


# ──────────────────────────────────────────────
# 6. SAMPLE PREDICTIONS
# ──────────────────────────────────────────────
def sample_predictions(model, X_test, y_test, feature_names, n=5):
    """Show predictions for n test applicants (mix of approved & rejected)."""
    print("\n" + "═"*60)
    print("  SAMPLE TEST APPLICANTS – PREDICTED vs ACTUAL")
    print("═"*60)

    y_arr   = np.array(y_test)
    app_idx = np.where(y_arr == 1)[0]
    rej_idx = np.where(y_arr == 0)[0]

    # Pick roughly half approved, half rejected
    n_app = min(n // 2 + n % 2, len(app_idx))
    n_rej = min(n - n_app, len(rej_idx))
    chosen = np.concatenate([
        np.random.choice(app_idx, n_app, replace=False),
        np.random.choice(rej_idx, n_rej, replace=False),
    ])
    np.random.shuffle(chosen)

    X_sample = X_test.iloc[chosen]
    y_sample = y_test.iloc[chosen]

    preds = model.predict(X_sample)
    probs = model.predict_proba(X_sample)

    correct = 0
    for i, (pred, actual, prob) in enumerate(zip(preds, y_sample, probs)):
        pred_label   = "✅ APPROVED" if pred == 1 else "❌ REJECTED"
        actual_label = "Approved"   if actual == 1 else "Rejected"
        match        = "✓" if pred == actual else "✗"
        correct     += int(pred == actual)
        print(f"\n  👤 Applicant {i+1}")
        print(f"     Predicted : {pred_label}  (conf: {max(prob)*100:.1f}%)")
        print(f"     Actual    : {actual_label}  {match}")

    print(f"\n  Sample Accuracy: {correct}/{len(preds)} correct\n")


# ──────────────────────────────────────────────
# 7. MAIN
# ──────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Loan Approval Prediction System")
    parser.add_argument("--csv",         type=str,  default=None, help="Path to CSV dataset")
    parser.add_argument("--interactive", action="store_true",     help="Manually enter applicant details")
    parser.add_argument("--no-plots",    action="store_true",     help="Skip saving plots")
    args = parser.parse_args()

    print("\n" + "═"*60)
    print("  🏦  BANK LOAN APPROVAL PREDICTION SYSTEM")
    print("  AI Problem Solving Assignment")
    print("═"*60 + "\n")

    # Load & preprocess
    df = load_data(args.csv)
    X, y, scaler, feature_names = preprocess(df)

    # Train/test split (80/20)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    X_train = X_train.reset_index(drop=True)
    X_test  = X_test.reset_index(drop=True)
    y_train = y_train.reset_index(drop=True)
    y_test  = y_test.reset_index(drop=True)
    print(f"🔀  Train size: {len(X_train)}  |  Test size: {len(X_test)}\n")

    # Train & evaluate all models
    results = train_models(X_train, X_test, y_train, y_test)

    # Save plots
    if not args.no_plots:
        save_plots(results, X_test, y_test, feature_names)

    # Best model = Logistic Regression (assignment requirement)
    best_model = results["Logistic Regression"]["model"]

    # Sample predictions
    sample_predictions(best_model, X_test, y_test, feature_names)

    # Interactive mode
    if args.interactive:
        while True:
            interactive_predict(best_model, scaler, feature_names)
            again = input("  Predict another? (y/n): ").strip().lower()
            if again != "y":
                break

    print("\n✅  Done! Check 'plots/' folder for visualisations.\n")


if __name__ == "__main__":
    main()
