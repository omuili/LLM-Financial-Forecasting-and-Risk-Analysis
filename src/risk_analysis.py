#!/usr/bin/env python3
"""Calculate supporting volatility statistics and write the risk register."""
from common import ROOT, read_csv, write_csv
import statistics, math

def main():
    rows=read_csv(ROOT/'data/processed/financial_dataset.csv')
    sp_returns=[float(r['SP500 Return (%)']) for r in rows if r['SP500 Return (%)']]
    wti_changes=[float(r['WTI Change (%)']) for r in rows if r['WTI Change (%)']]
    inflation=[float(r['Dec-to-Dec Inflation (%)']) for r in rows if int(r['Year'])>=2023]
    first=float(rows[0]['SP500 Year-end Close']); last=float(rows[-1]['SP500 Year-end Close'])
    cagr=((last/first)**(1/5)-1)*100
    metrics=[
      {'Metric':'S&P 500 2020-2025 CAGR (%)','Value':f'{cagr:.6f}'},
      {'Metric':'S&P annual return sample stdev, 2021-2025 (pp)','Value':f'{statistics.stdev(sp_returns):.6f}'},
      {'Metric':'WTI annual change sample stdev, 2021-2025 (pp)','Value':f'{statistics.stdev(wti_changes):.6f}'},
      {'Metric':'Average inflation, 2023-2025 (%)','Value':f'{statistics.mean(inflation):.6f}'},
    ]
    write_csv(ROOT/'results/risk_metrics.csv',['Metric','Value'],metrics)
    risks=[
      {'Risk':'Market volatility','Evidence':'S&P annual returns range from -19.4% (2022) to +26.9% (2021).','Assessment':'High variability; directional forecasts can fail quickly when macro conditions change.','Mitigation':'Diversification; scenario analysis; drawdown limits; periodic re-estimation; human review.'},
      {'Risk':'Commodity-price risk','Evidence':'WTI rose 74.0% in 2021 and 39.3% in 2022, then fell 18.3% in 2023 and 14.7% in 2025.','Assessment':'Very high sensitivity to exogenous supply/demand shocks.','Mitigation':'Hedging where appropriate; stress tests; exposure limits; scenario ranges rather than only point forecasts.'},
      {'Risk':'Inflation / rate risk','Evidence':'Dec-to-Dec inflation moved from 7.17% in 2021 to 2.65% in 2025.','Assessment':'Regime changes affect discount rates, credit conditions, and valuations.','Mitigation':'Monitor inflation, rates, and policy updates; use multiple macro scenarios.'},
      {'Risk':'Credit risk','Evidence':'Not directly measured by the selected stock, oil, and CPI datasets.','Assessment':'Cannot be quantified from these datasets alone.','Mitigation':'Add credit spreads, defaults, leverage, coverage ratios, and borrower-level data.'},
      {'Risk':'Liquidity risk','Evidence':'Not directly measured by annual price series.','Assessment':'Annual observations can hide market-depth or funding stress.','Mitigation':'Add bid-ask spreads, turnover, volume, funding data, and liquidity buffers.'},
    ]
    write_csv(ROOT/'results/risk_register.csv',list(risks[0].keys()),risks)
    print('wrote risk metrics and risk register')

if __name__=='__main__': main()
