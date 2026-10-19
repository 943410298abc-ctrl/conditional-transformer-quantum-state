"""Check saved scientific evidence independently of report prose (stdlib only)."""
import hashlib
import json
from pathlib import Path
import subprocess

ROOT=Path(__file__).resolve().parents[1]


def main():
    index=json.loads((ROOT/'experiments/round1_index.json').read_text())
    cfg=json.loads((ROOT/'experiments/configs/round1.json').read_text())
    expected={(a,m,s) for a in cfg['architectures'] for m in cfg['training_modes'] for s in cfg['seeds']}
    seen=set();count=0
    for rid in index['training_runs']:
        directory=ROOT/'experiments/runs'/rid
        m=json.loads((directory/'manifest.json').read_text())
        local_cfg=json.loads((directory/'config.json').read_text())
        assert local_cfg==cfg
        assert m['config_sha256']==hashlib.sha256(json.dumps(cfg,sort_keys=True).encode()).hexdigest()
        key=(m['model']['architecture'],m['model']['training_mode'],m['seed'])
        assert key not in seen and key in expected
        seen.add(key)
        assert m['status']=='completed' and m['oracle_access']['training'] is False and m['oracle_access']['selection'] is False
        assert m['budget']['gradient_steps']==cfg['steps']
        subprocess.run(['git','cat-file','-e',m['git_commit']+'^{commit}'],cwd=ROOT,check=True)
        rows=json.loads((directory/'metrics.json').read_text())
        assert len(rows)==75
        for row in rows:
            assert row['norm_error']<1e-10
            assert -1e-10 <= row['fidelity'] <= 1+1e-10
            assert row['energy_error']>=-1e-10 and row['variance']>=0
            assert row['h'] in cfg[row['split']]
        for h in cfg['train']+cfg['validation']+cfg['interpolation']+cfg['extrapolation']:
            at={r['method']:r for r in rows if r['h']==h}
            assert at['parity_ritz']['energy']<=at['direct']['energy']+1e-10
            assert at['train_span_ritz']['energy']<=at['lookup']['energy']+1e-10
        count+=len(rows)
    assert seen==expected
    replay=json.loads((ROOT/'docs/results/round1/replay_check.json').read_text())
    for file in ('metrics.json','training.json'):
        a=json.loads((ROOT/'experiments/runs'/replay['original']/file).read_text())
        b=json.loads((ROOT/'experiments/runs'/replay['replay']/file).read_text())
        assert a==b
    print(f'PASS: {len(seen)} prespecified jobs, {count} metric rows, physical inequalities, exact replay')


if __name__=='__main__':
    main()
