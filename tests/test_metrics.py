import csv
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'src'))
from forecast_metrics import ape


def read_csv(path):
    with open(path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def read_json(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


class ForecastMetricTests(unittest.TestCase):
    def test_ape_math(self):
        self.assertAlmostEqual(ape(90.0, 100.0), 10.0)
        self.assertAlmostEqual(ape(110.0, 100.0), 10.0)

    def test_holdout_isolation(self):
        train = read_csv(ROOT/'data/holdout/model_inputs_through_2024.csv')
        holdout = read_csv(ROOT/'data/holdout/actuals_2025.csv')
        self.assertTrue(all(int(row['Year']) <= 2024 for row in train))
        self.assertEqual(len(holdout), 1)
        self.assertEqual(holdout[0]['Year'], '2025')

    def test_results_match_saved_model_artifacts(self):
        holdout = read_csv(ROOT/'data/holdout/actuals_2025.csv')[0]
        claude = read_json(ROOT/'outputs/claude_opus_5/forecast_summary.json')
        gemini = read_json(ROOT/'outputs/gemini_3_8_flash/forecast_summary.json')
        results = {row['Target']: row for row in read_csv(ROOT/'results/forecast_errors.csv')}

        specs = {
            'S&P 500 year-end 2025': ('sp500_2025_year_end', float(holdout['SP500 Year-end Close']), 'pct'),
            'WTI 2025 annual average': ('wti_2025_annual_average', float(holdout['WTI Annual Average ($/bbl)']), 'pct'),
            '2025 Dec-to-Dec inflation': ('inflation_2025_dec_to_dec_pct', float(holdout['Dec-to-Dec Inflation (%)']), 'pp'),
        }

        for target, (key, actual, metric) in specs.items():
            row = results[target]
            for model, artifact, forecast_col, error_col in [
                ('Claude', claude, 'Claude Opus 5 Forecast', 'Claude Opus 5 Error'),
                ('Gemini', gemini, 'Gemini 3.8 Flash Forecast', 'Gemini 3.8 Flash Error'),
            ]:
                forecast = float(artifact['forecasts'][key]['point_estimate'])
                expected_error = ape(forecast, actual) if metric == 'pct' else abs(forecast - actual)
                self.assertAlmostEqual(float(row[forecast_col]), forecast, places=12, msg=model)
                self.assertAlmostEqual(float(row[error_col]), expected_error, places=9, msg=model)


if __name__ == '__main__':
    unittest.main()
