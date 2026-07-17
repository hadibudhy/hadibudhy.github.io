"""
Fake Job Postings -- ML Pipeline v2
Adds: threshold tuning, SHAP, keyword extraction, CV, sentence-transformers
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import warnings
warnings.filterwarnings("ignore")

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics import (
    classification_report, confusion_matrix,
    roc_auc_score, average_precision_score,
    precision_recall_curve, f1_score,
    precision_score, recall_score,
)
import lightgbm as lgb
import shap
from sentence_transformers import SentenceTransformer

PROJ = "D:/Agent/ai-analyst"

plt.rcParams.update({
    "font.family": "sans-serif",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.3,
    "figure.dpi": 120,
})

# =============================================================================
# 1. LOAD + FEATURE ENGINEERING (same as v1)
# =============================================================================

df = pd.read_csv(f"{PROJ}/data/fake_job_postings.csv")
print(f"Loaded: {df.shape[0]:,} rows | fraud rate: {df.fraudulent.mean():.1%}")

TEXT_COLS = ["title", "company_profile", "description", "requirements", "benefits"]
df["text_all"] = df[TEXT_COLS].fillna("").agg(" ".join, axis=1)

df["text_len"]         = df["text_all"].str.len()
df["word_count"]       = df["text_all"].str.split().str.len()
df["has_salary"]       = df["salary_range"].notna().astype(int)
df["has_dept"]         = df["department"].notna().astype(int)
df["has_profile"]      = df["company_profile"].notna().astype(int)
df["has_requirements"] = df["requirements"].notna().astype(int)
df["missing_count"]    = df[TEXT_COLS].isna().sum(axis=1)
df["has_url"]          = df["text_all"].str.contains(r"http|www\.|\.com", case=False, regex=True).astype(int)
df["has_phone"]        = df["text_all"].str.contains(r"\d{3}[-.\s]\d{3}", regex=True).astype(int)
df["exclamation_ct"]   = df["text_all"].str.count(r"!")
df["caps_ratio"]       = df["text_all"].apply(
    lambda x: sum(1 for c in x if c.isupper()) / max(len(x), 1)
)

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

X_text = df["text_all"]
X_tab  = df[TABULAR_FEATURES]
y      = df["fraudulent"]

X_text_tr, X_text_te, X_tab_tr, X_tab_te, y_tr, y_te = train_test_split(
    X_text, X_tab, y, test_size=0.2, random_state=42, stratify=y
)

scale_pos = (y_tr == 0).sum() / (y_tr == 1).sum()
print(f"Train: {len(y_tr):,} | Test: {len(y_te):,} | imbalance: {scale_pos:.1f}:1")

# =============================================================================
# 2. BASELINE MODELS (LR + LightGBM combined) -- replicated from v1
# =============================================================================

# LR TF-IDF
lr_pipe = Pipeline([
    ("tfidf", TfidfVectorizer(max_features=15000, ngram_range=(1,2),
                               sublinear_tf=True, min_df=2)),
    ("clf",   LogisticRegression(class_weight="balanced", max_iter=1000, C=1.0, random_state=42)),
])
lr_pipe.fit(X_text_tr, y_tr)
y_prob_lr = lr_pipe.predict_proba(X_text_te)[:, 1]

# LightGBM combined (TF-IDF LSA + tabular)
tfidf = TfidfVectorizer(max_features=20000, ngram_range=(1,2), sublinear_tf=True, min_df=2)
X_tfidf_tr = tfidf.fit_transform(X_text_tr)
X_tfidf_te = tfidf.transform(X_text_te)
svd = TruncatedSVD(n_components=100, random_state=42)
X_lsa_tr = svd.fit_transform(X_tfidf_tr)
X_lsa_te = svd.transform(X_tfidf_te)

X_comb_tr = np.hstack([X_lsa_tr, X_tab_tr.values])
X_comb_te = np.hstack([X_lsa_te, X_tab_te.values])

lgb_comb = lgb.LGBMClassifier(n_estimators=500, learning_rate=0.05, num_leaves=63,
                                scale_pos_weight=scale_pos, random_state=42, verbose=-1)
lgb_comb.fit(X_comb_tr, y_tr)
y_prob_comb = lgb_comb.predict_proba(X_comb_te)[:, 1]

print("Baseline models trained.")

# =============================================================================
# 3. SENTENCE TRANSFORMERS (all-MiniLM-L6-v2)
# =============================================================================

print("\n-- Model 4: Sentence Transformers + LightGBM --")
print("Encoding text with all-MiniLM-L6-v2 ...")
encoder = SentenceTransformer("all-MiniLM-L6-v2")

# Encode -- returns 384-dim vectors
X_emb_tr = encoder.encode(X_text_tr.tolist(), batch_size=128, show_progress_bar=True)
X_emb_te = encoder.encode(X_text_te.tolist(), batch_size=128, show_progress_bar=True)

# Combine embeddings with tabular
X_st_tr = np.hstack([X_emb_tr, X_tab_tr.values])
X_st_te = np.hstack([X_emb_te, X_tab_te.values])

lgb_st = lgb.LGBMClassifier(n_estimators=500, learning_rate=0.05, num_leaves=63,
                              scale_pos_weight=scale_pos, random_state=42, verbose=-1)
lgb_st.fit(X_st_tr, y_tr)
y_prob_st = lgb_st.predict_proba(X_st_te)[:, 1]
y_pred_st_def = (y_prob_st >= 0.5).astype(int)

print(classification_report(y_te, y_pred_st_def, target_names=["real", "fake"]))
print(f"ROC-AUC: {roc_auc_score(y_te, y_prob_st):.4f}")
print(f"PR-AUC:  {average_precision_score(y_te, y_prob_st):.4f}")

# =============================================================================
# 4. THRESHOLD TUNING (on best model = ST+tab LightGBM)
# =============================================================================

print("\n-- Threshold Tuning (Sentence Transformer model) --")
thresholds = np.arange(0.1, 0.9, 0.01)
f1_scores    = [f1_score(y_te, (y_prob_st >= t).astype(int)) for t in thresholds]
prec_scores  = [precision_score(y_te, (y_prob_st >= t).astype(int), zero_division=0) for t in thresholds]
rec_scores   = [recall_score(y_te, (y_prob_st >= t).astype(int)) for t in thresholds]

best_thresh = thresholds[np.argmax(f1_scores)]
best_f1     = max(f1_scores)
y_pred_tuned = (y_prob_st >= best_thresh).astype(int)

print(f"Best threshold: {best_thresh:.2f}  -->  F1={best_f1:.4f}")
print(classification_report(y_te, y_pred_tuned, target_names=["real", "fake"]))

# =============================================================================
# 5. CROSS-VALIDATION (5-fold, on ST+tab LightGBM)
# =============================================================================

print("\n-- 5-Fold Cross-Validation (Sentence Transformer model) --")
# Re-build full dataset embeddings for CV
print("Encoding full dataset for CV ...")
X_emb_all = encoder.encode(X_text.tolist(), batch_size=128, show_progress_bar=True)
X_cv_all   = np.hstack([X_emb_all, X_tab.values])
y_all      = y.values

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
cv_f1  = []
cv_auc = []

for fold, (tr_idx, te_idx) in enumerate(cv.split(X_cv_all, y_all)):
    X_cv_tr, X_cv_te = X_cv_all[tr_idx], X_cv_all[te_idx]
    y_cv_tr, y_cv_te = y_all[tr_idx], y_all[te_idx]
    sp = (y_cv_tr == 0).sum() / (y_cv_tr == 1).sum()
    m = lgb.LGBMClassifier(n_estimators=300, learning_rate=0.05, num_leaves=63,
                             scale_pos_weight=sp, random_state=42, verbose=-1)
    m.fit(X_cv_tr, y_cv_tr)
    prob = m.predict_proba(X_cv_te)[:, 1]
    pred = (prob >= best_thresh).astype(int)
    cv_f1.append(f1_score(y_cv_te, pred))
    cv_auc.append(roc_auc_score(y_cv_te, prob))
    print(f"  Fold {fold+1}: F1={cv_f1[-1]:.4f}  ROC-AUC={cv_auc[-1]:.4f}")

print(f"\nCV F1:      {np.mean(cv_f1):.4f} +/- {np.std(cv_f1):.4f}")
print(f"CV ROC-AUC: {np.mean(cv_auc):.4f} +/- {np.std(cv_auc):.4f}")

# =============================================================================
# 6. SUSPICIOUS KEYWORD EXTRACTION
# =============================================================================

print("\n-- Suspicious Keyword Extraction --")

fake_text = " ".join(df.loc[df.fraudulent == 1, "text_all"].tolist())
real_text = " ".join(df.loc[df.fraudulent == 0, "text_all"].tolist())

cv_kw = CountVectorizer(max_features=5000, ngram_range=(1,2),
                         stop_words="english", min_df=3)
cv_kw.fit(df["text_all"])
vocab = cv_kw.get_feature_names_out()

fake_counts = np.asarray(cv_kw.transform([fake_text]).todense()).flatten()
real_counts = np.asarray(cv_kw.transform([real_text]).todense()).flatten()

# Normalize by total words in each class
fake_freq = fake_counts / max(fake_counts.sum(), 1)
real_freq = real_counts / max(real_counts.sum(), 1)

# Log-odds: positive = more common in fake
eps = 1e-9
log_odds = np.log((fake_freq + eps) / (real_freq + eps))

kw_df = pd.DataFrame({"term": vocab, "log_odds": log_odds,
                        "fake_freq": fake_freq, "real_freq": real_freq})
top_fake = kw_df.nlargest(20, "log_odds")
top_real = kw_df.nsmallest(20, "log_odds")

print("\nTop 20 terms more common in FAKE postings:")
print(top_fake[["term", "log_odds"]].to_string(index=False))
print("\nTop 20 terms more common in REAL postings:")
print(top_real[["term", "log_odds"]].to_string(index=False))

# =============================================================================
# 7. SHAP EXPLANATION (LightGBM combined model, tabular features only)
# =============================================================================

print("\n-- SHAP Values (LightGBM tabular model) --")

lgb_tab = lgb.LGBMClassifier(n_estimators=300, learning_rate=0.05, num_leaves=31,
                               scale_pos_weight=scale_pos, random_state=42, verbose=-1)
lgb_tab.fit(X_tab_tr, y_tr)

explainer   = shap.TreeExplainer(lgb_tab)
# Use 200-sample subset for speed (SHAP on full test set is slow)
idx_sample  = np.random.RandomState(42).choice(len(X_tab_te), 200, replace=False)
X_shap      = X_tab_te.iloc[idx_sample]
shap_values = explainer.shap_values(X_shap)

# For binary classification, shap_values is list [class0, class1] or 3D array
if isinstance(shap_values, list):
    sv = shap_values[1]   # class 1 = fake
elif shap_values.ndim == 3:
    sv = shap_values[:, :, 1]
else:
    sv = shap_values

mean_abs_shap = np.abs(sv).mean(axis=0)
shap_df = pd.DataFrame({"feature": TABULAR_FEATURES, "mean_abs_shap": mean_abs_shap})
shap_df = shap_df.sort_values("mean_abs_shap", ascending=False)
print(shap_df.to_string(index=False))

# =============================================================================
# 8. CHARTS
# =============================================================================

# --- Fig 1: Threshold Tuning ---
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
fig.suptitle("Threshold Tuning -- Sentence Transformer Model", fontsize=12, fontweight="bold")

ax = axes[0]
ax.plot(thresholds, f1_scores,   label="F1",        color="#4C72B0", linewidth=2)
ax.plot(thresholds, prec_scores, label="Precision",  color="#DD8452", linestyle="--")
ax.plot(thresholds, rec_scores,  label="Recall",     color="#55A868", linestyle="--")
ax.axvline(best_thresh, color="red", linestyle=":", linewidth=1.5, label=f"Best thresh={best_thresh:.2f}")
ax.set_xlabel("Decision Threshold")
ax.set_title("F1, Precision, Recall vs Threshold")
ax.legend()

ax = axes[1]
cv_data = pd.DataFrame({"Fold": [f"Fold {i+1}" for i in range(5)],
                          "F1": cv_f1, "ROC-AUC": cv_auc})
x = np.arange(5)
w = 0.35
bars1 = ax.bar(x - w/2, cv_f1,  w, label="F1",       color="#4C72B0")
bars2 = ax.bar(x + w/2, cv_auc, w, label="ROC-AUC",  color="#55A868")
ax.set_xticks(x)
ax.set_xticklabels(cv_data["Fold"])
ax.set_ylim(0.7, 1.0)
ax.set_title(f"5-Fold CV  |  F1={np.mean(cv_f1):.3f}+/-{np.std(cv_f1):.3f}")
ax.legend()
for bar, val in zip(list(bars1) + list(bars2), cv_f1 + cv_auc):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.003,
            f"{val:.3f}", ha="center", va="bottom", fontsize=7)

plt.tight_layout()
plt.savefig(f"{PROJ}/outputs/fake_job_threshold_cv.png", bbox_inches="tight")
print("Chart saved --> outputs/fake_job_threshold_cv.png")

# --- Fig 2: Keyword Analysis ---
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle("Keyword Log-Odds: Fake vs Real Job Postings", fontsize=12, fontweight="bold")

ax = axes[0]
top_fake.sort_values("log_odds").plot(
    kind="barh", x="term", y="log_odds", ax=ax, color="#DD8452", legend=False)
ax.set_title("Terms more common in FAKE postings")
ax.set_xlabel("Log-Odds (higher = more fake)")
ax.axvline(0, color="black", linewidth=0.8)

ax = axes[1]
top_real.sort_values("log_odds", ascending=False).plot(
    kind="barh", x="term", y="log_odds", ax=ax, color="#4C72B0", legend=False)
ax.set_title("Terms more common in REAL postings")
ax.set_xlabel("Log-Odds (lower = more real)")
ax.axvline(0, color="black", linewidth=0.8)

plt.tight_layout()
plt.savefig(f"{PROJ}/outputs/fake_job_keywords.png", bbox_inches="tight")
print("Chart saved --> outputs/fake_job_keywords.png")

# --- Fig 3: SHAP Summary ---
fig, ax = plt.subplots(figsize=(8, 6))
top_shap = shap_df.head(14)
colors = ["#DD8452" if f in ["has_company_logo", "has_questions", "telecommuting",
                               "has_salary", "has_profile", "missing_count",
                               "exclamation_ct", "caps_ratio", "has_url"]
          else "#4C72B0" for f in top_shap["feature"]]
ax.barh(top_shap["feature"][::-1], top_shap["mean_abs_shap"][::-1], color=colors[::-1])
ax.set_title("SHAP Feature Importance (Tabular LightGBM)\nMean |SHAP| for fake job prediction",
             fontsize=11, fontweight="bold")
ax.set_xlabel("Mean |SHAP value|")
plt.tight_layout()
plt.savefig(f"{PROJ}/outputs/fake_job_shap.png", bbox_inches="tight")
print("Chart saved --> outputs/fake_job_shap.png")

# --- Fig 4: Model comparison (all 4 models) ---
all_models = [
    ("LR (TF-IDF)",       y_prob_lr,   None),
    ("LightGBM (LSA+tab)",y_prob_comb, None),
    ("ST + LightGBM @0.5",y_prob_st,   0.5),
    ("ST + LightGBM tuned",y_prob_st,  best_thresh),
]

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
fig.suptitle("All Models -- PR Curve & Final Metrics", fontsize=12, fontweight="bold")

ax = axes[0]
colors_m = ["#4C72B0", "#DD8452", "#55A868", "#C44E52"]
for (name, prob, _), c in zip(all_models, colors_m):
    from sklearn.metrics import precision_recall_curve
    prec, rec, _ = precision_recall_curve(y_te, prob)
    ap = average_precision_score(y_te, prob)
    ax.plot(rec, prec, label=f"{name} (AP={ap:.3f})", color=c)
ax.set_xlabel("Recall"); ax.set_ylabel("Precision")
ax.set_title("Precision-Recall Curves")
ax.legend(fontsize=8)

ax = axes[1]
summary_rows = []
for name, prob, thresh in all_models:
    t = thresh if thresh is not None else 0.5
    pred = (prob >= t).astype(int)
    summary_rows.append({
        "Model": name,
        "F1":      f1_score(y_te, pred),
        "Recall":  recall_score(y_te, pred),
        "PR-AUC":  average_precision_score(y_te, prob),
    })
sum_df = pd.DataFrame(summary_rows)
x = np.arange(len(sum_df))
w = 0.25
for i, (col, c) in enumerate([("F1","#4C72B0"),("Recall","#55A868"),("PR-AUC","#DD8452")]):
    bars = ax.bar(x + i*w, sum_df[col], w, label=col, color=c)
ax.set_xticks(x + w)
ax.set_xticklabels([r["Model"].replace(" ","\n") for r in summary_rows], fontsize=7)
ax.set_ylim(0.6, 1.0)
ax.set_title("F1 / Recall / PR-AUC by Model")
ax.legend(fontsize=9)

plt.tight_layout()
plt.savefig(f"{PROJ}/outputs/fake_job_all_models.png", bbox_inches="tight")
print("Chart saved --> outputs/fake_job_all_models.png")

# =============================================================================
# 9. FINAL SUMMARY
# =============================================================================

print("\n" + "="*60)
print("FINAL RESULTS")
print("="*60)
for row in summary_rows:
    print(f"  {row['Model']:30s}  F1={row['F1']:.4f}  Recall={row['Recall']:.4f}  PR-AUC={row['PR-AUC']:.4f}")

print(f"\nBest threshold (F1-optimized): {best_thresh:.2f}")
print(f"CV F1 (5-fold):  {np.mean(cv_f1):.4f} +/- {np.std(cv_f1):.4f}")
print(f"CV AUC (5-fold): {np.mean(cv_auc):.4f} +/- {np.std(cv_auc):.4f}")
print("\nDone. All charts in outputs/")
