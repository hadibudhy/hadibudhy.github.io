"""
Fake Job Postings — ML Pipeline
Target: fraudulent (0/1), ~4.8% positive (imbalanced)
Models: Logistic Regression (TF-IDF), Random Forest, LightGBM
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report, confusion_matrix,
    roc_auc_score, average_precision_score,
    precision_recall_curve, RocCurveDisplay
)
from sklearn.base import BaseEstimator, TransformerMixin
import lightgbm as lgb
import xgboost as xgb

# ── helpers ─────────────────────────────────────────────────────────────────

sys_path = "D:/Agent/ai-analyst"

def swd_style():
    plt.rcParams.update({
        "font.family": "sans-serif",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.alpha": 0.3,
        "figure.dpi": 120,
    })

swd_style()

# ── 1. Load ──────────────────────────────────────────────────────────────────

df = pd.read_csv(f"{sys_path}/data/fake_job_postings.csv")
print(f"Loaded: {df.shape[0]:,} rows | fraudulent rate: {df.fraudulent.mean():.1%}")

# ── 2. Feature Engineering ───────────────────────────────────────────────────

TEXT_COLS = ["title", "company_profile", "description", "requirements", "benefits"]

# Combine all text fields into one
df["text_all"] = df[TEXT_COLS].fillna("").agg(" ".join, axis=1)

# Text-derived numeric features
df["text_len"]        = df["text_all"].str.len()
df["word_count"]      = df["text_all"].str.split().str.len()
df["has_salary"]      = df["salary_range"].notna().astype(int)
df["has_dept"]        = df["department"].notna().astype(int)
df["has_profile"]     = df["company_profile"].notna().astype(int)
df["has_requirements"] = df["requirements"].notna().astype(int)
df["missing_count"]   = df[TEXT_COLS].isna().sum(axis=1)

# Suspicious text flags
df["has_url"]         = df["text_all"].str.contains(r"http|www\.|\.com", case=False, regex=True).astype(int)
df["has_phone"]       = df["text_all"].str.contains(r"\d{3}[-.\s]\d{3}", regex=True).astype(int)
df["exclamation_ct"]  = df["text_all"].str.count(r"!")
df["caps_ratio"]      = df["text_all"].apply(
    lambda x: sum(1 for c in x if c.isupper()) / max(len(x), 1)
)

# Categorical → int (simple label encode; many NaNs → "missing" category)
CAT_COLS = ["employment_type", "required_experience", "required_education",
            "industry", "function"]
for col in CAT_COLS:
    df[col] = df[col].fillna("missing")
    df[col] = LabelEncoder().fit_transform(df[col])

TABULAR_FEATURES = [
    "telecommuting", "has_company_logo", "has_questions",
    "text_len", "word_count", "has_salary", "has_dept",
    "has_profile", "has_requirements", "missing_count",
    "has_url", "has_phone", "exclamation_ct", "caps_ratio",
] + CAT_COLS

# ── 3. Train/Test Split ───────────────────────────────────────────────────────

X_text = df["text_all"]
X_tab  = df[TABULAR_FEATURES]
y      = df["fraudulent"]

# Stratified split preserves ~4.8% fraud rate in both sets
X_text_tr, X_text_te, X_tab_tr, X_tab_te, y_tr, y_te = train_test_split(
    X_text, X_tab, y, test_size=0.2, random_state=42, stratify=y
)

print(f"Train: {len(y_tr):,} | Test: {len(y_te):,}")
print(f"Train fraud rate: {y_tr.mean():.1%} | Test: {y_te.mean():.1%}")

scale_pos = (y_tr == 0).sum() / (y_tr == 1).sum()
print(f"Class imbalance ratio: {scale_pos:.1f}:1")

# ── 4. Model 1 — Logistic Regression (TF-IDF text only) ─────────────────────

print("\n── Model 1: Logistic Regression (TF-IDF) ──")
lr_pipe = Pipeline([
    ("tfidf", TfidfVectorizer(max_features=15000, ngram_range=(1, 2),
                               sublinear_tf=True, min_df=2)),
    ("clf",   LogisticRegression(class_weight="balanced", max_iter=1000,
                                  C=1.0, random_state=42)),
])
lr_pipe.fit(X_text_tr, y_tr)
y_prob_lr = lr_pipe.predict_proba(X_text_te)[:, 1]
y_pred_lr = (y_prob_lr >= 0.5).astype(int)

print(classification_report(y_te, y_pred_lr, target_names=["real", "fake"]))
print(f"ROC-AUC:  {roc_auc_score(y_te, y_prob_lr):.4f}")
print(f"PR-AUC:   {average_precision_score(y_te, y_prob_lr):.4f}")

# ── 5. Model 2 — LightGBM (tabular features only) ───────────────────────────

print("\n── Model 2: LightGBM (tabular features) ──")
lgb_model = lgb.LGBMClassifier(
    n_estimators=500,
    learning_rate=0.05,
    num_leaves=31,
    scale_pos_weight=scale_pos,
    random_state=42,
    verbose=-1,
)
lgb_model.fit(X_tab_tr, y_tr)
y_prob_lgb = lgb_model.predict_proba(X_tab_te)[:, 1]
y_pred_lgb = (y_prob_lgb >= 0.5).astype(int)

print(classification_report(y_te, y_pred_lgb, target_names=["real", "fake"]))
print(f"ROC-AUC:  {roc_auc_score(y_te, y_prob_lgb):.4f}")
print(f"PR-AUC:   {average_precision_score(y_te, y_prob_lgb):.4f}")

# ── 6. Model 3 — LightGBM (TF-IDF + tabular, combined) ───────────────────────

print("\n── Model 3: LightGBM (TF-IDF SVD + tabular, combined) ──")
from sklearn.decomposition import TruncatedSVD
from scipy.sparse import hstack, csr_matrix

tfidf = TfidfVectorizer(max_features=20000, ngram_range=(1, 2),
                         sublinear_tf=True, min_df=2)
X_tfidf_tr = tfidf.fit_transform(X_text_tr)
X_tfidf_te = tfidf.transform(X_text_te)

# Reduce TF-IDF to 100 LSA dims
svd = TruncatedSVD(n_components=100, random_state=42)
X_lsa_tr = svd.fit_transform(X_tfidf_tr)
X_lsa_te = svd.transform(X_tfidf_te)

X_combined_tr = np.hstack([X_lsa_tr, X_tab_tr.values])
X_combined_te = np.hstack([X_lsa_te, X_tab_te.values])

lgb_combined = lgb.LGBMClassifier(
    n_estimators=500,
    learning_rate=0.05,
    num_leaves=63,
    scale_pos_weight=scale_pos,
    random_state=42,
    verbose=-1,
)
lgb_combined.fit(X_combined_tr, y_tr)
y_prob_comb = lgb_combined.predict_proba(X_combined_te)[:, 1]
y_pred_comb = (y_prob_comb >= 0.5).astype(int)

print(classification_report(y_te, y_pred_comb, target_names=["real", "fake"]))
print(f"ROC-AUC:  {roc_auc_score(y_te, y_prob_comb):.4f}")
print(f"PR-AUC:   {average_precision_score(y_te, y_prob_comb):.4f}")

# ── 7. Summary table ─────────────────────────────────────────────────────────

from sklearn.metrics import f1_score, precision_score, recall_score

results = []
for name, y_pred, y_prob in [
    ("LR (TF-IDF)",          y_pred_lr,   y_prob_lr),
    ("LightGBM (tabular)",   y_pred_lgb,  y_prob_lgb),
    ("LightGBM (TF-IDF+tab)",y_pred_comb, y_prob_comb),
]:
    results.append({
        "Model":     name,
        "Precision": precision_score(y_te, y_pred),
        "Recall":    recall_score(y_te, y_pred),
        "F1":        f1_score(y_te, y_pred),
        "ROC-AUC":   roc_auc_score(y_te, y_prob),
        "PR-AUC":    average_precision_score(y_te, y_prob),
    })

results_df = pd.DataFrame(results).set_index("Model")
print("\n── Summary ──")
print(results_df.round(4).to_string())

# ── 8. Charts ────────────────────────────────────────────────────────────────

fig, axes = plt.subplots(1, 3, figsize=(16, 5))
fig.suptitle("Fake Job Posting Detection — Model Comparison", fontsize=13, fontweight="bold")

# 8a. PR curves
ax = axes[0]
for name, y_prob in [
    ("LR (TF-IDF)",           y_prob_lr),
    ("LightGBM (tabular)",    y_prob_lgb),
    ("LightGBM (TF-IDF+tab)", y_prob_comb),
]:
    prec, rec, _ = precision_recall_curve(y_te, y_prob)
    ap = average_precision_score(y_te, y_prob)
    ax.plot(rec, prec, label=f"{name} (AP={ap:.3f})")
ax.set_xlabel("Recall"); ax.set_ylabel("Precision")
ax.set_title("Precision-Recall Curves")
ax.legend(fontsize=8)

# 8b. ROC-AUC bar chart
ax = axes[1]
models = results_df.index.tolist()
roc_vals = results_df["ROC-AUC"].values
bars = ax.bar(range(len(models)), roc_vals, color=["#4C72B0", "#DD8452", "#55A868"])
ax.set_xticks(range(len(models)))
ax.set_xticklabels([m.replace(" ", "\n") for m in models], fontsize=8)
ax.set_ylim(0.85, 1.0)
ax.set_title("ROC-AUC by Model")
for bar, val in zip(bars, roc_vals):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.001,
            f"{val:.4f}", ha="center", va="bottom", fontsize=9)

# 8c. Feature importance (LightGBM combined)
ax = axes[2]
feature_names = [f"LSA_{i}" for i in range(100)] + TABULAR_FEATURES
feat_imp = pd.Series(lgb_combined.feature_importances_, index=feature_names)
top15 = feat_imp.nlargest(15)
top15_tab = top15[top15.index.isin(TABULAR_FEATURES)]  # show only tabular for readability
# show top 15 overall
colors = ["#DD8452" if i in TABULAR_FEATURES else "#4C72B0" for i in top15.index]
top15.plot(kind="barh", ax=ax, color=colors)
ax.set_title("Top 15 Features (Combined Model)\norange=tabular, blue=LSA")
ax.set_xlabel("Importance")
ax.invert_yaxis()

plt.tight_layout()
plt.savefig(f"{sys_path}/outputs/fake_job_model_comparison.png", bbox_inches="tight")
print(f"\nChart saved → outputs/fake_job_model_comparison.png")

# 8d. Confusion matrix for best model
fig2, axes2 = plt.subplots(1, 3, figsize=(13, 4))
fig2.suptitle("Confusion Matrices (test set)", fontsize=12, fontweight="bold")
for ax, name, y_pred in zip(
    axes2,
    ["LR (TF-IDF)", "LightGBM (tabular)", "LightGBM (TF-IDF+tab)"],
    [y_pred_lr, y_pred_lgb, y_pred_comb],
):
    cm = confusion_matrix(y_te, y_pred)
    im = ax.imshow(cm, cmap="Blues")
    ax.set_xticks([0, 1]); ax.set_yticks([0, 1])
    ax.set_xticklabels(["Pred Real", "Pred Fake"])
    ax.set_yticklabels(["Actual Real", "Actual Fake"])
    for i in range(2):
        for j in range(2):
            ax.text(j, i, str(cm[i, j]), ha="center", va="center",
                    color="white" if cm[i, j] > cm.max()/2 else "black", fontsize=12)
    ax.set_title(name, fontsize=9)

plt.tight_layout()
plt.savefig(f"{sys_path}/outputs/fake_job_confusion_matrices.png", bbox_inches="tight")
print(f"Chart saved → outputs/fake_job_confusion_matrices.png")

print("\nDone.")
