"""
World Happiness Report 2011-2025 -- Portfolio Analysis
Narrative: 14 years of data, balanced panel, factor decomposition
"""

import sys
sys.path.insert(0, ".")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
from pathlib import Path

from helpers.chart_helpers import swd_style, COLORS

OUTPUT = Path("outputs")
OUTPUT.mkdir(exist_ok=True)

df = pd.read_csv("data/world_happiness_report_2005_2025.csv")

# ── Balanced panel (all 14 years) ─────────────────────────────────────────────
all_years = set(df["year"].unique())
country_years = df.groupby("country")["year"].apply(set)
balanced = country_years[country_years.apply(lambda s: s == all_years)].index
df_bal = df[df["country"].isin(balanced)].copy()

# ── Factor columns ─────────────────────────────────────────────────────────────
FACTOR_COLS = [c for c in df.columns if c.startswith("explained_")]
FACTOR_LABELS = {
    "explained_log_gdp_per_capita": "GDP per capita",
    "explained_social_support": "Social support",
    "explained_healthy_life_expectancy": "Life expectancy",
    "explained_freedom": "Freedom",
    "explained_corruption": "Low corruption",
    "explained_generosity": "Generosity",
}
FACTOR_COLORS = [
    "#2563EB",  # GDP -- blue
    "#16A34A",  # social -- green
    "#DC2626",  # life exp -- red
    "#9333EA",  # freedom -- purple
    "#EA580C",  # corruption -- orange
    "#6B7280",  # generosity -- gray
]

# ════════════════════════════════════════════════════════════════════════════════
# CHART 1 -- Global happiness trend 2011-2025 (balanced panel)
# ════════════════════════════════════════════════════════════════════════════════
colors = swd_style()

fig, ax = plt.subplots(figsize=(10, 5))

yearly = df_bal.groupby("year")["happiness_score"].agg(["mean", "std"]).reset_index()
years = yearly["year"].values
means = yearly["mean"].values
stds = yearly["std"].values

# Shaded band: mean ± 0.5 SD
ax.fill_between(years, means - 0.5 * stds, means + 0.5 * stds,
                color=COLORS["action"], alpha=0.12, zorder=1)

# Main line
ax.plot(years, means, color=COLORS["action"], linewidth=2.5, zorder=3, marker="o",
        markersize=4, markerfacecolor="white", markeredgewidth=1.5,
        markeredgecolor=COLORS["action"])

# COVID shading 2020-2022
ax.axvspan(2019.5, 2022.5, color="#6B7280", alpha=0.08, zorder=0)
ax.text(2021, means.min() - 0.05, "COVID\nyears", ha="center", va="top",
        fontsize=8, color=COLORS["muted"], style="italic")

# Annotate start and end
ax.annotate(f"{means[0]:.2f}", xy=(years[0], means[0]),
            xytext=(-14, 6), textcoords="offset points",
            fontsize=9, color=COLORS["gray900"], fontweight="bold")
ax.annotate(f"{means[-1]:.2f}", xy=(years[-1], means[-1]),
            xytext=(6, 0), textcoords="offset points",
            fontsize=9, color=COLORS["action"], fontweight="bold")

# Annotation: delta
delta = means[-1] - means[0]
ax.text(0.98, 0.05, f"+{delta:.2f} since 2011", transform=ax.transAxes,
        ha="right", va="bottom", fontsize=10, color=COLORS["success"],
        fontweight="bold")

ax.set_xlim(2010.5, 2025.5)
ax.set_ylim(5.2, 6.1)
ax.set_xticks(years)
ax.set_xticklabels([str(y) if y % 2 == 1 else "" for y in years], fontsize=8)
ax.set_ylabel("Average Happiness Score (0-10)", fontsize=9, color=COLORS["muted"])
ax.set_title("The World Is Getting Happier -- Even Through COVID", fontsize=14,
             fontweight="bold", pad=12, loc="left")
ax.text(0, 1.01, "Balanced panel: 129 countries present all 14 years  |  Shaded band = ±0.5 SD",
        transform=ax.transAxes, fontsize=7.5, color=COLORS["muted"])

ax.spines["left"].set_visible(False)
ax.yaxis.set_tick_params(length=0)
ax.set_axisbelow(True)

fig.tight_layout()
fig.savefig(OUTPUT / "happiness_01_global_trend.png", dpi=150, bbox_inches="tight")
plt.close()
print("Chart 1 saved.")

# ════════════════════════════════════════════════════════════════════════════════
# CHART 2 -- Top risers and fallers 2011 → 2025 (balanced panel only)
# ════════════════════════════════════════════════════════════════════════════════
colors = swd_style()

