# SBA 930 — LLM Financial Forecasting and Risk Analysis

This project was completed as part of the Per Scholas **AI Prompt Engineering Program for SBA 930: Evaluating LLMs for Financial Forecasting and Risk Analysis**. The project evaluates the use of large language models for financial forecasting, economic trend analysis, risk identification, and prompt optimization using historical financial and economic data.

## Models

- **Model A:** Claude Opus 5
- **Model B:** Gemini 3.8 Flash

Both models are evaluated against the same historical cutoff, forecast targets, and scoring framework.

## Experimental design

The project uses a retrospective forecasting backtest:

1. Public S&P 500, WTI crude oil, and CPI observations are stored in `data/raw/`.
2. `src/preprocess.py` merges the series and calculates annual returns/changes and December-to-December inflation.
3. `src/create_holdout.py` places **2020-2024** in model-facing inputs and isolates **2025** as the holdout outcome.
4. Identical evaluation prompts are version-controlled under `prompts/`.
5. Structured forecasts from Claude Opus 5 and Gemini 3.8 Flash are stored under `outputs/`.
6. `src/forecast_metrics.py` calculates numerical error against the 2025 holdout.
7. `src/risk_analysis.py` creates supporting risk metrics and a risk register.
8. `src/prompt_optimization.py` compares baseline prompts with the optimized prompt controls.

## Headline forecast errors

| Forecast target | Claude Opus 5 | Gemini 3.8 Flash |
|---|---:|---:|
| S&P 500 year-end 2025 | **4.3%** | **10.9%** |
| WTI 2025 annual average | **10.1%** | **25.4%** |
| 2025 Dec-to-Dec inflation | **0.15 pp** | **0.55 pp** |

These values are regenerated from the committed holdout and structured model forecasts rather than typed into the final results file. The notebook, validation script, and tests all load the Claude and Gemini forecast artifacts directly from `outputs/`; model forecast values are not embedded in calculation code.

## Quick reproduction

Requires Python 3.10+; the core validation uses only the Python standard library.

```bash
python src/validate_project.py
python -m unittest discover -s tests -v
```

Expected final line:

```text
VALIDATION PASSED: holdout isolation, calculations, risk metrics, and prompt audit reproduced.
```

## Optional notebook

```bash
pip install -r requirements.txt
jupyter notebook notebooks/SBA930_analysis.ipynb
```

## Optional refresh from FRED

The repository commits data snapshots so grading remains deterministic. To download current copies of the public FRED series separately:

```bash
python src/fetch_data.py --output-dir data/downloaded
```

See `data/SOURCES.md` for source URLs.

## Local model execution

`src/run_models.py` is a runner-agnostic helper for preserving local executions. It accepts any local CLI command that reads a prompt from standard input and writes the response to standard output. This keeps machine-specific runner configuration and credentials out of source control.

Example pattern:

```bash
python src/run_models.py   --model-name "<local model>"   --command "<your local model command>"   --prompt-file prompts/evaluation_prompts.md   --output-dir outputs/local_run/raw
```

## Repository map

```text
data/raw/               fixed public-source snapshots
data/processed/         merged/derived dataset
data/holdout/           2020-2024 model input + isolated 2025 actuals
prompts/                baseline and exact evaluation prompts
outputs/                structured model forecast artifacts
results/                errors, risk metrics, scoring, optimization audit
src/                    preprocessing, holdout, metrics, risk, execution, validation
notebooks/              reproducible analysis notebook
tests/                  calculation tests
```

## Reproducibility and auditability

The project preserves the historical cutoff, exact prompt text, model names, structured model forecasts, actual 2025 outcomes, deterministic scoring calculations, risk evidence, and optimization controls. No secret keys or credentials are committed.
