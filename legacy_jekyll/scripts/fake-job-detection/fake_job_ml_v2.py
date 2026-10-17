"""
Fake Job Postings -- ML Pipeline v2
Adds: validation threshold selection, feature importance, and keyword analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
import hashlib
import sys
from pathlib import Path
warnings.filterwarnings("ignore")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics import (
    classification_report, confusion_matrix,
    average_precision_score, f1_score,
    precision_score, recall_score,
)
import lightgbm as lgb

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
    df[col] = df[col].fillna("missing").astype(str)

TABULAR_FEATURES = [
    "telecommuting", "has_company_logo", "has_questions",
    "text_len", "word_count", "has_salary", "has_dept",
    "has_profile", "has_requirements", "missing_count",
    "has_url", "has_phone", "exclamation_ct", "caps_ratio",
] + CAT_COLS

X_text = df["text_all"]
X_tab  = df[TABULAR_FEATURES]
y      = df["fraudulent"]

development_idx, test_idx = train_test_split(
    np.arange(len(y)), test_size=0.2, random_state=42, stratify=y
)
train_idx, validation_idx = train_test_split(
    development_idx, test_size=0.25, random_state=43, stratify=y.iloc[development_idx]
)
X_text_tr = X_text.iloc[train_idx]
X_text_val = X_text.iloc[validation_idx]
X_text_te = X_text.iloc[test_idx]
X_tab_tr = X_tab.iloc[train_idx].copy()
X_tab_val = X_tab.iloc[validation_idx].copy()
X_tab_te = X_tab.iloc[test_idx].copy()
y_tr = y.iloc[train_idx]
y_val = y.iloc[validation_idx]
y_te = y.iloc[test_idx]

category_encoder = OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1)
X_tab_tr[CAT_COLS] = category_encoder.fit_transform(X_tab_tr[CAT_COLS]).astype(float)
X_tab_val[CAT_COLS] = category_encoder.transform(X_tab_val[CAT_COLS]).astype(float)
X_tab_te[CAT_COLS] = category_encoder.transform(X_tab_te[CAT_COLS]).astype(float)

scale_pos = (y_tr == 0).sum() / (y_tr == 1).sum()
print(f"Train: {len(y_tr):,} | Validation: {len(y_val):,} | Test: {len(y_te):,} | imbalance: {scale_pos:.1f}:1")

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
X_tfidf_val = tfidf.transform(X_text_val)
X_tfidf_te = tfidf.transform(X_text_te)
svd = TruncatedSVD(n_components=100, random_state=42)
X_lsa_tr = svd.fit_transform(X_tfidf_tr)
X_lsa_val = svd.transform(X_tfidf_val)
X_lsa_te = svd.transform(X_tfidf_te)

X_comb_tr = np.hstack([X_lsa_tr, X_tab_tr.values])
X_comb_val = np.hstack([X_lsa_val, X_tab_val.values])
X_comb_te = np.hstack([X_lsa_te, X_tab_te.values])

lgb_comb = lgb.LGBMClassifier(n_estimators=500, learning_rate=0.05, num_leaves=63,
                                scale_pos_weight=scale_pos, random_state=42, verbose=-1)
lgb_comb.fit(X_comb_tr, y_tr)
y_prob_comb_val = lgb_comb.predict_proba(X_comb_val)[:, 1]
y_prob_comb = lgb_comb.predict_proba(X_comb_te)[:, 1]

print("Baseline models trained.")

# =============================================================================
# 4. THRESHOLD SELECTION (validation set only)
# =============================================================================

print("\n-- Threshold Selection (combined LightGBM model) --")
thresholds = np.arange(0.1, 0.9, 0.01)
f1_scores = [f1_score(y_val, (y_prob_comb_val >= t).astype(int)) for t in thresholds]
prec_scores = [precision_score(y_val, (y_prob_comb_val >= t).astype(int), zero_division=0) for t in thresholds]
rec_scores = [recall_score(y_val, (y_prob_comb_val >= t).astype(int)) for t in thresholds]

best_thresh = thresholds[np.argmax(f1_scores)]
best_val_f1 = max(f1_scores)
test_pred_tuned = (y_prob_comb >= best_thresh).astype(int)

print(f"Validation threshold: {best_thresh:.2f}  -->  validation F1={best_val_f1:.4f}")
print("Untouched test result at the selected threshold:")
print(classification_report(y_te, test_pred_tuned, target_names=["real", "fake"]))
print(f"Test F1: {f1_score(y_te, test_pred_tuned):.4f}")

# =============================================================================
# 5. SUSPICIOUS KEYWORD EXTRACTION
# =============================================================================

print("\n-- Suspicious Keyword Extraction --")

development_df = df.iloc[development_idx]
fake_text = " ".join(development_df.loc[development_df.fraudulent == 1, "text_all"].tolist())
real_text = " ".join(development_df.loc[development_df.fraudulent == 0, "text_all"].tolist())

cv_kw = CountVectorizer(max_features=5000, ngram_range=(1,2),
                         stop_words="english", min_df=3)
cv_kw.fit(development_df["text_all"])
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
# 7. TABULAR FEATURE IMPORTANCE (LightGBM model)
# =============================================================================

print("\n-- Tabular Feature Importance (LightGBM) --")

lgb_tab = lgb.LGBMClassifier(n_estimators=300, learning_rate=0.05, num_leaves=31,
                               scale_pos_weight=scale_pos, random_state=42, verbose=-1)
lgb_tab.fit(X_tab_tr, y_tr)

importance_df = pd.DataFrame({"feature": TABULAR_FEATURES, "split_count": lgb_tab.feature_importances_})
importance_df = importance_df.sort_values("split_count", ascending=False)
print(importance_df.to_string(index=False))

# =============================================================================
# 8. CHARTS
# =============================================================================

# --- Fig 1: Validation threshold and untouched test results ---
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
ax.set_ylabel("Validation score")
ax.set_ylim(0, 1.02)
ax.legend(frameon=False, labelcolor=INK, fontsize=8)
ax.set_title("Select threshold on validation data", loc="left", color=INK, fontsize=11, fontweight="bold")

ax = axes[1]
test_cm = confusion_matrix(y_te, test_pred_tuned, labels=[0, 1])
ax.imshow(test_cm, cmap="Blues")
ax.set_xticks([0, 1], ["Predicted real", "Predicted fake"])
ax.set_yticks([0, 1], ["Actual real", "Actual fake"])
ax.set_title(f"Untouched test set (n={len(y_te):,})", loc="left", color=INK, fontsize=10.5, fontweight="bold")
for row in range(2):
    for column in range(2):
        color = "white" if row == 0 and column == 0 else INK
        ax.text(column, row, f"{test_cm[row, column]:,}", ha="center", va="center", color=color, fontsize=12, fontweight="bold")

assert len(y_te) == 3_576 and int(y_te.sum()) == 173
assert len(y_val) == 3_576 and int(y_val.sum()) == 173
assert 0.1 <= best_thresh <= 0.89
add_header(fig, f"A {best_thresh:.2f} threshold was selected on validation data",
           "The untouched test set estimates performance at this review-policy threshold")
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
add_header(fig, "Posting language differs in the development sample",
           "Relative keyword frequency; association does not prove intent or predict future scams")
add_source(fig, "Employment Scam Aegean Dataset; train and validation posts only")
fig.savefig(OUT / "fake-job-keywords.png", dpi=DPI, facecolor=fig.get_facecolor())
plt.close(fig)
print("Validated and saved fake-job-keywords.png")

# --- Fig 3: Tabular feature importance ---
fig, ax = plt.subplots(figsize=WIDE_SIZE, facecolor=CANVAS)
style_figure(fig)
fig.subplots_adjust(left=0.22, right=0.96, top=0.80, bottom=0.16)
style_axis(ax, grid_axis="x")
top_importance = importance_df.head(14)
feature_colors = [HIGHLIGHT if f in ["has_company_logo", "has_questions", "telecommuting",
                               "has_salary", "has_profile", "missing_count",
                               "exclamation_ct", "caps_ratio", "has_url"]
                 else ACCENT for f in top_importance["feature"]]
ax.barh(top_importance["feature"][::-1], top_importance["split_count"][::-1], color=feature_colors[::-1])
ax.set_xlabel("LightGBM split count")
add_header(fig, "Text length, capitalization, and industry dominate split counts",
           "Split-count importance shows model structure, not causal influence")
add_source(fig, "Employment Scam Aegean Dataset; profile-feature LightGBM, fit on training data")
fig.savefig(OUT / "fake-job-feature-importance.png", dpi=DPI, facecolor=fig.get_facecolor())
plt.close(fig)
print("Saved fake-job-feature-importance.png")

# --- Fig 4: Model comparison (all 4 models) ---
all_models = [
    ("Text LR (TF-IDF)", y_prob_lr, 0.5),
    ("Combined default", y_prob_comb, 0.5),
    ("Combined tuned", y_prob_comb, best_thresh),
]

summary_rows = []
for name, prob, thresh in all_models:
    t = thresh
    pred = (prob >= t).astype(int)
    summary_rows.append({
        "Model": name,
        "F1":      f1_score(y_te, pred),
        "Recall":  recall_score(y_te, pred),
        "PR-AUC":  average_precision_score(y_te, prob),
    })
sum_df = pd.DataFrame(summary_rows)
assert len(sum_df) == 3 and np.isfinite(sum_df[["F1", "Recall", "PR-AUC"]].to_numpy()).all()

fig, ax = plt.subplots(figsize=WIDE_SIZE, facecolor=CANVAS)
style_figure(fig)
style_axis(ax)
fig.subplots_adjust(left=0.08, right=0.97, top=0.80, bottom=0.21)
labels = ["Text model\nLogistic regression", "Combined\ndefault", "Combined\nvalidation tuned"]
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
add_header(fig, "Text-only and combined models show different test trade-offs",
           f"Combined threshold {best_thresh:.2f} selected on validation data; all bars use the untouched test set")
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

print(f"\nValidation-selected threshold (F1-optimized): {best_thresh:.2f}")
print("\nDone. Fake Job charts saved to public/images/")