score_2011 = df_bal[df_bal["year"] == 2011].set_index("country")["happiness_score"]
score_2025 = df_bal[df_bal["year"] == 2025].set_index("country")["happiness_score"]
change = (score_2025 - score_2011).dropna().rename("change")
change_df = pd.DataFrame({
    "s2011": score_2011,
    "s2025": score_2025,
    "change": change,
}).dropna()

top_risers = change_df.nlargest(8, "change")
top_fallers = change_df.nsmallest(8, "change")
plot_df = pd.concat([top_risers, top_fallers]).sort_values("change")

fig, ax = plt.subplots(figsize=(9, 8))

y_pos = range(len(plot_df))
countries = plot_df.index.tolist()
s2011 = plot_df["s2011"].values
s2025 = plot_df["s2025"].values
changes = plot_df["change"].values

for i, (c, y11, y25, chg) in enumerate(zip(countries, s2011, s2025, changes)):
    col = COLORS["success"] if chg > 0 else COLORS["negative"]
    # Line connecting 2011 → 2025
    ax.plot([y11, y25], [i, i], color=col, linewidth=1.5, zorder=2, alpha=0.7)
    # 2011 dot (hollow)
    ax.scatter(y11, i, color="white", edgecolors=COLORS["muted"],
               linewidths=1.2, s=55, zorder=3)
    # 2025 dot (filled)
    ax.scatter(y25, i, color=col, s=70, zorder=4)
    # Change label
    label = f"+{chg:.2f}" if chg > 0 else f"{chg:.2f}"
    x_label = max(y11, y25) + 0.06 if chg > 0 else min(y11, y25) - 0.06
    ha = "left" if chg > 0 else "right"
    ax.text(x_label, i, label, va="center", ha=ha, fontsize=8.5,
            color=col, fontweight="bold")

ax.set_yticks(list(y_pos))
ax.set_yticklabels(countries, fontsize=9)
ax.set_xlabel("Happiness Score", fontsize=9, color=COLORS["muted"])
ax.set_title("Who Rose, Who Fell: 14 Years of Happiness Change", fontsize=13,
             fontweight="bold", pad=12, loc="left")
ax.text(0, 1.01,
        "Each country: open dot = 2011 score, filled dot = 2025 score  |  Balanced panel, 129 countries",
        transform=ax.transAxes, fontsize=7.5, color=COLORS["muted"])

# Divider line between fallers and risers
ax.axhline(y=7.5, color=COLORS["gray400"], linewidth=0.8, linestyle="--")
ax.text(3.5, 7.55, "Risers", fontsize=8, color=COLORS["success"], fontweight="bold")
ax.text(3.5, 7.35, "Fallers", fontsize=8, color=COLORS["negative"], fontweight="bold")

legend_elements = [
    Line2D([0], [0], marker="o", color="w", markerfacecolor="white",
           markeredgecolor=COLORS["muted"], markersize=7, label="2011 score"),
    Line2D([0], [0], marker="o", color="w", markerfacecolor=COLORS["action"],
           markersize=7, label="2025 score"),
]
ax.legend(handles=legend_elements, loc="lower right", fontsize=8, frameon=False)

ax.spines["left"].set_visible(False)
ax.xaxis.set_tick_params(length=0)
ax.set_xlim(2.8, 8.0)

fig.tight_layout()
fig.savefig(OUTPUT / "happiness_02_movers.png", dpi=150, bbox_inches="tight")
plt.close()
print("Chart 2 saved.")

# ════════════════════════════════════════════════════════════════════════════════
# CHART 3 -- Factor profile: top 10 vs bottom 10 (2025, stacked bar)
# ════════════════════════════════════════════════════════════════════════════════
colors = swd_style()

df_2025 = df[df["year"] == 2025].dropna(subset=FACTOR_COLS).copy()
top10 = df_2025.nlargest(10, "happiness_score")
bot10 = df_2025.nsmallest(10, "happiness_score")

RESIDUAL_LABEL = "Unexplained (dystopia + residual)"

def mean_factors(group):
    row = {}
    for col in FACTOR_COLS:
        row[FACTOR_LABELS[col]] = group[col].mean()
    row[RESIDUAL_LABEL] = group["dystopia_plus_residual"].mean()
    return pd.Series(row)

top_factors = mean_factors(top10)
bot_factors = mean_factors(bot10)

fig, ax = plt.subplots(figsize=(10, 5.5))

group_x = [0, 0.55]
all_colors = FACTOR_COLORS + ["#D1D5DB"]
all_labels = list(FACTOR_LABELS.values()) + [RESIDUAL_LABEL]
top_stack = [top_factors[f] if f in top_factors.index else 0 for f in all_labels]
bot_stack = [bot_factors[f] if f in bot_factors.index else 0 for f in all_labels]

