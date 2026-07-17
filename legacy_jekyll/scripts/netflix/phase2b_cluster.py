"""Phase 2b: Content archetype clustering (fixed)."""
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

df = pd.read_parquet(r"D:\Agent\ai-analyst\working\netflix\clean_df.parquet")

print("=" * 60)
print("ADVANCED ANALYSIS 5: Content Archetype Clustering")
print("=" * 60)

# Multi-hot encode top genres from the string column directly
top_genres = (
    df["listed_in"].str.split(", ").explode()
    .value_counts().head(15).index.tolist()
)
print("Top genres:", top_genres)

cluster_df = df.dropna(subset=["year_added", "acquisition_lag"]).copy()
cluster_df = cluster_df.reset_index(drop=True)

# Binary genre flags
for g in top_genres:
    safe = g.replace(" ", "_").replace("&", "and").replace("'", "")
    cluster_df[f"g_{safe}"] = cluster_df["listed_in"].str.contains(g, regex=False).fillna(False).astype(int)

# Encode categoricals
cluster_df["type_enc"] = LabelEncoder().fit_transform(cluster_df["type"])
cluster_df["rating_enc"] = LabelEncoder().fit_transform(cluster_df["rating_tier"])
cluster_df["lag_enc"] = LabelEncoder().fit_transform(cluster_df["lag_bucket"])

genre_cols = [c for c in cluster_df.columns if c.startswith("g_")]
feature_cols = genre_cols + ["type_enc", "rating_enc", "lag_enc"]

X = cluster_df[feature_cols].values.astype(float)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# PCA
pca = PCA(n_components=2, random_state=42)
X_pca = pca.fit_transform(X_scaled)
print(f"PCA explained variance: PC1={pca.explained_variance_ratio_[0]:.3f}, PC2={pca.explained_variance_ratio_[1]:.3f}")

# KMeans with k=5
km = KMeans(n_clusters=5, random_state=42, n_init=10)
cluster_df["cluster"] = km.fit_predict(X_scaled)
cluster_df["pca_x"] = X_pca[:, 0]
cluster_df["pca_y"] = X_pca[:, 1]

# Cluster profiles
profile = cluster_df.groupby("cluster").agg(
    count=("cluster", "size"),
    movie_share=("type", lambda x: (x == "Movie").mean()),
    adult_share=("rating_tier", lambda x: (x == "Adult").mean()),
    kids_share=("rating_tier", lambda x: (x == "Kids").mean()),
    median_lag=("acquisition_lag", "median"),
    avg_genre_count=("genre_count", "mean"),
    top_country=("country_bucket", lambda x: x.value_counts().index[0]),
).round(3)

# Dominant genre per cluster
for c in range(5):
    sub = cluster_df[cluster_df["cluster"] == c]
    genre_counts = sub[genre_cols].sum().sort_values(ascending=False)
    profile.loc[c, "top_genre_1"] = genre_counts.index[0].replace("g_", "").replace("_", " ")
    profile.loc[c, "top_genre_2"] = genre_counts.index[1].replace("g_", "").replace("_", " ")

print("\nCluster profiles:")
print(profile.to_string())

# Cluster labels
labels = {
    0: "Cluster 0",
    1: "Cluster 1",
    2: "Cluster 2",
    3: "Cluster 3",
    4: "Cluster 4",
}

# Growth analysis: 2016-2018 vs 2019-2021
print("\nCluster growth (2016-18 vs 2019-21 annual additions):")
for c in range(5):
    sub = cluster_df[cluster_df["cluster"] == c]
    early = len(sub[sub["year_added"].between(2016, 2018)]) / 3
    late = len(sub[sub["year_added"].between(2019, 2021)]) / 3
    ratio = late / early if early > 0 else 0
    trend = "BET" if ratio > 1.3 else ("HARVEST" if ratio < 0.8 else "STABLE")
    dominant_genre = profile.loc[c, "top_genre_1"]
    movie_pct = profile.loc[c, "movie_share"]
    print(f"  Cluster {c} [{dominant_genre}, {'Movie' if movie_pct > 0.6 else 'TV'}]: "
          f"{early:.0f} -> {late:.0f}/yr (x{ratio:.2f}) [{trend}]")

# Save
cluster_df[["show_id", "title", "type", "cluster", "pca_x", "pca_y",
            "year_added", "acquisition_lag", "rating_tier", "country_bucket"]].to_csv(
    r"D:\Agent\ai-analyst\working\netflix\cluster_data.csv", index=False
)
profile.to_csv(r"D:\Agent\ai-analyst\working\netflix\cluster_profiles.csv")
print("\nSaved cluster_data.csv and cluster_profiles.csv")
