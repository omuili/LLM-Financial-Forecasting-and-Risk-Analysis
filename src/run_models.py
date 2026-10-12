#!/usr/bin/env python3
"""Generic local-model execution helper.

This script is intentionally independent of any specific proprietary/local runner.
Provide the command that launches the local model CLI. Each prompt is sent via stdin;
stdout and stderr are saved verbatim for auditability.

Example:
  python src/run_models.py --model-name "My Local Model" \
      --command "my_model_cli --temperature 0" \
      --prompt-file prompts/evaluation_prompts.md \
      --output-dir outputs/my_model/raw
"""
from pathlib import Path
import argparse, subprocess, re, json, datetime

def split_prompts(text):
    parts=[]
    current=None; buf=[]
    for line in text.splitlines():
        if line.startswith('## '):
            if current is not None:
                parts.append((current,''.join(buf).strip()))
            current=line[3:].strip(); buf=[]
        elif current is not None:
            buf.append(line)
    if current is not None: parts.append((current,''.join(buf).strip()))
    return [(n,p) for n,p in parts if p]

def slug(s): return re.sub(r'[^a-z0-9]+','_',s.lower()).strip('_')

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--model-name', required=True)
    ap.add_argument('--command', required=True, help='Local CLI command; prompt is sent on stdin')
    ap.add_argument('--prompt-file', default='prompts/evaluation_prompts.md')
    ap.add_argument('--output-dir', required=True)
    args=ap.parse_args()
    text=Path(args.prompt_file).read_text(encoding='utf-8')
    prompts=split_prompts(text)
    out=Path(args.output_dir); out.mkdir(parents=True, exist_ok=True)
    manifest={'model_name':args.model_name,'command':args.command,'executed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'runs':[]}
    for name,prompt in prompts:
        proc=subprocess.run(args.command, input=prompt, text=True, shell=True, capture_output=True)
        base=out/slug(name)
        (base.with_suffix('.prompt.txt')).write_text(prompt+'',encoding='utf-8')
        (base.with_suffix('.stdout.txt')).write_text(proc.stdout,encoding='utf-8')
        (base.with_suffix('.stderr.txt')).write_text(proc.stderr,encoding='utf-8')
        manifest['runs'].append({'task':name,'returncode':proc.returncode,'prompt_file':str(base.with_suffix('.prompt.txt')),'stdout_file':str(base.with_suffix('.stdout.txt'))})
        if proc.returncode != 0:
            raise SystemExit(f'{name} failed with return code {proc.returncode}')
    (out/'execution_manifest.json').write_text(json.dumps(manifest,indent=2)+'',encoding='utf-8')
    print(f'wrote {len(prompts)} local model outputs to {out}')

if __name__=='__main__': main()