bottom_top = 0
bottom_bot = 0
bar_w = 0.4
for i, (lbl, col) in enumerate(zip(all_labels, all_colors)):
    tv = top_stack[i]
    bv = bot_stack[i]
    ax.bar(group_x[0], tv, bottom=bottom_top, width=bar_w, color=col,
           alpha=0.92, label=lbl)
    ax.bar(group_x[1], bv, bottom=bottom_bot, width=bar_w, color=col,
           alpha=0.55)
    bottom_top += tv
    bottom_bot += bv

# Annotate total scores
ax.text(group_x[0], bottom_top + 0.05, f"{bottom_top:.1f}", ha="center",
        fontsize=11, fontweight="bold", color=COLORS["gray900"])
ax.text(group_x[1], bottom_bot + 0.05, f"{bottom_bot:.1f}", ha="center",
        fontsize=11, fontweight="bold", color=COLORS["gray900"])

group_labels = ["Top 10 countries\n(avg score 7.33)", "Bottom 10 countries\n(avg score 3.36)"]
ax.set_xticks(group_x)
ax.set_xticklabels(group_labels, fontsize=10)
ax.set_ylabel("Score contribution", fontsize=9, color=COLORS["muted"])
ax.set_title("What Separates the Happiest from the Least Happy Countries", fontsize=13,
             fontweight="bold", pad=12, loc="left")
ax.text(0, 1.01,
        "Stacked bars show average contribution of each factor to happiness score  |  2025 data  |  Source: World Happiness Report",
        transform=ax.transAxes, fontsize=7.5, color=COLORS["muted"])
ax.set_xlim(-0.3, 1.0)
ax.set_ylim(0, 9.5)

ax.legend(loc="upper right", fontsize=7.5, frameon=False, ncol=1,
          bbox_to_anchor=(1.0, 0.98))

ax.spines["left"].set_visible(False)
ax.yaxis.set_tick_params(length=0)

fig.tight_layout()
fig.savefig(OUTPUT / "happiness_03_factor_profile.png", dpi=150, bbox_inches="tight")
plt.close()
print("Chart 3 saved.")

# ════════════════════════════════════════════════════════════════════════════════
# CHART 4 -- Factor importance: correlation vs happiness (2019-2025)
# ════════════════════════════════════════════════════════════════════════════════
colors = swd_style()

df_factors = df.dropna(subset=FACTOR_COLS).copy()
corrs = {}
for col in FACTOR_COLS:
    corrs[FACTOR_LABELS[col]] = df_factors[col].corr(df_factors["happiness_score"])

corr_df = pd.Series(corrs).sort_values()

fig, ax = plt.subplots(figsize=(8, 5))

bar_colors_corr = []
for lbl in corr_df.index:
    if corr_df[lbl] > 0.6:
        bar_colors_corr.append(COLORS["action"])
    elif corr_df[lbl] > 0.4:
        bar_colors_corr.append(COLORS["accent"])
    else:
        bar_colors_corr.append(COLORS["gray400"])

bars = ax.barh(corr_df.index, corr_df.values, color=bar_colors_corr,
               height=0.55, alpha=0.9)

for bar, val in zip(bars, corr_df.values):
    ax.text(val + 0.008, bar.get_y() + bar.get_height() / 2,
            f"{val:.2f}", va="center", fontsize=9, fontweight="bold",
            color=COLORS["gray900"])

ax.axvline(x=0, color=COLORS["gray600"], linewidth=0.8)
ax.set_xlim(0, 0.85)
ax.set_xlabel("Correlation with happiness score (r)", fontsize=9, color=COLORS["muted"])
ax.set_title("Social Bonds and Wealth Drive Happiness;\nGenerosity Barely Registers", fontsize=13,
             fontweight="bold", pad=12, loc="left")
ax.text(0, 1.02,
        "Pearson r between each factor contribution and happiness score  |  2019-2025  |  n = 1,013 country-years",
        transform=ax.transAxes, fontsize=7.5, color=COLORS["muted"])

# Annotations -- placed to avoid overlap with value labels
ax.text(0.42, 5.48, "Strongest predictor",
        va="bottom", fontsize=8, color=COLORS["action"], style="italic")
ax.text(corr_df["Generosity"] + 0.05, 0, "Near zero effect",
        va="center", fontsize=8, color=COLORS["gray600"], style="italic")

ax.spines["left"].set_visible(False)
ax.spines["bottom"].set_visible(False)
ax.xaxis.set_tick_params(length=0)
ax.yaxis.set_tick_params(length=0)

fig.tight_layout()
fig.savefig(OUTPUT / "happiness_04_factor_importance.png", dpi=150, bbox_inches="tight")
plt.close()
print("Chart 4 saved.")

print("\nAll 4 charts saved to outputs/")
