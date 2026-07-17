import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

os.makedirs("outputs/charts", exist_ok=True)

from helpers.chart_helpers import (
    hadi_dark, highlight_bar, highlight_line, action_title,
    check_label_collisions, save_chart
)

theme = hadi_dark()

# hadi_dark() returns the theme dict and updates COLORS. But action_title
# hardcodes COLORS["gray900"] (dark) for titles.  Override module-level
# COLORS so titles, subtitles, and labels are visible on dark backgrounds.
from helpers.chart_helpers import COLORS
COLORS["gray900"] = "#f1f5f9"   # Slate 100 — for headings on dark bg
COLORS["gray600"] = "#94a3b8"   # Slate 400 — for subtitles on dark bg
COLORS["gray400"] = "#64748b"   # Slate 500 — for muted labels on dark bg
COLORS["gray100"] = "#334155"   # Slate 700 — for grid lines on dark bg
colors = dict(COLORS)

# Dark-theme specific palette for stacked / grouped elements
DARK_HIGHLIGHT = "#3b82f6"      # Blue 500
DARK_MUTED     = "#334155"      # Slate 700
DARK_TEXT       = "#f1f5f9"     # Slate 100
DARK_TEXT_MUTED = "#94a3b8"     # Slate 400
DARK_SURFACE    = "#1e293b"     # Slate 800

print("Loading data...")
df = pd.read_parquet("working/netflix/clean_df.parquet")
cluster_df = pd.read_csv("working/netflix/cluster_data.csv")
profiles = pd.read_csv("working/netflix/cluster_profiles.csv")

CLUSTER_LABELS = {
    0: "Documentary Movies",
    1: "International Drama Movies",
    2: "US Kids TV",
    3: "International TV",
    4: "Children & Family Movies"
}

# -----------------------------------------------------------------------------
# BEAT 01: Multi-line — US TV vs Movie fresh%
# -----------------------------------------------------------------------------
print("Generating beat_01...")
us_df = df[(df['country_bucket'] == 'US') & (df['year_added'] >= 2015) & (df['year_added'] <= 2021)].copy()
us_df['is_fresh'] = (us_df['acquisition_lag'] == 0.0)
fresh_trend = us_df.groupby(['year_added', 'type'])['is_fresh'].mean().unstack() * 100

fig, ax = plt.subplots(figsize=(10, 6))
x_vals = fresh_trend.index.values
y_dict = {
    'TV Show': fresh_trend['TV Show'].values,
    'Movie': fresh_trend['Movie'].values
}
highlight_line(ax, x_vals, y_dict, highlight='TV Show')

# Annotate crossing point — where TV freshness exceeds Movie
cross_year = None
for i in range(1, len(x_vals)):
    if fresh_trend['TV Show'].iloc[i-1] < fresh_trend['Movie'].iloc[i-1] and fresh_trend['TV Show'].iloc[i] > fresh_trend['Movie'].iloc[i]:
        cross_year = x_vals[i]
        cross_y = fresh_trend['TV Show'].iloc[i]
        break

if cross_year:
    ax.annotate(f"TV becomes fresher\n(~{cross_year})",
                xy=(cross_year, cross_y),
                xytext=(cross_year, cross_y + 15),
                arrowprops=dict(arrowstyle="->", color=DARK_TEXT_MUTED),
                color=DARK_TEXT_MUTED, fontsize=10, ha='center')

action_title(ax,
    "US TV acquisition is accelerating freshness while Movies pivot to library",
    "Percentage of US additions acquired in their release year (lag=0)")

check_label_collisions(fig, ax, fix=True)
save_chart(fig, "outputs/charts/beat_01.png")
save_chart(fig, "outputs/charts/beat_01.svg")
plt.close(fig)
print("  beat_01 done")

# -----------------------------------------------------------------------------
# BEAT 02: Stacked bar — US Movie lag-band distribution
# -----------------------------------------------------------------------------
print("Generating beat_02...")
us_movies = us_df[us_df['type'] == 'Movie'].copy()

def get_lag_band(lag):
    if pd.isna(lag): return "Unknown"
    if lag == 0: return "Fresh (0)"
    if 1 <= lag <= 2: return "Recent (1-2)"
    if 3 <= lag <= 5: return "Mid (3-5)"
    return "Library (6+)"

us_movies['lag_band'] = us_movies['acquisition_lag'].apply(get_lag_band)
band_order = ["Fresh (0)", "Recent (1-2)", "Mid (3-5)", "Library (6+)"]

