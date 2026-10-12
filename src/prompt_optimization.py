#!/usr/bin/env python3
"""Deterministic prompt-control audit for baseline vs optimized prompts.

This does not pretend that prompt quality alone proves forecast accuracy. It verifies
that the optimized prompts implement the six controls described in the SBA report.
"""
from common import ROOT, write_csv
import re

BASELINE={
 'S&P 500':'Forecast the potential impact of recent economic policies on the stock market.',
 'WTI':'Analyze historical financial data to predict future trends in commodity prices.',
 'Inflation':"Forecast the next year's inflation rate.",
}
OPTIMIZED={
 'S&P 500':'Using only the supplied S&P 500 year-end data for 2020-2024 and the stated 2024 monetary-policy easing context, forecast the S&P 500 year-end level for 2025. Provide a point estimate, plausible range, expected direction, three major drivers, three major risks, and confidence. Do not use any data after 2024 and do not invent missing values.',
 'WTI':'Using only WTI annual average prices for 2020-2024 ($39.16, $68.13, $94.90, $77.58, $76.63), forecast the 2025 annual average. Provide a point estimate, plausible range, major supply/demand drivers, major risks, and confidence. Do not use post-2024 data.',
 'Inflation':'Using only the December CPI index values from 2019 through 2024 (258.630, 262.045, 280.845, 298.832, 308.741, 317.604), calculate the historical December-to-December inflation rates and forecast the 2025 December-to-December inflation rate. Provide a point estimate, plausible range, and concise rationale. Do not use post-2024 information.',
}

def audit(p):
    low=p.lower(); nums=re.findall(r'\d+(?:\.\d+)?',p)
    return {
      'Historical cutoff': int(('2024' in p) and ('do not use' in low)),
      'Grounded data values': int(len(nums)>=4),
      'Defined 2025 target': int('2025' in p),
      'Uncertainty range': int('range' in low),
      'Drivers/risks/confidence': int(('driver' in low or 'rationale' in low) and ('risk' in low or 'rationale' in low) and ('confidence' in low or 'rationale' in low)),
      'Anti-leakage / no invention': int(('post-2024' in low) or ('after 2024' in low) or ('do not invent' in low)),
    }

def main():
    rows=[]
    for task in BASELINE:
      for version,prompt in [('Baseline',BASELINE[task]),('Optimized',OPTIMIZED[task])]:
        a=audit(prompt); score=sum(a.values())
        row={'Task':task,'Prompt version':version,'Control score (0-6)':score,**a}
        rows.append(row)
    write_csv(ROOT/'results/prompt_optimization_audit.csv',list(rows[0].keys()),rows)
    print('wrote results/prompt_optimization_audit.csv')
    for r in rows: print(r['Task'],r['Prompt version'],r['Control score (0-6)'])

if __name__=='__main__': main()
