from pathlib import Path
import argparse, csv, io, urllib.request

SERIES = {
    'SP500': 'https://fred.stlouisfed.org/graph/fredgraph.csv?id=SP500',
    'ACOILWTICO': 'https://fred.stlouisfed.org/graph/fredgraph.csv?id=ACOILWTICO',
    'CPIAUCSL': 'https://fred.stlouisfed.org/graph/fredgraph.csv?id=CPIAUCSL',
}

def download(url):
    with urllib.request.urlopen(url, timeout=30) as r:
        return r.read().decode('utf-8')

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--output-dir', default='data/downloaded', help='Destination directory')
    args=ap.parse_args()
    out=Path(args.output_dir); out.mkdir(parents=True, exist_ok=True)
    for series,url in SERIES.items():
        text=download(url)
        (out/f'{series}.csv').write_text(text, encoding='utf-8')
        print(f'wrote {out/f"{series}.csv"}')

if __name__=='__main__': main()
