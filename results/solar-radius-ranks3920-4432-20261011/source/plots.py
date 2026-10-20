"""Diagnostic figures for campaign peaks; all panels show measured photometry."""
import json
from pathlib import Path
import numpy as np
from .campaign import load_training


def plot_discovery(discovery, output, peak_index=0, loader=load_training):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    row=json.loads(discovery.read_text())
    p=row['screened_peaks'][peak_index]
    b=p['best']
    t,y,dy,_=loader(row['target'],Path('data'))
    phase=(t-b['transit_time']+b['period']/2)%b['period']-b['period']/2
    fig,axes=plt.subplots(3,1,figsize=(11,9),constrained_layout=True)
    axes[0].plot(t,(y-1)*1e6,'.',ms=2)
    axes[0].set(xlabel='BTJD',ylabel='Flux residual (ppm)')
    for ax,lim in zip(axes[1:],[b['period']/2,min(b['period']/2,3*b['duration'])]):
        ax.plot(phase*24,(y-1)*1e6,'.',ms=2,alpha=.3)
        edges=np.linspace(-lim,lim,61)
        centers=[];means=[]
        for l,r in zip(edges[:-1],edges[1:]):
            m=(phase>=l)&(phase<r)
            if m.any():
                centers.append((l+r)/2*24)
                means.append(np.average(y[m]-1,weights=1/dy[m]**2)*1e6)
        ax.plot(centers,means,'o-',color='black',ms=3)
        ax.set(xlabel='Hours from fitted event',ylabel='Flux residual (ppm)',xlim=(-lim*24,lim*24))
    fig.suptitle(f'TIC {row["tic"]}, P={b["period"]:.6f} d; exploratory signal\n'+', '.join(p['flags']))
    fig.savefig(output,dpi=120);plt.close(fig)