band_trend = us_movies.groupby(['year_added', 'lag_band']).size().unstack(fill_value=0)
band_trend_pct = band_trend.div(band_trend.sum(axis=1), axis=0) * 100
for col in band_order:
    if col not in band_trend_pct.columns:
        band_trend_pct[col] = 0
band_trend_pct = band_trend_pct[band_order]

fig, ax = plt.subplots(figsize=(10, 6))
BAND_COLORS = {
    "Fresh (0)":    "#64748b",   # Slate 500 — readable on dark bg
    "Recent (1-2)": "#475569",   # Slate 600
    "Mid (3-5)":    "#334155",   # Slate 700 — near-background, subtle
    "Library (6+)": DARK_HIGHLIGHT  # Blue 500 — highlighted band
}
bottom = np.zeros(len(band_trend_pct))
categories = band_trend_pct.index.astype(str)
for col in band_order:
    col_vals = band_trend_pct[col].values
    ax.bar(categories, col_vals, bottom=bottom, color=BAND_COLORS[col], edgecolor='white', width=0.7, label=col)
    if col == "Library (6+)":
        for i, val in enumerate(col_vals):
            if val > 8:
                ax.text(i, bottom[i] + val/2, f"{val:.0f}%", ha='center', va='center', color='white', fontweight='bold', fontsize=9)
    bottom += col_vals

# Add legend for bands — dark background
legend = ax.legend(frameon=False, loc='upper center', bbox_to_anchor=(0.5, 1.05), ncol=4)
for text in legend.get_texts():
    text.set_color(DARK_TEXT_MUTED)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.yaxis.grid(True, color=DARK_MUTED, linewidth=0.5)
ax.set_axisbelow(True)

action_title(ax,
    "US Movie additions are now dominated by deep library content (lag > 5yr)",
    "Acquisition lag distribution for US Movie additions, 2015-2021")

check_label_collisions(fig, ax, fix=True)
save_chart(fig, "outputs/charts/beat_02.png")
save_chart(fig, "outputs/charts/beat_02.svg")
plt.close(fig)
print("  beat_02 done")

# -----------------------------------------------------------------------------
# BEAT 03: Horizontal bar — Change in library% by cluster
# -----------------------------------------------------------------------------
print("Generating beat_03...")
us_movies_w_cluster = us_movies.merge(cluster_df[['show_id', 'cluster']], on='show_id', how='inner')
us_movies_w_cluster['is_library'] = (us_movies_w_cluster['lag_band'] == 'Library (6+)')
us_movies_w_cluster['period'] = np.where(us_movies_w_cluster['year_added'] <= 2017, 'pre', 'post')
us_movies_w_cluster['cluster_label'] = us_movies_w_cluster['cluster'].map(CLUSTER_LABELS)

lib_by_cluster = us_movies_w_cluster.groupby(['cluster_label', 'period'])['is_library'].mean().unstack() * 100
lib_by_cluster['change'] = lib_by_cluster['post'] - lib_by_cluster['pre']
lib_change = lib_by_cluster['change'].dropna().sort_values()

fig, ax = plt.subplots(figsize=(10, 6))
cats = lib_change.index.values
vals = lib_change.values

# highlight the International Drama and Children & Family
highlight_target = ["International Drama Movies", "Children & Family Movies"]
highlight_bar(ax, cats, vals, highlight=highlight_target, horizontal=True, sort=False,
              highlight_color=DARK_HIGHLIGHT, base_color=DARK_MUTED)

# Add pp-change value labels
for i, val in enumerate(vals):
    color = DARK_HIGHLIGHT if cats[i] in highlight_target else DARK_TEXT_MUTED
    ax.text(val + 1, i, f"+{val:.1f}pp", va='center', color=color, fontweight='bold', fontsize=10)

action_title(ax,
    "International Drama and Children & Family drive the library licensing pivot",
    "Percentage point change in deep library share, Post-2018 vs Pre-2018")

check_label_collisions(fig, ax, fix=True)
save_chart(fig, "outputs/charts/beat_03.png")
save_chart(fig, "outputs/charts/beat_03.svg")
plt.close(fig)
print("  beat_03 done")

