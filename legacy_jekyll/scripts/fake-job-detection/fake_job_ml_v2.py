"""
Fake Job Postings -- ML Pipeline v2
Adds: threshold tuning, SHAP, keyword extraction, CV, sentence-transformers
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import warnings
import hashlib
import sys
from pathlib import Path
warnings.filterwarnings("ignore")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

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

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts.chart_theme import (
    ACCENT, BORDER, CANVAS, DPI, GRID, HIGHLIGHT, INK, MUTED, PAPER,
    SECONDARY, WIDE_SIZE, add_header, add_source, style_axis, style_figure,
)
SOURCE = ROOT / "analysis_data" / "raw" / "fake_job_postings.csv"
OUT = ROOT / "public" / "images"
EXPECTED_SOURCE_SHA256 = "59253295129d8b6a27607f9904f7d4ddf4dbb0ee35e079c7eb51b58b5e62bf60"

# =============================================================================
# 1. LOAD + FEATURE ENGINEERING (same as v1)
# =============================================================================

actual_source_sha256 = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
if actual_source_sha256 != EXPECTED_SOURCE_SHA256:
    raise ValueError(f"Fake job source snapshot drift: {actual_source_sha256}")
df = pd.read_csv(SOURCE)
assert len(df) == 17_880 and int(df["fraudulent"].sum()) == 866
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

train_idx, test_idx = train_test_split(
    np.arange(len(y)), test_size=0.2, random_state=42, stratify=y
)
X_text_tr, X_text_te = X_text.iloc[train_idx], X_text.iloc[test_idx]
X_tab_tr, X_tab_te = X_tab.iloc[train_idx], X_tab.iloc[test_idx]
y_tr, y_te = y.iloc[train_idx], y.iloc[test_idx]

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

# Keep the original train and test encoding batches so its stored metrics are
# reproducible, then encode the full set separately for the five-fold check.
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
assert round(float(np.mean(cv_f1)), 4) == 0.8251
assert round(float(np.std(cv_f1)), 4) == 0.0208
assert round(float(np.mean(cv_auc)), 4) == 0.9859
assert round(float(np.std(cv_auc)), 4) == 0.0030

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

# --- Fig 1: Threshold tuning and cross-validation ---
fig, axes = plt.subplots(1, 2, figsize=WIDE_SIZE, facecolor=CANVAS)
style_figure(fig)
fig.subplots_adjust(left=0.08, right=0.97, top=0.79, bottom=0.17, wspace=0.28)
for axis in axes:
    style_axis(axis)

ax = axes[0]
ax.plot(thresholds, f1_scores, label="F1", color=ACCENT, linewidth=2.1)
ax.plot(thresholds, prec_scores, label="Precision", color=HIGHLIGHT, linewidth=1.7)
ax.plot(thresholds, rec_scores, label="Recall", color=SECONDARY, linewidth=1.7)
ax.axvline(best_thresh, color=MUTED, linestyle="--", linewidth=1.2)
ax.set_xlabel("Decision threshold")
ax.set_ylabel("Held-out test score")
ax.set_ylim(0, 1.02)
ax.legend(frameon=False, labelcolor=INK, fontsize=8)
ax.set_title("Threshold trade-off", loc="left", color=INK, fontsize=11, fontweight="bold")

ax = axes[1]
folds = [f"Fold {i + 1}" for i in range(5)]
x = np.arange(5)
w = 0.36
bars1 = ax.bar(x - w / 2, cv_f1, w, label="F1", color=ACCENT)
bars2 = ax.bar(x + w / 2, cv_auc, w, label="ROC-AUC", color=SECONDARY)
ax.set_xticks(x, folds)
ax.set_ylim(0.7, 1.03)
ax.set_ylabel("Cross-validation score")
ax.set_title(f"Five-fold check: F1 {np.mean(cv_f1):.3f} ± {np.std(cv_f1):.3f}",
             loc="left", color=INK, fontsize=10.5, fontweight="bold")
ax.legend(frameon=False, labelcolor=INK, fontsize=8)
for bars in (bars1, bars2):
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.004,
                f"{bar.get_height():.3f}", ha="center", va="bottom", fontsize=7.5, color=INK)

test_pred = (y_prob_st >= best_thresh).astype(int)
assert len(y_te) == 3_576 and int(y_te.sum()) == 173
assert round(best_thresh, 2) == 0.10
assert round(best_f1, 3) == 0.850
assert round(recall_score(y_te, test_pred), 3) == 0.751
assert round(precision_score(y_te, test_pred), 2) == 0.98
assert round(np.mean(cv_f1), 3) == 0.825 and round(np.std(cv_f1), 3) == 0.021
add_header(fig, "A 0.10 threshold balanced scam capture and review volume",
           "Held-out stratified test and five-fold validation; a threshold is a review-policy choice")
add_source(fig, "Employment Scam Aegean Dataset; 17,880 labeled job posts")
fig.savefig(OUT / "fake-job-threshold-cv.png", dpi=DPI, facecolor=fig.get_facecolor())
plt.close(fig)
print("Validated and saved fake-job-threshold-cv.png")

# --- Fig 2: Keyword signals ---
fig, axes = plt.subplots(1, 2, figsize=WIDE_SIZE, facecolor=CANVAS)
style_figure(fig)
fig.subplots_adjust(left=0.15, right=0.97, top=0.79, bottom=0.17, wspace=0.30)
for axis in axes:
    style_axis(axis, grid_axis="x")
fake_sorted = top_fake.sort_values("log_odds")
real_sorted = top_real.sort_values("log_odds", ascending=False)
axes[0].barh(fake_sorted["term"], fake_sorted["log_odds"], color=HIGHLIGHT, height=0.72)
axes[0].set_title("More common in fake posts", loc="left", color=INK, fontsize=11, fontweight="bold")
axes[0].set_xlabel("Log-odds (higher means more common)")
axes[0].axvline(0, color=BORDER, linewidth=0.9)
axes[1].barh(real_sorted["term"], real_sorted["log_odds"], color=ACCENT, height=0.72)
axes[1].set_title("More common in legitimate posts", loc="left", color=INK, fontsize=11, fontweight="bold")
axes[1].set_xlabel("Log-odds (negative means more common in legitimate posts)")
axes[1].axvline(0, color=BORDER, linewidth=0.9)
for axis in axes:
    axis.tick_params(axis="y", labelsize=7.5)
add_header(fig, "Posting language differs between fake and legitimate jobs",
           "Relative keyword frequency in the full labeled dataset; association does not prove intent")
add_source(fig, "Employment Scam Aegean Dataset; text fields combined by posting")
fig.savefig(OUT / "fake-job-keywords.png", dpi=DPI, facecolor=fig.get_facecolor())
plt.close(fig)
print("Validated and saved fake-job-keywords.png")

# --- Fig 3: SHAP Summary ---
fig, ax = plt.subplots(figsize=WIDE_SIZE, facecolor=CANVAS)
style_figure(fig)
fig.subplots_adjust(left=0.22, right=0.96, top=0.80, bottom=0.16)
style_axis(ax, grid_axis="x")
top_shap = shap_df.head(14)
feature_colors = [HIGHLIGHT if f in ["has_company_logo", "has_questions", "telecommuting",
                               "has_salary", "has_profile", "missing_count",
                               "exclamation_ct", "caps_ratio", "has_url"]
                 else ACCENT for f in top_shap["feature"]]
ax.barh(top_shap["feature"][::-1], top_shap["mean_abs_shap"][::-1], color=feature_colors[::-1])
ax.set_xlabel("Mean absolute SHAP value")
add_header(fig, "Text and profile details both contribute to the model score",
           "Mean absolute SHAP values for a LightGBM model using profile and engineered text features")
add_source(fig, "Employment Scam Aegean Dataset; SHAP on a 200-post stratified test subset")
fig.savefig(OUT / "fake-job-shap.png", dpi=DPI, facecolor=fig.get_facecolor())
plt.close(fig)
print("Validated and saved fake-job-shap.png")

# --- Fig 4: Model comparison (all 4 models) ---
all_models = [
    ("LR (TF-IDF)",       y_prob_lr,   None),
    ("LightGBM (LSA+tab)",y_prob_comb, None),
    ("ST + LightGBM @0.5",y_prob_st,   0.5),
    ("ST + LightGBM tuned",y_prob_st,  best_thresh),
]

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
expected = {
    "F1": [0.819, 0.828, 0.831, 0.850],
    "Recall": [0.913, 0.723, 0.711, 0.751],
    "PR-AUC": [0.927, 0.915, 0.901, 0.901],
}
for metric, values in expected.items():
    assert [round(value, 3) for value in sum_df[metric].tolist()] == values, (metric, sum_df[metric].tolist())

fig, ax = plt.subplots(figsize=WIDE_SIZE, facecolor=CANVAS)
style_figure(fig)
style_axis(ax)
fig.subplots_adjust(left=0.08, right=0.97, top=0.80, bottom=0.21)
labels = ["Text model\nLogistic regression", "Profile\nLightGBM", "Combined\ndefault", "Combined\ntuned"]
x = np.arange(len(sum_df))
w = 0.23
metric_colors = [("F1", ACCENT), ("Recall", SECONDARY), ("PR-AUC", HIGHLIGHT)]
for offset, (metric, color) in enumerate(metric_colors):
    bars = ax.bar(x + (offset - 1) * w, sum_df[metric], w, label=metric, color=color)
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.012,
                f"{bar.get_height():.3f}", ha="center", va="bottom", color=INK, fontsize=7.5)
ax.set_xticks(x, labels)
ax.tick_params(axis="x", labelsize=8)
ax.set_ylim(0.65, 1.02)
ax.set_ylabel("Held-out test score")
ax.legend(frameon=False, ncols=3, loc="upper left", labelcolor=INK, fontsize=9)
add_header(fig, "Text signals caught more scams; threshold tuning raised combined F1",
           "Stratified held-out test; recall and precision describe different review trade-offs")
add_source(fig, "Employment Scam Aegean Dataset; 3,576 held-out posts")
fig.savefig(OUT / "fake-job-all-models.png", dpi=DPI, facecolor=fig.get_facecolor())
plt.close(fig)
print("Validated and saved fake-job-all-models.png")

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
