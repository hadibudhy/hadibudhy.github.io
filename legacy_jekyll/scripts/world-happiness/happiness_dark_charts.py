"""
World Happiness 2011-2025 -- Dark theme charts matching portfolio style
"""
import sys
sys.path.insert(0, ".")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
from pathlib import Path

OUTPUT = Path("outputs")
OUTPUT.mkdir(exist_ok=True)

# ── Dark theme palette (matches existing portfolio charts) ─────────────────────
BG       = "#0F1923"   # outer background
PLOT_BG  = "#17212E"   # plot area
BLUE     = "#4B8EF5"   # primary data color
BLUE2    = "#6BA3F7"   # lighter blue
GRAY     = "#8899AA"   # muted / de-emphasis
WHITE    = "#FFFFFF"
RED      = "#E05252"   # fallers / negative
GREEN    = "#52C08A"   # risers / positive
GRID     = "#1E2D3E"   # subtle grid lines
ANNOT    = "#AAC4E8"   # annotation text

def dark_base(figsize=(11, 5.5)):
    fig, ax = plt.subplots(figsize=figsize, facecolor=BG)
    fig.subplots_adjust(top=0.82)          # reserve room for title + subtitle
    ax.set_facecolor(PLOT_BG)
    ax.tick_params(colors=GRAY, labelsize=9)
    ax.xaxis.label.set_color(GRAY)
    ax.yaxis.label.set_color(GRAY)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.grid(axis="y", color=GRID, linewidth=0.7, zorder=0)
    return fig, ax

def set_title(fig, title, subtitle=""):
    """Place title + subtitle above plot area using figure coordinates."""
    fig.text(0.01, 0.97, title, color=WHITE, fontsize=14, fontweight="bold",
             va="top", ha="left", transform=fig.transFigure)
    if subtitle:
        fig.text(0.01, 0.90, subtitle, color=GRAY, fontsize=8.5,
                 va="top", ha="left", transform=fig.transFigure)

# ── Load data ──────────────────────────────────────────────────────────────────
df = pd.read_csv("data/world_happiness_report_2005_2025.csv")

all_years = set(df["year"].unique())
country_years = df.groupby("country")["year"].apply(set)
balanced = country_years[country_years.apply(lambda s: s == all_years)].index
df_bal = df[df["country"].isin(balanced)].copy()

FACTOR_COLS = [c for c in df.columns if c.startswith("explained_")]
FACTOR_LABELS = {
    "explained_log_gdp_per_capita":        "GDP per capita",
    "explained_social_support":            "Social support",
    "explained_healthy_life_expectancy":   "Life expectancy",
    "explained_freedom":                   "Freedom",
    "explained_corruption":                "Low corruption",
    "explained_generosity":                "Generosity",
}
RESIDUAL_LABEL = "Unexplained (dystopia + residual)"

# ════════════════════════════════════════════════════════════════════════════════
# CHART 1 -- Global happiness trend (balanced panel)
# ════════════════════════════════════════════════════════════════════════════════
fig, ax = dark_base(figsize=(11, 5.5))

yearly = df_bal.groupby("year")["happiness_score"].agg(["mean", "std"]).reset_index()
years = yearly["year"].values
means = yearly["mean"].values
stds  = yearly["std"].values

ax.fill_between(years, means - 0.5*stds, means + 0.5*stds,
                color=BLUE, alpha=0.12, zorder=1)
ax.plot(years, means, color=BLUE, linewidth=2.5, zorder=3,
        marker="o", markersize=5, markerfacecolor=PLOT_BG,
        markeredgewidth=2, markeredgecolor=BLUE)

# COVID shading
ax.axvspan(2019.5, 2022.5, color=GRAY, alpha=0.08, zorder=0)
ax.text(2021, means.min() - 0.03, "COVID\nyears",
        ha="center", va="top", fontsize=8, color=GRAY, style="italic")

# End-point labels
ax.text(years[0] - 0.2, means[0], f"{means[0]:.2f}",
        ha="right", va="center", fontsize=9.5, color=WHITE, fontweight="bold")
ax.text(years[-1] + 0.2, means[-1], f"{means[-1]:.2f}",
        ha="left", va="center", fontsize=9.5, color=BLUE, fontweight="bold")

# Delta callout
ax.text(0.98, 0.05, f"+{means[-1]-means[0]:.2f} since 2011",
        transform=ax.transAxes, ha="right", va="bottom",
        fontsize=10, color=GREEN, fontweight="bold")

ax.set_xlim(2010.3, 2025.7)
ax.set_ylim(5.15, 6.15)
ax.set_xticks(years)
ax.set_xticklabels([str(y) if y % 2 == 1 else "" for y in years], color=GRAY, fontsize=8)
ax.yaxis.set_tick_params(length=0)

