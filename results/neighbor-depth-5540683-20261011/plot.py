from pathlib import Path
import json,numpy as np,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(__file__).parent;r=json.loads((p/'results.json').read_text());fig,axes=plt.subplots(1,2,figsize=(11,4),constrained_layout=True)
for ax,s in zip(axes,r['sectors']):
 for ap in s['apertures']:
  ax.errorbar([v['event'] for v in ap['events']],[100*v['depth'] for v in ap['events']],yerr=[100*v['error'] for v in ap['events']],fmt='o-',label=f"r={ap['radius_pixels']}px diluted aperture",ms=4)
 for m,ls in zip(s['models'],['--',':']):ax.axhline(100*m['fractional_dip'],ls=ls,label=m['model'])
 ax.set_title(f"Sector{s['sector']}: assumed neighbor5540683");ax.set_xlabel('Fixed-clock event number');ax.set_ylabel('Average fractional dip (%)');ax.legend(fontsize=7);ax.grid(alpha=.2)
fig.suptitle('Diluted aperture measurements and model-dependent intrinsic depths');fig.savefig(p/'depths.png',dpi=160)
