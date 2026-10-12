#!/usr/bin/env python3
"""Merge the three source snapshots and calculate annual changes/inflation."""
from common import ROOT, read_csv, write_csv, pct_change

def main():
    sp={int(r['Year']): float(r['SP500_Year_End_Close']) for r in read_csv(ROOT/'data/raw/sp500_year_end.csv')}
    wt={int(r['Year']): float(r['WTI_Annual_Average_USD_per_bbl']) for r in read_csv(ROOT/'data/raw/wti_annual_average.csv')}
    cp={int(r['Year']): float(r['CPI_December_SA']) for r in read_csv(ROOT/'data/raw/cpi_december.csv')}
    rows=[]
    for y in range(2020, 2026):
        rows.append({
            'Year': y,
            'SP500 Year-end Close': f'{sp[y]:.2f}',
            'SP500 Return (%)': '' if y==2020 else f'{pct_change(sp[y],sp[y-1]):.12f}',
            'WTI Annual Average ($/bbl)': f'{wt[y]:.2f}',
            'WTI Change (%)': '' if y==2020 else f'{pct_change(wt[y],wt[y-1]):.12f}',
            'CPI December (SA)': f'{cp[y]:.3f}',
            'Dec-to-Dec Inflation (%)': f'{pct_change(cp[y],cp[y-1]):.12f}',
        })
    fields=list(rows[0].keys())
    write_csv(ROOT/'data/processed/financial_dataset.csv', fields, rows)
    print('wrote data/processed/financial_dataset.csv')

if __name__=='__main__': main()
