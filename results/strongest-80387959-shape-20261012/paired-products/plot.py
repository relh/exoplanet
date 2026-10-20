from pathlib import Path
import json,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
O=Path(__file__).parent;r=json.loads((O/'results.json').read_text())['rows'];fig,ax=plt.subplots(figsize=(7,4),constrained_layout=True)
for i,row in enumerate(r):
 for j,c in enumerate(row['rows'][:2]):ax.errorbar(i+(j-.5)*.12,c['depth_ppm'],yerr=c['conditional_error_ppm'],fmt='o',color=['tab:blue','tab:orange'][j],label=c['product'] if i==0 else None)
ax.set_xticks([0,1],['Sector36','Sector37']);ax.set(ylabel='Fixed-clock depth on matched cadences, ppm',title='Paired products: conditional errors; shared photons');ax.legend();fig.savefig(O/'comparison.png',dpi=140)
