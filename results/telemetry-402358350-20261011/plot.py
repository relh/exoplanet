from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
O=Path(__file__).parent;r=json.loads((O/'results.json').read_text());channels=list(r['events'][0]['channels']);fig,axs=plt.subplots(1,5,figsize=(17,5),sharey=True)
for ax,key in zip(axs,channels):
 for i,event in enumerate(r['events']):
  z=event['channels'][key];m=z['measurement'];control=[c['measurement']['ratio'] for c in z['controls'] if c['matched_counts'] and c['measurement']['ratio'] is not None]
  ax.scatter(control,[i]*len(control),color='gray',alpha=.6,s=17)
  if m and m['ratio'] is not None:ax.scatter([m['ratio']],[i],color='red',marker='x',s=50)
 ax.axvline(0,color='black',lw=.5);ax.set_title(key);ax.set_xlabel('Offset / local residual scatter');ax.set_yticks(range(len(r['events'])),[f"S{x['sector']} event{x['event']}" for x in r['events']]);ax.grid(alpha=.2)
fig.suptitle('TIC402358350 fixed transit windows(red) versus count-matched off-event controls(gray)\nRatios descriptive, controls overlapping; no matched controls for S54event34');fig.tight_layout();fig.savefig(O/'matched-controls.png',dpi=140)
