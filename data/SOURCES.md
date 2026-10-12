# Data sources

The committed CSV files are fixed snapshots used by the SBA 930 retrospective backtest.

- **S&P 500 (SP500)** — S&P Dow Jones Indices LLC via FRED: https://fred.stlouisfed.org/series/SP500
- **WTI crude oil (ACOILWTICO)** — U.S. Energy Information Administration via FRED: https://fred.stlouisfed.org/series/ACOILWTICO
- **Consumer Price Index (CPIAUCSL)** — U.S. Bureau of Labor Statistics via FRED: https://fred.stlouisfed.org/series/CPIAUCSL

## Backtest rule

Only observations through **2024-12-31** are included in model-facing inputs. The 2025 values are retained exclusively as holdout outcomes for evaluation.

`src/fetch_data.py` provides a reproducible route for refreshing public FRED data. The committed snapshots are used by default so results do not change if public series are revised later.
