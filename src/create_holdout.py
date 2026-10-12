#!/usr/bin/env python3
"""Create model-facing data (through 2024) and a separate 2025 holdout file."""
from common import ROOT, read_csv, write_csv

def main():
    rows=read_csv(ROOT/'data/processed/financial_dataset.csv')
    train=[r for r in rows if int(r['Year']) <= 2024]
    hold=[r for r in rows if int(r['Year']) == 2025]
    if len(hold) != 1:
        raise RuntimeError('Expected exactly one 2025 holdout row')
    fields=list(rows[0].keys())
    write_csv(ROOT/'data/holdout/model_inputs_through_2024.csv', fields, train)
    write_csv(ROOT/'data/holdout/actuals_2025.csv', fields, hold)
    print('wrote model inputs through 2024 and isolated 2025 actuals')

if __name__=='__main__': main()