set_title(fig,
    "The World Is Getting Happier -- Even Through COVID",
    "Balanced panel: 129 countries present all 14 years  |  Shaded band = ±0.5 SD  |  Source: World Happiness Report")

fig.savefig(OUTPUT / "happiness-beat01.png", dpi=150, bbox_inches="tight", facecolor=BG)
plt.close()
print("Chart 1 saved.")

# ════════════════════════════════════════════════════════════════════════════════
# CHART 2 -- Risers and fallers dumbbell (balanced panel)
# ════════════════════════════════════════════════════════════════════════════════
fig, ax = dark_base(figsize=(10, 9))
ax.grid(axis="x", color=GRID, linewidth=0.7, zorder=0)
ax.grid(axis="y", visible=False)

s2011 = df_bal[df_bal["year"]==2011].set_index("country")["happiness_score"]
s2025 = df_bal[df_bal["year"]==2025].set_index("country")["happiness_score"]
change = (s2025 - s2011).dropna()
change_df = pd.DataFrame({"s2011": s2011, "s2025": s2025, "change": change}).dropna()

top_risers = change_df.nlargest(8, "change")
top_fallers = change_df.nsmallest(8, "change")
plot_df = pd.concat([top_risers, top_fallers]).sort_values("change")

for i, (country, row) in enumerate(plot_df.iterrows()):
    col = GREEN if row["change"] > 0 else RED
    ax.plot([row["s2011"], row["s2025"]], [i, i],
            color=col, linewidth=1.8, alpha=0.8, zorder=2)
    ax.scatter(row["s2011"], i, color=PLOT_BG, edgecolors=GRAY,
               linewidths=1.5, s=60, zorder=3)
    ax.scatter(row["s2025"], i, color=col, s=70, zorder=4)
    label = f"+{row['change']:.2f}" if row["change"] > 0 else f"{row['change']:.2f}"
    if row["change"] > 0:
        ax.text(row["s2025"] + 0.07, i, label, va="center", ha="left",
                fontsize=8.5, color=col, fontweight="bold")
    else:
        # place to the left of 2025 dot -- clear of the connecting line
        ax.text(row["s2025"] - 0.12, i, label, va="center", ha="right",
                fontsize=8.5, color=col, fontweight="bold")

ax.set_yticks(range(len(plot_df)))
ax.set_yticklabels(plot_df.index.tolist(), color=WHITE, fontsize=9.5)
ax.set_xlabel("Happiness Score (0-10)", color=GRAY, fontsize=9)
ax.set_xlim(0.8, 8.5)   # xlim left at 0.8 so Afghanistan dot (1.45) is fully visible

# Divider
ax.axhline(y=7.5, color=GRAY, linewidth=0.8, linestyle="--", alpha=0.5)
ax.text(0.9, 7.7, "Risers", fontsize=8.5, color=GREEN, fontweight="bold")
ax.text(0.9, 7.2, "Fallers", fontsize=8.5, color=RED, fontweight="bold")

legend_elements = [
    Line2D([0],[0], marker="o", color="w", markerfacecolor=PLOT_BG,
           markeredgecolor=GRAY, markersize=7, label="2011 score (open dot)"),
    Line2D([0],[0], marker="o", color="w", markerfacecolor=GREEN,
           markersize=7, label="2025 score — riser"),
    Line2D([0],[0], marker="o", color="w", markerfacecolor=RED,
           markersize=7, label="2025 score — faller"),
]
legend = ax.legend(handles=legend_elements, loc="lower right",
                   fontsize=8, frameon=True, facecolor=PLOT_BG,
                   edgecolor=GRID, labelcolor=WHITE)

set_title(fig,
    "Who Rose, Who Fell: 14 Years of Happiness Change",
    "Open dot = 2011 score, filled dot = 2025 score  |  Balanced panel, 129 countries  |  Source: World Happiness Report")

fig.savefig(OUTPUT / "happiness-beat02.png", dpi=150, bbox_inches="tight", facecolor=BG)
plt.close()
print("Chart 2 saved.")

# ════════════════════════════════════════════════════════════════════════════════
# CHART 3 -- Factor decomposition: top 10 vs bottom 10 (2025)
# ════════════════════════════════════════════════════════════════════════════════
fig, ax = dark_base(figsize=(10, 5.5))
ax.grid(axis="y", visible=False)

df_2025 = df[df["year"]==2025].dropna(subset=FACTOR_COLS).copy()
top10 = df_2025.nlargest(10, "happiness_score")
bot10 = df_2025.nsmallest(10, "happiness_score")

