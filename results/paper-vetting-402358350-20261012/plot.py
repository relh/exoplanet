from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(__file__).parent
r=json.loads((p/'results.json').read_text())
fig,ax=plt.subplots(figsize=(9,5))
for j,kind in enumerate(['SAP','PDCSAP']):
 ss=[s for s in r['summary'] if s['kind']==kind];xx=[i+(j-.5)*.16 for i in range(6)]
 ax.errorbar(xx,[s['depth']*1e6 for s in ss],yerr=[s['inflated_error_fixed_weights']*1e6 for s in ss],fmt='o',label=kind+' time-averaged noise',capsize=5)
 ax.errorbar(xx,[s['depth']*1e6 for s in ss],yerr=[s['original_error']*1e6 for s in ss],fmt='none',ecolor='black',capsize=2,alpha=.5)
ax.set_xticks(range(6),['constant 3D','constant 5D','linear 3D','linear 5D','quadratic 3D','quadratic 5D'])
ax.set_ylabel('Fixed-clock combined depth (ppm)');ax.set_ylim(0,850);ax.set_title('TIC 402358350: sensitivity to correlated residuals');ax.legend()
ax.text(.01,.02,'Colored bars: heuristic beta inflation; black: previous errors.\nThese are not planet probabilities or global detection significance.',transform=ax.transAxes,fontsize=9)
fig.tight_layout();fig.savefig(p/'noise-sensitivity.png',dpi=160)
