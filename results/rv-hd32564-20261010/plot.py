import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from exoplanet.rv_search import fit,design
p=Path(__file__).parent;d=np.load(p/'nightly.npz');t,y,e,g=[d[k] for k in ['time','rv','error','group']]
r=next(r for r in json.loads((p/'mode-comparison.json').read_text())['results'] if r['jitter']==2 and r['n_signals']==3 and r['periods'][0]>2)
f=fit(t,y,e,g,r['periods']);x=design(t,g,r['periods'],f['epoch']);fig,axs=plt.subplots(3,1,figsize=(9,9),constrained_layout=True)
for i,ax in enumerate(axs):
 k=x.shape[1]-6+2*i;component=x[:,k:k+2]@f['coefficients'][k:k+2];phase=((t-f['epoch'])/r['periods'][i])%1
 ax.errorbar(phase,y-f['model']+component,yerr=e,fmt='.',alpha=.5,ms=4)
 ph=np.linspace(0,1,400);c=f['coefficients'][k:k+2];ax.plot(ph,c[0]*np.sin(2*np.pi*ph)+c[1]*np.cos(2*np.pi*ph),'k-')
 ax.set(title=f"HD 32564: P={r['periods'][i]:.6f} d; K={r['amplitudes'][i]:.2f} m/s",xlabel='Orbital phase (circular model)',ylabel='Residual + component (m/s)')
fig.suptitle('Replication of external lead; activity/alias validation incomplete')
fig.savefig(p/'reported-family.png',dpi=140)
