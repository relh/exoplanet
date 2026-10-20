from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
O=Path(__file__).parent;r=json.loads((O/'comparison.json').read_text())['rows'];fig,axes=plt.subplots(1,2,figsize=(11,4),sharey=True)
for ax,w in zip(axes,[1.5,2.5]):
 for component,shift,col in [('primary',-.10,'tab:blue'),('half_phase',.10,'tab:orange')]:
  rr=[x for x in r if x['window']==w and x['component']==component];rr.sort(key=lambda x:x['sector']);ax.errorbar([i+shift for i in range(4)],[x['total']['depth']*1e6 for x in rr],[x['total']['error']*1e6 for x in rr],fmt='o',label=component,color=col)
 ax.set_xticks(range(4),['40','41','54','81']);ax.set_xlabel('Sector');ax.set_title(f'{w}d detrending, unchanged pre81clock');ax.axhline(0,color='gray',lw=.6);ax.legend()
axes[0].set_ylabel('Fixed-window depth ± formal error(ppm)');fig.tight_layout();fig.savefig(O/'comparison.png',dpi=150)
