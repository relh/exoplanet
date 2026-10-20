from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
O=Path(__file__).parent;r=json.loads((O/'results.json').read_text());obs=json.loads((O/'observed.json').read_text());fig,axs=plt.subplots(1,3,figsize=(12,4),sharex=True)
for ax,length in zip(axs,[.25,.5,1.]):
 ax.hist([x['best']['power'] for x in r if x['block_days']==length],bins=10,color='gray');ax.axvline(obs['observed']['power'],label='Observed',color='red');ax.axvline(obs['inverted']['power'],label='Inverted',color='blue',ls=':');ax.set_title(f'{length}day blocks ·40controls');ax.set_xlabel('Selected-family maximum BLS likelihood');ax.legend()
fig.suptitle('Conditional sector/block randomizations: not original-search or global false-alarm probability');fig.tight_layout();fig.savefig(O/'controls.png',dpi=150)
