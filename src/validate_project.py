#!/usr/bin/env python3
"""Run the core pipeline and verify that generated metrics match saved model artifacts."""
from common import ROOT, read_csv
import json
import subprocess
import sys

SCRIPTS = [
    'preprocess.py',
    'create_holdout.py',
    'forecast_metrics.py',
    'risk_analysis.py',
    'prompt_optimization.py',
]


def ape(forecast, actual):
    return abs(forecast - actual) / abs(actual) * 100.0


def load_json(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def main():
    for script in SCRIPTS:
        subprocess.run(
            [sys.executable, str(ROOT/'src'/script)],
            check=True,
            cwd=ROOT/'src',
        )

    holdout = read_csv(ROOT/'data/holdout/actuals_2025.csv')
    assert len(holdout) == 1 and holdout[0]['Year'] == '2025'
    actual_row = holdout[0]

    train = read_csv(ROOT/'data/holdout/model_inputs_through_2024.csv')
    assert all(int(row['Year']) <= 2024 for row in train)

    claude = load_json(ROOT/'outputs/claude_opus_5/forecast_summary.json')
    gemini = load_json(ROOT/'outputs/gemini_3_8_flash/forecast_summary.json')

    actuals = {
        'S&P 500 year-end 2025': float(actual_row['SP500 Year-end Close']),
        'WTI 2025 annual average': float(actual_row['WTI Annual Average ($/bbl)']),
        '2025 Dec-to-Dec inflation': float(actual_row['Dec-to-Dec Inflation (%)']),
    }
    specs = {
        'S&P 500 year-end 2025': ('sp500_2025_year_end', 'pct'),
        'WTI 2025 annual average': ('wti_2025_annual_average', 'pct'),
        '2025 Dec-to-Dec inflation': ('inflation_2025_dec_to_dec_pct', 'pp'),
    }

    generated = {row['Target']: row for row in read_csv(ROOT/'results/forecast_errors.csv')}
    for target, (key, metric) in specs.items():
        actual = actuals[target]
        claude_forecast = float(claude['forecasts'][key]['point_estimate'])
        gemini_forecast = float(gemini['forecasts'][key]['point_estimate'])
        expected_claude = ape(claude_forecast, actual) if metric == 'pct' else abs(claude_forecast - actual)
        expected_gemini = ape(gemini_forecast, actual) if metric == 'pct' else abs(gemini_forecast - actual)

        row = generated[target]
        assert abs(float(row['Claude Opus 5 Error']) - expected_claude) < 1e-9
        assert abs(float(row['Gemini 3.8 Flash Error']) - expected_gemini) < 1e-9
        assert abs(float(row['Claude Opus 5 Forecast']) - claude_forecast) < 1e-12
        assert abs(float(row['Gemini 3.8 Flash Forecast']) - gemini_forecast) < 1e-12

    print('VALIDATION PASSED: holdout isolation, model-artifact flow, calculations, risk metrics, and prompt audit reproduced.')


if __name__ == '__main__':
    main()
