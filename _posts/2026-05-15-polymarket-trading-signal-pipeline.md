---
title: "Building a Trading Signal Pipeline for Polymarket"
date: 2026-05-15
categories: machine learning
tags:
  - python
  - xgboost
  - optuna
  - mlops
  - trading
  - polymarket
excerpt: Four engineering decisions that separate a production-grade prediction pipeline from a backtest that only works in hindsight.
mathjax: false
---

Polymarket is a prediction market where you bet YES or NO on real-world outcomes. Every contract has a price between $0.01 and $0.99 that reflects the crowd's implied probability of YES resolving. The edge -- if any -- comes from finding contracts where that price is wrong.

The problem: there are dozens of active contracts at any given time, each requiring OHLCV pattern recognition, position sizing, and constant monitoring. That is not a manual workflow.

I built a pipeline to automate the signal generation step. It ingests 1-minute Binance OHLCV data for four tickers (BTC, ETH, SOL, XRP), engineers features, trains a calibrated XGBoost classifier per ticker, and outputs a probability estimate for each 1-hour bar. A bet is placed only when that estimate diverges from the market price by enough to cover the round-trip cost.

Here are the four engineering decisions that made the difference between a pipeline that looks good on training data and one that might actually work.

---

## Decision 1: Triple-Barrier Labeling Instead of Return Sign

The naive approach is to label each bar +1 if the next return is positive and 0 if it is negative. This sounds reasonable and is completely wrong.

Most bars have ambiguous outcomes. A +0.02% return 30 minutes later carries no real signal -- it is noise. Labeling it as a "correct long prediction" adds garbage to the training set.

Triple-barrier labeling only assigns a label when the outcome is clear: the price moved a full ATR multiple upward (label: 1) or downward (label: 0) before the time limit expired. Bars that hit the time limit without a definitive resolution are labeled NaN and excluded from training.

```python
def build_triple_barrier_target(
    df: pd.DataFrame,
    atr_mult: float,
    max_bars: int,
) -> pd.Series:
    """
    Labels: 1 = upper barrier hit first, 0 = lower barrier hit first.
    NaN = neither barrier hit within max_bars (excluded from training).
    """
```

The labeled dataset is smaller -- roughly 40-60% of bars get a clean label. But the signal-to-noise ratio is much better.

---

## Decision 2: Walk-Forward CV With Embargo, Not a Simple Split

An 80/20 train/test split on time-series data leaks future information. Features computed with rolling windows near the split boundary include bars from the test period. The model sees the future during training. The backtest looks great. Live trading does not.

Walk-forward cross-validation fixes this by testing on genuinely out-of-sample periods: train on 24 months, test on the next 3, slide forward, repeat. Adding `embargo_bars` between train end and test start removes the leakage zone at each boundary.

```python
def generate_walk_forward_splits(df, embargo_bars=0):
    curr = start + pd.DateOffset(months=TRAIN_MONTHS)
    while curr < end:
        test_start = curr + embargo_bars  # skip leakage zone
        yield (
            df.loc[:curr],
            df.loc[test_start : test_start + pd.DateOffset(months=TEST_MONTHS)],
        )
        curr += pd.DateOffset(months=TEST_MONTHS)
```

The cost is more computation. Each ticker runs multiple folds instead of one. The benefit is a test result you can actually trust.

---

## Decision 3: A Cost-Aware Objective Function

Standard Sharpe ratio ignores trading costs. A strategy that generates many small wins can have a strong Sharpe on paper and lose money in practice once fees are included.

Polymarket charges roughly 2% on winnings, about 100 basis points round-trip. The pipeline deducts this from every simulated trade's return before computing the Sharpe-like objective that Optuna optimizes.

A second guard: the pipeline skips any bar where the market already implies >50% probability for YES. At a $0.50 YES price, the breakeven win rate after costs is above 50%. The model would need to be more confident than the market already is, in the right direction, to generate edge. That bar is rarely cleared.

---

## Decision 4: Checkpoint-Based Resumability

Each Optuna study runs 60 trials. On CPU, a single ticker takes 20-30 minutes. Four tickers is 2+ hours. A crash halfway through without a checkpoint means restarting everything.

The pipeline writes a JSON checkpoint after each completed ticker. On restart, finished tickers are loaded from the checkpoint and skipped. Only incomplete work is re-run.

```python
checkpoint[name] = row
with open(checkpoint_path, "w") as f:
    json.dump(checkpoint, f, indent=2, default=str)
```

The JSON is human-readable. If a run fails mid-ticker, the checkpoint shows exactly what completed and what needs to be re-run. Useful for diagnosing whether the failure was a data issue or a code issue.

---

## What the Pipeline Produces

After a full run across all four tickers:

| Output | Location |
|--------|---------|
| Trained models | `models/1h/{TICKER}_1h_model.joblib` |
| Best hyperparameters | `source/best_models_summary_1h.csv` |
| Run state | `source/checkpoint_1h.json` |

Each model is a calibrated XGBoost classifier. Raw probabilities pass through Platt scaling so a 0.6 output actually means roughly 60% confidence, not just "higher than 0.5."

---

## Known Limitations

This pipeline has three significant gaps that would need to be addressed before treating any live results as reliable.

**No data versioning.** The `source/*.parquet` files are overwritten by the download scripts. There is no record of which data version trained which model. A model trained on corrupted or incomplete data would show no obvious failure -- it would just perform poorly in live use.

**No logging framework.** All status output is `print()`. Silent failures are possible in long runs. A proper logger with timestamps and error capture would make debugging much faster.

**Manual OOS evaluation.** The out-of-sample evaluation script (`eval_april2026.py`) is run manually after training. It is not triggered automatically. It is easy to forget, or to selectively run it only when you expect good results.

The 75 `cycle_*.py` files in the repo are a visible record of the research process. Each file is one iteration of trying to improve the labeling, features, or objective. They show what was attempted and abandoned. That trail is intentional.

---

**Methodology notes:**
- Source data: Binance 1-minute OHLCV klines via CCXT, stored as parquet per ticker.
- Timeframe: resampled to 1 hour. Zero-volume bars filtered before feature calculation.
- Walk-forward config: 24-month train, 3-month test, stepped by 3 months.
- HPO: Optuna 60 trials, TPE sampler transitioning to CMA-ES after initial exploration.
- Calibration: Platt scaling (sklearn CalibratedClassifierCV, sigmoid method).
- Cost model: 100 bps round-trip, max YES price $0.50.

**Code:** Available on request. The pipeline lives in a private repository.
