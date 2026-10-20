from pathlib import Path
import json,numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
O=Path(__file__).parent;f=json.loads((O/'frozen.json').read_text());fig,ax=plt.subplots(1,2,figsize=(11,4))
for r in f['rows']:
 z=np.load(O/f"w{r['window']}-profile.npz");ax[0].plot(z['period'],z['power']-max(z['power']),label=f"{r['window']}day detrending");v=r['illustrative_forecasts'];ax[1].plot([x['days_after_training_end'] for x in v],[x['spread_days'] for x in v],'.-',label=f"{r['window']}day detrending")
ax[0].axhline(-4.5,color='gray',ls=':');ax[0].set_ylim(-20,1);ax[0].set_xlabel('Period (days)');ax[0].set_ylabel('Profile log-likelihood minus maximum');ax[0].legend();ax[1].axhline(f['rows'][0]['best']['duration']/2,color='gray',ls=':',label='Half-duration criterion');ax[1].set_xlabel('Hypothetical window start after training end (d)');ax[1].set_ylabel('Conditional timing spread (d)');ax[1].legend();fig.suptitle('TIC402358350: discovery40/41 timing only; no later observations opened');fig.tight_layout();fig.savefig(O/'timing.png',dpi=150)
