"""Oracle-only spectral mechanism check; not a training or acquisition method."""
import datetime as dt
import json
from pathlib import Path
import platform
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
import numpy as np
import scipy
from scipy.linalg import eigh
from ctqs.physics import hamiltonian, metrics


def main():
    stamp = dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    run_id = stamp + '-spectral-mechanism-s0'
    out = ROOT / 'experiments' / 'runs' / run_id
    out.mkdir(parents=True)
    start = time.monotonic()
    rows = []
    for n in (4,6,8):
        d = 1 << n
        q = np.zeros((d,d//2))
        for i in range(d//2):
            q[i,i] = q[d-1-i,i] = 1/np.sqrt(2)
        for h in (.2,.35,.8):
            matrix = hamiltonian(n,h)
            vals, vecs = eigh(matrix)
            plus_vals = eigh(q.T@matrix@q, eigvals_only=True)
            mixed = (vecs[:,0]+vecs[:,1])/np.sqrt(2)
            m = metrics(matrix,mixed,n,(vals,vecs))
            rows.append(dict(n=n,h=h,gap=float(vals[1]-vals[0]),
                even_gap=float(plus_vals[1]-plus_vals[0]),
                mixture_fidelity=m['fidelity'], mixture_energy_error=m['energy_error'],
                mixture_variance=m['variance'],
                energy_identity_error=abs(m['energy_error']-(vals[1]-vals[0])/2),
                variance_identity_error=abs(m['variance']-(vals[1]-vals[0])**2/4)))
    # Exact eigenstates all have zero residual. Residual alone cannot certify ground identity.
    counterexample = dict(H=[[0.,0.],[0.,1e-6]], state=[0.,1.],
                          energy_error=1e-6, variance=0., fidelity=0.)
    payload = dict(rows=rows, residual_counterexample=counterexample)
    (out/'spectral.json').write_text(json.dumps(payload,indent=2)+'\n')
    manifest = dict(schema_version=1,run_id=run_id,created_at_utc=stamp,status='completed',
        owner='Bian-M-X/Codex',issue=1,git_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        seed=0,question='How does restricting to known even parity change the energy-fidelity bound?',
        model='exact spectral mechanism; no neural model',hamiltonian='open TFIM, J=1, lambda=0, MSB-left',
        parameter_split=dict(train=None,validation=None,test='N=4/6/8; h=0.2/0.35/0.8; diagnostic sweep'),
        command='python scripts/check_spectral_mechanism.py',
        environment=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,platform=platform.platform()),
        budget=dict(gradient_steps=0,exact_diagonalizations=18,wall_seconds=time.monotonic()-start,device='cpu'),
        oracle_access=dict(training=False,selection=False,evaluation=True,counterexample_construction=True),
        metrics=dict(max_energy_identity_error=max(r['energy_identity_error'] for r in rows),
                     max_variance_identity_error=max(r['variance_identity_error'] for r in rows)),
        artifacts=['spectral.json'],notes='Derived standard spectral identities; explicitly oracle diagnostic. Not a new theorem or deployed certificate.')
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(run_id)
    for row in rows:
        print(row['n'],row['h'],row['gap'],row['even_gap'])


if __name__ == '__main__':
    main()
