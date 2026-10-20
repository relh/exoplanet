from pathlib import Path
import json,numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;rows=json.loads((out/'results.json').read_text())['rows'];fig,axes=plt.subplots(1,2,figsize=(10,4),constrained_layout=True)
for j,n in enumerate([2,3]):
 for width in [0.,.4]:
  es=[next(e for e in r['events'] if e['event']==n) for r in rows if r['width']==width];axes[j].scatter([e['target_amplitude'] for e in es],[e['neighbor090_amplitude'] for e in es],label=f'Broadening {width}px',s=20)
 axes[j].set_title(f'Event {n}: all 36 variants');axes[j].set_xlabel('Target conditional flux');axes[j].set_ylabel('Neighbor 090 conditional flux');axes[j].legend()
fig.savefig(out/'sensitivity.png',dpi=140)
summary=[]
for n in [2,3]:
 es=[e for r in rows for e in r['events'] if e['event']==n];inj={}
 for src in ['156001092','156001090']:
  xs=[i for e in es for i in e['injections'] if i['source']==src];inj[src]={k:[min(x[k] for x in xs),max(x[k] for x in xs)] for k in ['target_amplitude','neighbor090_amplitude']}
 summary.append({'event':n,'target_range':[min(e['target_amplitude'] for e in es),max(e['target_amplitude'] for e in es)],'neighbor_range':[min(e['neighbor090_amplitude'] for e in es),max(e['neighbor090_amplitude'] for e in es)],'injections':inj})
save_json(out/'summary.json',{'script_sha256':sha(Path(__file__)),'results_sha256':sha(out/'results.json'),'plot_sha256':sha(out/'sensitivity.png'),'rows':summary,'scene_rms_fraction_range':[min(r['scene_rms_fraction'] for r in rows),max(r['scene_rms_fraction'] for r in rows)]});print(summary)