# -----------------------------------------------------------------------------
# BEAT 04: Grouped bar — Director Observed vs Expected by cluster
# -----------------------------------------------------------------------------
print("Generating beat_04...")
movies_w_directors = df[(df['type'] == 'Movie') & (df['director'].notna())].copy()
movies_w_directors = movies_w_directors.merge(cluster_df[['show_id', 'cluster']], on='show_id', how='inner')
movies_w_directors['cluster_label'] = movies_w_directors['cluster'].map(CLUSTER_LABELS)

# Base rate: overall cluster distribution for attributed movies
base_rates = movies_w_directors['cluster_label'].value_counts(normalize=True) * 100

# Top-50 directors: most prolific by attributed title count
director_counts = movies_w_directors.groupby('director').size()
top_50_dirs = director_counts.nlargest(50).index

top_50_movies = movies_w_directors[movies_w_directors['director'].isin(top_50_dirs)]
observed_rates = top_50_movies['cluster_label'].value_counts(normalize=True) * 100

# Combine — focus on Documentary, Intl Drama, and Children & Family
comparison = pd.DataFrame({
    'Catalog Base Rate': base_rates,
    'Top 50 Directors': observed_rates
}).fillna(0)

# Sort by Catalog Base Rate descending
comparison = comparison.sort_values('Catalog Base Rate', ascending=False)

# For visualization: show top 5 clusters to ensure Documentary is included
to_plot = comparison.head(5).copy()
to_plot['Lift'] = to_plot['Top 50 Directors'] / to_plot['Catalog Base Rate']
to_plot['Lift'] = to_plot['Lift'].replace([np.inf, np.nan], 0)

fig, ax = plt.subplots(figsize=(10, 6))
y = np.arange(len(to_plot))
h = 0.35

ax.barh(y - h/2, to_plot['Catalog Base Rate'], h, label='Catalog Base Rate', color=colors["gray200"])

obs_colors = [colors["action"] if row['Lift'] >= 1.1 else colors["accent"] for _, row in to_plot.iterrows()]
ax.barh(y + h/2, to_plot['Top 50 Directors'], h, label='Top 50 Directors', color=obs_colors)

ax.set_yticks(y)
ax.set_yticklabels(to_plot.index, fontsize=11)
ax.invert_yaxis()

# Lift annotation — only for Documentary and Children & Family
for i, (idx, row) in enumerate(to_plot.iterrows()):
    lift = row['Lift']
    if lift > 0:
        ax.text(row['Top 50 Directors'] + 1, y[i] + h/2, f"{lift:.2f}x", va='center', fontsize=9,
                color=colors["action"] if lift >= 1.1 else colors["accent"])

ax.set_xlabel('% of attributed titles', color=DARK_TEXT_MUTED)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.xaxis.grid(True, color=DARK_MUTED, linewidth=0.5)
ax.set_axisbelow(True)

action_title(ax,
    "Netflix lacks repeat relationships with Documentary directors",
    "Observed % vs. Catalog Base Rate % for the 50 most prolific directors")

check_label_collisions(fig, ax, fix=True)
save_chart(fig, "outputs/charts/beat_04.png")
save_chart(fig, "outputs/charts/beat_04.svg")
plt.close(fig)
print("  beat_04 done")

