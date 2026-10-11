# Fake Job Detection analysis

The v2 case study uses the 17,880-row Employment Scam Aegean Dataset (EMSCAD), with 866 fraudulent posts. The dataset is publicly available from [Kaggle](https://www.kaggle.com/datasets/shivamb/real-or-fake-fake-jobposting-prediction). Download `fake_job_postings.csv` to `analysis_data/raw/fake_job_postings.csv`; raw data is excluded from Git.

The checked local snapshot has SHA-256 `59253295129d8b6a27607f9904f7d4ddf4dbb0ee35e079c7eb51b58b5e62bf60` and MD5 `10d9f3cf4faa78f8ce0932c5ec333c39`.

Run from the repository root with an environment that has pandas, numpy, scikit-learn, LightGBM, SHAP, PyTorch, and sentence-transformers installed:

```bash
python legacy_jekyll/scripts/fake-job-detection/fake_job_ml_v2.py
```

The script verifies the source checksum and key held-out and cross-validation metrics, then regenerates the four Fake Job charts used by the case study. Sentence embeddings use `all-MiniLM-L6-v2`. The model evaluation is a random stratified split of historical data, not a time-based or production test.