def mean_factors(group):
    row = {FACTOR_LABELS[c]: group[c].mean() for c in FACTOR_COLS}
    row[RESIDUAL_LABEL] = group["dystopia_plus_residual"].mean()
    return pd.Series(row)

top_f = mean_factors(top10)
bot_f = mean_factors(bot10)

all_labels = list(FACTOR_LABELS.values()) + [RESIDUAL_LABEL]
bar_colors = ["#4B8EF5","#52C08A","#E05252","#9B6EF5","#F5A64B","#8899AA","#4A6080"]
bar_w = 0.32
group_x = [0.2, 0.75]

bt = 0; bb = 0
for i, (lbl, col) in enumerate(zip(all_labels, bar_colors)):
    tv = top_f[lbl]
    bv = bot_f[lbl]
    ax.bar(group_x[0], tv, bottom=bt, width=bar_w, color=col,
           alpha=0.9, label=lbl, zorder=2)
    ax.bar(group_x[1], bv, bottom=bb, width=bar_w, color=col,
           alpha=0.55, zorder=2)
    bt += tv; bb += bv

# Total score labels
ax.text(group_x[0], bt + 0.08, f"{bt:.1f}", ha="center",
        fontsize=12, fontweight="bold", color=WHITE, zorder=3)
ax.text(group_x[1], bb + 0.08, f"{bb:.1f}", ha="center",
        fontsize=12, fontweight="bold", color=WHITE, zorder=3)

ax.set_xticks(group_x)
ax.set_xticklabels([
    "Top 10 happiest\n(avg 7.33)",
    "Bottom 10 least happy\n(avg 3.36)",
], color=WHITE, fontsize=10.5)
ax.set_ylabel("Score contribution", color=GRAY, fontsize=9)
ax.set_xlim(-0.1, 1.1)
ax.set_ylim(0, 10)
ax.yaxis.set_tick_params(labelcolor=GRAY)

legend = ax.legend(loc="upper right", fontsize=7.5, frameon=True,
                   facecolor=PLOT_BG, edgecolor=GRID, labelcolor=WHITE,
                   ncol=1, bbox_to_anchor=(1.0, 0.98))

set_title(fig,
    "What Separates the Happiest from the Least Happy",
    "Average factor contribution to happiness score  |  2025 data, 147 countries  |  Source: World Happiness Report")

fig.savefig(OUTPUT / "happiness-beat03.png", dpi=150, bbox_inches="tight", facecolor=BG)
plt.close()
print("Chart 3 saved.")

# ════════════════════════════════════════════════════════════════════════════════
# CHART 4 -- Factor correlations (horizontal bar)
# ════════════════════════════════════════════════════════════════════════════════
fig, ax = dark_base(figsize=(9, 5))
ax.grid(axis="x", color=GRID, linewidth=0.7, zorder=0)
ax.grid(axis="y", visible=False)

df_f = df.dropna(subset=FACTOR_COLS).copy()
corrs = {FACTOR_LABELS[c]: df_f[c].corr(df_f["happiness_score"]) for c in FACTOR_COLS}
corr_s = pd.Series(corrs).sort_values()

bar_colors_c = [GRAY if v < 0.4 else (BLUE2 if v < 0.65 else BLUE)
                for v in corr_s.values]
bars = ax.barh(corr_s.index, corr_s.values, color=bar_colors_c,
               height=0.5, alpha=0.9, zorder=2)

for bar, val in zip(bars, corr_s.values):
    ax.text(val + 0.01, bar.get_y() + bar.get_height()/2,
            f"{val:.2f}", va="center", fontsize=9.5,
            fontweight="bold", color=WHITE)

# Annotations -- placed to avoid label overlap
ax.text(0.35, 5.48, "Strongest predictor", ha="left", va="bottom",
        fontsize=8.5, color=ANNOT, style="italic")
ax.text(0.13, 0, "Near zero effect",
        va="center", fontsize=8.5, color=GRAY, style="italic")

ax.set_xlim(0, 0.88)
ax.set_xlabel("Correlation with happiness score (r)", color=GRAY, fontsize=9)
ax.yaxis.set_tick_params(labelcolor=WHITE)

set_title(fig,
    "Social Bonds and Wealth Drive Happiness; Generosity Barely Registers",
    "Pearson r, factor contribution vs happiness score  |  2019-2025  |  n=1,013 country-years  |  Source: World Happiness Report")

fig.savefig(OUTPUT / "happiness-beat04.png", dpi=150, bbox_inches="tight", facecolor=BG)
plt.close()
print("Chart 4 saved.")

print("\nAll 4 dark-theme charts saved to outputs/")
