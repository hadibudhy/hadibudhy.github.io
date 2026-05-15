---
title: "Polymarket Trading Signal Pipeline"
date: 2026-05-15
categories: data-engineer
tags: [python, xgboost, optuna, mlops, trading, polymarket]
excerpt: "A pipeline that predicts binary market outcomes using triple-barrier labeling, walk-forward CV, and a Polymarket-specific cost model."
mathjax: false
---

## The Story

Polymarket is a prediction market where you bet YES or NO on real-world outcomes. The edge is knowing when the market's implied probability is wrong. The problem: watching dozens of contracts, reading OHLCV patterns, and sizing positions manually is not sustainable.

I built a pipeline to automate the signal generation step. It takes 1-minute Binance price data for four tickers: BTC, ETH, SOL, and XRP. The pipeline engineers 30+ features, trains a calibrated XGBoost model per ticker, and outputs a probability estimate for each bar. Bets are placed only when the model's estimate diverges from the market price by enough to cover the round-trip cost.

**Key decisions:**

- **Triple-barrier labeling, not raw return sign.** Most bars have ambiguous outcomes. Labeling every bar as "up or down" forces a signal onto noise. Triple-barrier labels only include bars where price moved a full ATR multiple in one direction before reversing. Bars that hit the time limit without a clear result are excluded. The labeled dataset is smaller but cleaner.
- **Walk-forward CV with embargo, not a simple train/test split.** Crypto features are autocorrelated. A naive 80/20 split leaks future information across the boundary. Walk-forward uses 24-month training windows with an embargo gap before each test fold. This ensures each test period is genuinely out-of-sample.
- **Polymarket-specific cost model.** Standard Sharpe ratio ignores fees. The objective function deducts 100 bps per round trip from every simulated trade before optimizing. The pipeline skips any contract where the market already prices YES above $0.50 — insufficient edge given the cost.
- **Checkpoint-based resumability.** Each Optuna study runs 60 trials — 20+ minutes per ticker. A crash without checkpoints means restarting everything. `checkpoint_1h.json` saves each completed ticker. Re-runs skip finished tickers and resume from where they stopped.

**Outcome:** Four trained models with calibrated probability outputs. Each ticker gets a Sharpe summary and its best hyperparameters saved to a shared CSV. The pipeline feeds a downstream live bot that checks these estimates before placing bets.

The 75 `cycle_*.py` files are a visible research trail. Each iteration tried a different approach to labeling, features, or the training objective. Keeping them is intentional. They document what didn't work as much as what did.

---

## How I Did It

**Tools and stack:** Python 3.12 · pandas 2.0 · XGBoost 2.0 · Optuna 3.6 · joblib · CCXT · scikit-learn (calibration) · numpy · scipy

**Data flow:**

```
[Source: source/*.parquet (Binance 1-min OHLCV, 4 tickers)]
→ [Resample to 1h]
→ [Feature engineering: ALMA, RSI, ADX, triple-barrier target, session labels, lagged returns]
→ [Walk-forward CV: 24m train / 3m test, embargo bars at boundaries]
→ [HPO: Optuna 60 trials, TPE then CMA-ES sampler, Sharpe-like objective minus 100 bps]
→ [Train: XGBoost + Platt scaling calibration]
→ [Output: models/1h/*.joblib + checkpoint_1h.json + best_models_summary_1h.csv]
```

**Schema:** Input parquet has standard OHLCV columns plus a `quote_volume` field. Zero-volume bars are filtered before feature calculation. The pipeline resamples 1-minute bars to 1-hour using standard OHLC aggregation rules.

**Data quality checks built in:**
- Zero-volume bar filter (silent data gaps from Binance rate limiting)
- Walk-forward fold minimum bar count (skip folds with insufficient labeled examples)
- Timeframe assertion at startup (`assert TIMEFRAME in _BARS_PER_DAY`) prevents misconfiguration from passing silently

**Known limitations:**
- No data versioning — `source/*.parquet` files are overwritten by the download scripts. There is no snapshot of which data version trained which model.
- No logging framework — all status output is `print()` statements. Silent failures are possible in long runs.
- OOS evaluation (`eval_april2026.py`) is run manually after training, not integrated into the pipeline trigger.

---

## Key Code

Triple-barrier labeling assigns 1 (long signal) only when the upper ATR barrier is hit before the lower barrier, within a maximum bar window. Bars where neither fires are excluded. This is the core of why the model is not just predicting return sign.

```python
def build_triple_barrier_target(
    df: pd.DataFrame,
    atr_mult: float,
    max_bars: int,
) -> pd.Series:
    """
    Triple-barrier labeling: returns Series of {0, 1} aligned to df.index.
    Bars where neither barrier is hit within max_bars are labeled NaN (filtered later).
    """
```

Walk-forward splits add `embargo_bars` between train end and test start. Without this gap, features computed at bar T using a rolling window can include information from test-period bars, creating look-ahead leakage.

```python
def generate_walk_forward_splits(
    df: pd.DataFrame,
    embargo_bars: int = 0,
) -> list[tuple]:
    curr = start + pd.DateOffset(months=TRAIN_MONTHS)
    while curr < end:
        # Advance test start by embargo_bars to prevent label leakage
        test_start = curr + embargo_bars
        yield (
            df.loc[:curr],
            df.loc[test_start : min(test_start + pd.DateOffset(months=TEST_MONTHS), end)],
        )
        curr += pd.DateOffset(months=TEST_MONTHS)
```

The checkpoint write happens after every completed ticker. The JSON is human-readable so a failed run can be inspected before deciding whether to resume or restart from scratch.

```python
checkpoint[name] = row
with open(checkpoint_path, "w") as f:
    json.dump(checkpoint, f, indent=2, default=str)
print(f"[{name}] Checkpoint saved -> {checkpoint_path}")
```

> Full pipeline code: `D:/Code/Projects/model_pipeline/pipeline.py`
