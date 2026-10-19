#!/usr/bin/env python3
"""Create a unique, initially unexecuted research run record using Python stdlib."""
import argparse
import datetime as dt
import json
from pathlib import Path
import re
import subprocess

ROOT=Path(__file__).resolve().parents[1]
RUNS=ROOT/'experiments'/'runs'

def get_commit():
    try:
        return subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,stderr=subprocess.DEVNULL,text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None

def make_run_id(stamp,slug,seed):
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',slug):
        raise ValueError('slug must use lowercase letters/numbers joined by hyphens')
    if seed<0: raise ValueError('seed must be nonnegative')
    return f'{stamp}-{slug}-s{seed}'

def main():
    ap=argparse.ArgumentParser(description='Create a metadata-only experiment run (no model execution).')
    ap.add_argument('--slug',required=True)
    ap.add_argument('--owner',required=True)
    ap.add_argument('--issue',type=int,required=True)
    ap.add_argument('--seed',type=int,required=True)
    args=ap.parse_args()
    if args.issue<=0: ap.error('issue must be a positive real GitHub Issue number')
    if not args.owner.strip(): ap.error('owner is required')
    stamp=dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    try: run_id=make_run_id(stamp,args.slug,args.seed)
    except ValueError as e: ap.error(str(e))
    directory=RUNS/run_id
    directory.mkdir(parents=True,exist_ok=False)
    manifest={
      'schema_version':1,'run_id':run_id,'created_at_utc':stamp,'status':'planned',
      'owner':args.owner.strip(),'issue':args.issue,'git_commit':get_commit(),
      'seed':args.seed,'question':None,'model':None,'hamiltonian':None,
      'parameter_split':{'train':None,'validation':None,'test':None},
      'command':None,'environment':None,
      'budget':{'gradient_steps':None,'hamiltonian_evaluations':None,'wall_seconds':None,'device':None},
      'oracle_access':{'training':None,'selection':None,'evaluation':None},
      'metrics':{},'artifacts':[],'notes':'Created by new_run.py. No experiment has been run.'
    }
    (directory/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(f'Created {directory.relative_to(ROOT)}')
    print('This creates metadata ONLY. Fill manifest and run your experiment separately.')

if __name__=='__main__': main()