# -----------------------------------------------------------------------------
# BEAT 05: Line chart — UK sparse metadata rate by vintage
# -----------------------------------------------------------------------------
print("Generating beat_05...")
uk_df = df[df['country_bucket'] == 'UK'].copy()
uk_df['decade'] = (uk_df['release_year'] // 10) * 10
uk_df['is_sparse'] = (uk_df['completeness_tier'] == 'Sparse')

uk_df['vintage'] = uk_df['decade'].apply(lambda x: 'Pre-2000s' if x < 2000 else f"{int(x)}s")
sparse_rate = uk_df.groupby('vintage')['is_sparse'].mean() * 100

vintages = ['Pre-2000s', '2000s', '2010s', '2020s']
sparse_rate = sparse_rate.reindex(vintages).fillna(0)

fig, ax = plt.subplots(figsize=(10, 6))
x_vals = np.arange(len(vintages))

ax.plot(x_vals, sparse_rate.values, color=DARK_HIGHLIGHT, marker='o', linewidth=4,
        markersize=10, markeredgecolor=DARK_SURFACE, markeredgewidth=2)
for i, val in enumerate(sparse_rate.values):
    ax.text(i, val + 0.8, f"{val:.1f}%", ha='center', va='bottom', color=DARK_TEXT, fontweight='bold', fontsize=11)

ax.set_xticks(x_vals)
ax.set_xticklabels(vintages, fontsize=12)
ax.set_ylim(0, max(sparse_rate.values) + 5)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.yaxis.grid(True, color=DARK_MUTED, linewidth=0.5)
ax.set_axisbelow(True)

action_title(ax,
    "Sparse metadata rates are rising for recent UK acquisitions",
    "% of UK titles with sparse metadata by content vintage")

check_label_collisions(fig, ax, fix=True)
save_chart(fig, "outputs/charts/beat_05.png")
save_chart(fig, "outputs/charts/beat_05.svg")
plt.close(fig)
print("  beat_05 done")

# -----------------------------------------------------------------------------
# BEAT 06: Grouped bar — US vs Intl 1-season rate by cohort
# -----------------------------------------------------------------------------
print("Generating beat_06...")
tv_df = df[(df['type'] == 'TV Show') & (df['duration_seasons'].notna())].copy()
tv_df['is_1season'] = (tv_df['duration_seasons'] == 1.0)

def cohort_label(x):
    if 2015 <= x <= 2018: return '2015-18'
    if x == 2021: return '2021'
    return 'Exclude'

def region_label(cb):
    if cb == 'US': return 'US'
    if cb in ['Unknown', 'Multiple']: return 'Exclude'
    return 'International'

tv_df['cohort'] = tv_df['year_added'].apply(cohort_label)
tv_df['region'] = tv_df['country_bucket'].apply(region_label)
tv_df = tv_df[(tv_df['cohort'] != 'Exclude') & (tv_df['region'] != 'Exclude')]

rate_table = tv_df.groupby(['cohort', 'region'])['is_1season'].mean().unstack() * 100
# Sort cohorts in order
cohort_order = ['2015-18', '2021']
rate_table = rate_table.loc[cohort_order]

fig, ax = plt.subplots(figsize=(10, 6))
x = np.arange(len(rate_table.index))
w = 0.4

ax.bar(x - w/2, rate_table['US'], w, label='US', color=DARK_MUTED)
ax.bar(x + w/2, rate_table['International'], w, label='International', color=DARK_HIGHLIGHT)

ax.set_xticks(x)
ax.set_xticklabels(rate_table.index, fontsize=12)

# Direct labels on bars
for i, idx in enumerate(rate_table.index):
    us_val = rate_table['US'].loc[idx]
    intl_val = rate_table['International'].loc[idx]
    ax.text(i - w/2, us_val + 1.5, f"{us_val:.1f}%", ha='center', va='bottom', color=DARK_TEXT_MUTED, fontweight='bold', fontsize=10)
    ax.text(i + w/2, intl_val + 1.5, f"{intl_val:.1f}%", ha='center', va='bottom', color=DARK_HIGHLIGHT, fontweight='bold', fontsize=10)

# Mark the inversion
if rate_table['International'].iloc[1] < rate_table['US'].iloc[1]:
    ax.annotate('Inversion', xy=(x[1] + w/2, rate_table['International'].iloc[1]),
                xytext=(x[1] + w/2 + 0.35, rate_table['International'].iloc[1] + 15),
                arrowprops=dict(arrowstyle='->', connectionstyle="arc3,rad=.2", color=DARK_HIGHLIGHT),
                color=DARK_HIGHLIGHT, fontsize=10, fontweight='bold')

ax.set_ylim(0, rate_table.max().max() + 25)
ax.set_ylabel('% of TV Shows with only 1 season', color=DARK_TEXT_MUTED)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.yaxis.grid(True, color=DARK_MUTED, linewidth=0.5)
ax.set_axisbelow(True)

# Style legend for dark background
legend = ax.legend(frameon=False, loc='upper center', bbox_to_anchor=(0.5, 1.05), ncol=2)
for text in legend.get_texts():
    text.set_color(DARK_TEXT_MUTED)

action_title(ax,
    "International TV is maturing: 1-season rates dropped below US in 2021",
    "% of TV Shows with only 1 season by acquisition cohort\n(2021 = partial year through ~Sep)")

check_label_collisions(fig, ax, fix=False)
save_chart(fig, "outputs/charts/beat_06.png")
save_chart(fig, "outputs/charts/beat_06.svg")
plt.close(fig)
print("  beat_06 done")

print("\nAll charts generated successfully.")
print("Files:")
for i in range(1, 7):
    print(f"  outputs/charts/beat_{i:02d}.png")