#!/usr/bin/env python3
"""Calculate forecast errors for Claude Opus 5 and Gemini 3.8 Flash."""
from common import ROOT, read_csv, write_csv
import json

def ape(forecast, actual):
    return abs(forecast-actual)/abs(actual)*100.0

def main():
    actual_row=read_csv(ROOT/'data/holdout/actuals_2025.csv')[0]
    actuals={
        'S&P 500 year-end 2025': float(actual_row['SP500 Year-end Close']),
        'WTI 2025 annual average': float(actual_row['WTI Annual Average ($/bbl)']),
        '2025 Dec-to-Dec inflation': float(actual_row['Dec-to-Dec Inflation (%)']),
    }
    with open(ROOT/'outputs/claude_opus_5/forecast_summary.json', encoding='utf-8') as f: a=json.load(f)
    with open(ROOT/'outputs/gemini_3_8_flash/forecast_summary.json', encoding='utf-8') as f: b=json.load(f)
    specs=[
      ('S&P 500 year-end 2025','sp500_2025_year_end','Index','pct'),
      ('WTI 2025 annual average','wti_2025_annual_average','$ per barrel','pct'),
      ('2025 Dec-to-Dec inflation','inflation_2025_dec_to_dec_pct','Percent','pp'),
    ]
    rows=[]
    for target,key,unit,metric in specs:
        actual=actuals[target]
        fa=float(a['forecasts'][key]['point_estimate']); fb=float(b['forecasts'][key]['point_estimate'])
        ea=ape(fa,actual) if metric=='pct' else abs(fa-actual)
        eb=ape(fb,actual) if metric=='pct' else abs(fb-actual)
        rows.append({
          'Target':target,'Actual':f'{actual:.6f}','Claude Opus 5 Forecast':fa,'Gemini 3.8 Flash Forecast':fb,
          'Unit':unit,'Error Metric':'Absolute percentage error (%)' if metric=='pct' else 'Absolute error (percentage points)',
          'Claude Opus 5 Error':f'{ea:.12f}','Gemini 3.8 Flash Error':f'{eb:.12f}'
        })
    fields=list(rows[0].keys())
    write_csv(ROOT/'results/forecast_errors.csv', fields, rows)
    print('wrote results/forecast_errors.csv')
    for r in rows:
        print(f"{r['Target']}: Claude={float(r['Claude Opus 5 Error']):.2f}; Gemini={float(r['Gemini 3.8 Flash Error']):.2f}")

if __name__=='__main__': main()
