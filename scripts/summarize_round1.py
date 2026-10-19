"""Rebuild figures/tables from one explicitly selected, unique set of run manifests."""
import argparse
import csv
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--index',default='experiments/round1_index.json')
    args=parser.parse_args()
    index=json.loads((ROOT/args.index).read_text())
    output=ROOT/'docs'/'results'/'round1'
    output.mkdir(parents=True,exist_ok=True)
    rows, manifests = [], []
    seen=set()
    for run_id in index['training_runs']:
        path=ROOT/'experiments'/'runs'/run_id
        m=json.loads((path/'manifest.json').read_text())
        key=(m['model']['architecture'],m['model']['training_mode'],m['seed'])
        if key in seen or m['status']!='completed':
            raise ValueError('duplicate seed/model or incomplete selected run')
        seen.add(key)
        manifests.append(m)
        rows.extend(json.loads((path/'metrics.json').read_text()))
    with (output/'all_metrics.csv').open('w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    aggregates=[]
    for arch in ['mlp','transformer']:
        for mode in ['raw','even']:
            for split in ['train','interpolation','extrapolation']:
                for method in ['direct','lookup','even_projection','parity_ritz','train_span_ritz']:
                    seeds=sorted({r['seed'] for r in rows if r['architecture']==arch and r['training_mode']==mode})
                    samples=[]
                    for seed in seeds:
                        rr=[r for r in rows if (r['architecture'],r['training_mode'],r['split'],r['method'],r['seed'])==(arch,mode,split,method,seed)]
                        samples.append([np.mean([1-r['fidelity'] for r in rr]),max(1-r['fidelity'] for r in rr),
                                        np.mean([r['energy_error_per_spin'] for r in rr]),max(r['correlation_error'] for r in rr)])
                    a=np.asarray(samples)
                    row=dict(architecture=arch,training_mode=mode,split=split,method=method,seeds=seeds)
                    for j,metric in enumerate(['mean_infidelity','worst_infidelity','mean_energy_error_per_spin','worst_correlation_error']):
                        row[metric]=float(a[:,j].mean());row[metric+'_seed_sd']=float(a[:,j].std(ddof=1))
                    aggregates.append(row)
    (output/'summary.json').write_text(json.dumps(aggregates,indent=2)+'\n')
    lines=['# Round 1 aggregate results','', 'Mean +/- sample SD across **three seeds**; not confidence intervals. Within-seed means/maxima use the fixed parameter grid.','',
           '| Architecture | Train mode | Split | Predictor | Mean infidelity | Worst infidelity |',
           '|---|---|---|---|---:|---:|']
    for r in aggregates:
        lines.append(f"| {r['architecture']} | {r['training_mode']} | {r['split']} | {r['method']} | {r['mean_infidelity']:.6g} +/- {r['mean_infidelity_seed_sd']:.3g} | {r['worst_infidelity']:.6g} +/- {r['worst_infidelity_seed_sd']:.3g} |")
    lines+=['','## Actual budgets','', '| Model | Mode | Seed | Selected step | Full steps | Training seconds | Total seconds |','|---|---|---:|---:|---:|---:|---:|']
    for m in manifests:
        lines.append(f"| {m['model']['architecture']} | {m['model']['training_mode']} | {m['seed']} | {m['model']['selected_step']} | {m['budget']['gradient_steps']} | {m['budget']['training_seconds']:.2f} | {m['budget']['wall_seconds']:.2f} |")
    (output/'tables.md').write_text('\n'.join(lines)+'\n')
    colors={'direct':'#175d8c','lookup':'#bc5b32','even_projection':'#2a9069','train_span_ritz':'#8456a1'}
    for arch in ['mlp','transformer']:
        fig, axes=plt.subplots(2,3,figsize=(13,7),layout='constrained')
        for i,mode in enumerate(['raw','even']):
            for j,(metric,label) in enumerate([('fidelity','Ground-state fidelity'),('energy_error_per_spin','Energy error / spin [J]'),('correlation_error','Endpoint connected-correlation error')]):
                ax=axes[i,j]
                for method,color in colors.items():
                    rr=[r for r in rows if r['architecture']==arch and r['training_mode']==mode and r['method']==method and r['split']!='validation']
                    hs=sorted({r['h'] for r in rr})
                    groups=[[r[metric] for r in rr if r['h']==h] for h in hs]
                    mean=np.array([np.mean(g) for g in groups]);sd=np.array([np.std(g,ddof=1) for g in groups])
                    ax.plot(hs,mean,'.-',color=color,label=method)
                    ax.fill_between(hs,mean-sd,mean+sd,color=color,alpha=.13)
                for h in [.2,.8,1.4]: ax.axvline(h,color='gray',ls=':',lw=.8)
                ax.set(xlabel='Transverse field h / J',ylabel=label,title=f'{arch}, {mode} training')
                if metric!='fidelity':ax.set_yscale('symlog',linthresh=1e-5)
                ax.grid(alpha=.2)
        axes[0,0].legend(fontsize=8)
        fig.suptitle('N=6 open TFIM; 600 updates; mean +/- seed SD (n=3); dotted lines = train h')
        fig.savefig(output/f'{arch}_generalization.png',dpi=160);plt.close(fig)
    # Frozen split diagram; no metric-dependent point selection.
    cfg=json.loads((ROOT/'experiments/configs/round1.json').read_text())
    fig,ax=plt.subplots(figsize=(10,2.6),layout='constrained')
    for y,key in enumerate(['extrapolation','interpolation','validation','train']):
        ax.scatter(cfg[key],[y]*len(cfg[key]),label=key,s=45)
    ax.set(yticks=range(4),yticklabels=['extrapolation','interpolation','validation','train'],xlabel='h / J',title='Frozen parameter split, N=6, lambda=0')
    ax.axvspan(.2,1.4,color='gray',alpha=.08)
    fig.savefig(output/'parameter_split.png',dpi=160);plt.close(fig)
    print(f'Wrote {len(rows)} rows, {len(aggregates)} aggregates from {len(manifests)} selected runs')


if __name__=='__main__':
    main()
