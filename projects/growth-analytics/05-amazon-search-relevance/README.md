# Amazon product search relevance

This project reranks Amazon's preselected candidate products for a shopping query. It compares title-token coverage with a lexical score that combines title, bullet points, description, brand, and color. It is a search reranking study; it does not retrieve from Amazon's full catalog.

## Reproduce

The raw files are kept out of Git under `analysis_data/`. The official dataset is published by Amazon Science under Apache-2.0.

```powershell
$env:GIT_LFS_SKIP_SMUDGE = "1"
git clone --depth 1 https://github.com/amazon-science/esci-data.git analysis_data/raw/amazon-esci-reference
Remove-Item Env:GIT_LFS_SKIP_SMUDGE
git -C analysis_data/raw/amazon-esci-reference lfs pull --include="shopping_queries_dataset/shopping_queries_dataset_examples.parquet"
curl.exe --fail --location --output analysis_data/raw/amazon-esci-products.parquet https://media.githubusercontent.com/media/amazon-science/esci-data/main/shopping_queries_dataset/shopping_queries_dataset_products.parquet
python projects/growth-analytics/05-amazon-search-relevance/src/analyze.py
```

The script checks both pinned file hashes before analysis. Required libraries are Polars, PyArrow, NumPy, and Matplotlib.

## Evaluation design

The study uses `small_version=1`, `product_locale=us`, and the dataset's query-disjoint train/test split. Product metadata is joined by both locale and product ID. Query token IDF is estimated on 80% of the training queries; field weights are selected on a separate 20% training-query tuning split. Test labels are used only for the final reported scores.

Amazon's TREC scorer gain map is Exact=1, Complement=0.1, Substitute=0.01, Irrelevant=0. The project reports query-macro full nDCG with that gain map. It also reports nDCG@10 as a custom top-10 view.

## Interpretation boundary

The candidate products were already selected for each query and manually judged. Results measure how well text fields rerank those candidates. They do not measure full-catalog retrieval, impressions, clicks, purchases, or the effect on shopping behavior.
