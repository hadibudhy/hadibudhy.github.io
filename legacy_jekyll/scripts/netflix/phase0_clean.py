"""Phase 0: Data cleaning, feature engineering, quality flags."""
import pandas as pd
import numpy as np

df = pd.read_csv(r"D:\Agent\ai-analyst\data\netflix_titles.csv")

# --- Parse date_added ---
df["date_added_parsed"] = pd.to_datetime(df["date_added"].str.strip(), format="%B %d, %Y", errors="coerce")
df["year_added"] = df["date_added_parsed"].dt.year
df["month_added"] = df["date_added_parsed"].dt.month
df["date_unknown"] = df["date_added_parsed"].isna().astype(int)

# --- Parse duration ---
def parse_duration(row):
    if pd.isna(row["duration"]):
        return np.nan, np.nan
    d = row["duration"]
    if row["type"] == "Movie":
        try:
            return int(d.replace(" min", "")), np.nan
        except:
            return np.nan, np.nan
    else:
        try:
            return np.nan, int(d.split(" ")[0])
        except:
            return np.nan, np.nan

df[["duration_minutes", "duration_seasons"]] = df.apply(
    lambda r: pd.Series(parse_duration(r)), axis=1
)

# --- Acquisition lag ---
df["acquisition_lag"] = df["year_added"] - df["release_year"]

# Data error: release_year > year_added
df["lag_error_flag"] = (df["acquisition_lag"] < 0).astype(int)
print(f"Lag error rows (release > added): {df['lag_error_flag'].sum()}")

df.loc[df["lag_error_flag"] == 1, "acquisition_lag"] = np.nan

# --- Same-year acquisition proxy ---
df["same_year_acquisition"] = (df["acquisition_lag"] == 0).astype(int)

# --- Acquisition freshness bucket ---
def lag_bucket(lag):
    if pd.isna(lag): return "Unknown"
    if lag <= 1: return "Fresh (0-1yr)"
    if lag <= 5: return "Recent (2-5yr)"
    if lag <= 15: return "Library (6-15yr)"
    return "Archive (>15yr)"

df["lag_bucket"] = df["acquisition_lag"].apply(lag_bucket)

# --- Genre features ---
df["genre_list"] = df["listed_in"].str.split(", ")
df["genre_count"] = df["genre_list"].apply(len)
df["primary_genre"] = df["genre_list"].apply(lambda x: x[0])

def genre_entropy(genres):
    from collections import Counter
    import math
    c = Counter(genres)
    total = sum(c.values())
    return -sum((v/total) * math.log2(v/total) for v in c.values())

df["genre_entropy"] = df["genre_list"].apply(genre_entropy)

# --- Country features ---
df["is_multi_country"] = df["country"].str.contains(",", na=False).astype(int)
df["primary_country"] = df["country"].str.split(",").str[0].str.strip()

def country_bucket(c):
    if pd.isna(c): return "Unknown"
    buckets = {
        "United States": "US", "United Kingdom": "UK",
        "India": "India", "South Korea": "South Korea",
        "Japan": "Japan", "France": "France",
        "Canada": "Canada", "Spain": "Spain",
    }
    return buckets.get(c, "Other")

df["country_bucket"] = df["primary_country"].apply(country_bucket)

# --- Metadata completeness ---
df["director_null"] = df["director"].isna().astype(int)
df["cast_null"] = df["cast"].isna().astype(int)
df["country_null"] = df["country"].isna().astype(int)
df["metadata_completeness_score"] = (
    (1 - df["director_null"]) +
    (1 - df["cast_null"]) +
    (1 - df["country_null"])
) / 3

def completeness_tier(s):
    if s >= 1.0: return "Complete"
    if s >= 0.34: return "Partial"
    return "Sparse"

df["completeness_tier"] = df["metadata_completeness_score"].apply(completeness_tier)

# --- Rating tier ---
def rating_tier(r):
    if pd.isna(r): return "Unknown"
    kids = ["TV-Y", "TV-Y7", "TV-Y7-FV", "TV-G", "G"]
    teen = ["TV-14", "PG-13", "PG"]
    adult = ["TV-MA", "R", "NC-17", "NR", "UR"]
    if r in kids: return "Kids"
    if r in teen: return "Teen"
    if r in adult: return "Adult"
    return "Unknown"

df["rating_tier"] = df["rating"].apply(rating_tier)

# --- Duration outlier flags ---
df["duration_outlier"] = 0
movie_mask = df["type"] == "Movie"
df.loc[movie_mask & ((df["duration_minutes"] < 20) | (df["duration_minutes"] > 300)), "duration_outlier"] = 1

# --- Duplicate check ---
dupes = df.duplicated(subset=["title", "type"]).sum()
print(f"Duplicate title+type rows: {dupes}")

# --- Summary stats ---
print(f"\nClean dataset shape: {df.shape}")
print(f"Year added range: {df['year_added'].min()} - {df['year_added'].max()}")
print(f"\nType split:\n{df['type'].value_counts()}")
print(f"\nRating tier split:\n{df['rating_tier'].value_counts()}")
print(f"\nLag bucket split:\n{df['lag_bucket'].value_counts()}")
print(f"\nCompleteness tier:\n{df['completeness_tier'].value_counts()}")
print(f"\nCountry bucket:\n{df['country_bucket'].value_counts().head(10)}")
print(f"\nGenre count stats:\n{df['genre_count'].describe()}")
print(f"\nAcquisition lag stats:\n{df['acquisition_lag'].describe()}")

df.to_parquet(r"D:\Agent\ai-analyst\working\netflix\clean_df.parquet", index=False)
print("\nSaved: working/netflix/clean_df.parquet")
