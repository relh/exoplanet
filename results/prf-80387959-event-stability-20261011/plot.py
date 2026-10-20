from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
out=Path(__file__).parent;rows=json.loads((out/'results.json').read_text())
hosts=['80387959','80387965','80387961','937808821']
fig,axes=plt.subplots(1,2,figsize=(10,10),constrained_layout=True)
for ax,key,title in zip(axes,['individual','leave_one_out'],['Individual event fits','Leave-one-event-out stacks']):
 labels=[];values=[]
 for r in rows:
  for e in r[key]:
   labels.append(f"S{r['sector']} / {e.get('event',e.get('omitted_event'))}")
   vals=[e['chi2'][h] for h in hosts];values.append(np.array(vals)-min(vals))
 im=ax.imshow(values,aspect='auto',vmin=0,vmax=30,cmap='viridis_r')
 ax.set_xticks(range(4),hosts,rotation=40,ha='right');ax.set_yticks(range(len(labels)),labels);ax.set_title(title)
 fig.colorbar(im,ax=ax,label='Conditional chi-square above best (clipped at30)')
fig.suptitle('TIC80387959 fixed templates: model preference, not host probability')
fig.savefig(out/'stability.png',dpi=140)
