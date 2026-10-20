from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;r=json.loads((out/'results.json').read_text())
fig,axes=plt.subplots(4,1,figsize=(11,10),constrained_layout=True,sharex=True)
for ax,row in zip(axes,r['rows']):
 for tic,color,label in [('149919534','tab:blue','Target'),('149919536','tab:orange','Neighbor 536')]:
  xs=[x['mid'] for x in row['bins'] if x['status']=='measured'];ys=[x['amplitudes'][tic] for x in row['bins'] if x['status']=='measured'];ax.plot(xs,ys,'.-',color=color,label=label,lw=1)
 ax.axvspan(-.5,.5,color='gray',alpha=.2);ax.axhline(0,color='black',lw=.5);ax.set_title(f"{row['label']} — center BTJD {row['center']:.5f}");ax.set_ylabel('Conditional flux deficit');ax.legend(loc='upper right',ncol=2)
axes[-1].set_xlabel('Time from fixed center / duration (0.216 days); shaded = original dip window')
fig.suptitle('Fixed-scene time profiles; common-baseline correlations, no calibrated error bars')
fig.savefig(out/'profiles.png',dpi=140)
save_json(out/'plot-manifest.json',{'script_sha256':sha(Path(__file__)),'results_sha256':sha(out/'results.json'),'plot_sha256':sha(out/'profiles.png')})
