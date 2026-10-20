from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
O=Path(__file__).parent;r=json.loads((O/'results.json').read_text());o=json.loads((O/'observed.json').read_text());fig,axs=plt.subplots(1,3,figsize=(12,4),sharex=True)
for ax,l in zip(axs,[.25,.5,1.]):
 ax.hist([x['statistic'] for x in r if x['block_days']==l],bins=10,color='gray');ax.axvline(o['result']['statistic'],color='red',label='Observed');ax.axvline(o['inverted']['statistic'],color='blue',ls=':',label='Inverted');ax.axvline(8,color='black',ls='--',label='Both-SNR threshold');ax.set_title(f'{l}day blocks;40draws');ax.set_xlabel('Minimum two-window local-refinement SNR');ax.legend(fontsize=8)
fig.suptitle('TIC469309982 actual weak-seed conditional controls; other localflag criteria also required');fig.tight_layout();fig.savefig(O/'controls.png',dpi=150)
