from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
O=Path(__file__).parent;r=json.loads((O/'results.json').read_text())['rows'];fig,axs=plt.subplots(1,4,figsize=(15,5),sharey=True)
for ax,sector in zip(axs,[19,43,44,59]):
 for i,row in enumerate(r):
  m=next(s for s in row['sectors'] if s['sector']==sector)['measurement']['total'];color='tab:blue' if row['clock']=='primary' else 'tab:orange';ax.errorbar(m['depth']*1e6,i,xerr=m['error']*1e6,fmt='o',color=color)
 ax.axvline(0,color='gray',lw=.5);ax.set_title(f'Sector{sector}');ax.set_xlabel('Fixed-clock depth ± formal error(ppm)');ax.set_yticks(range(len(r)),[f"{x['clock']} {x['kind']} {x['window']}d" for x in r]);ax.grid(alpha=.15)
fig.suptitle('TIC96166003: retrospective clock × processing comparison; shared photons');fig.tight_layout();fig.savefig(O/'comparison.png',dpi=150)
