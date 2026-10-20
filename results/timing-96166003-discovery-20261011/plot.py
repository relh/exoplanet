from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
O=Path(__file__).parent;f=json.loads((O/'frozen.json').read_text());fig,axes=plt.subplots(2,1,figsize=(9,7))
for ax,row in zip(axes,f['rows']):
 z=np.load(O/f"w{row['window']}-profile.npz");ax.plot(z['period'],z['power'].max()-z['power']);ax.axhline(4.5,color='orange');ax.axvline(json.loads((O/'plan.json').read_text())['seed']['period'],color='gray',ls='--');ax.set_ylim(0,15);ax.set_xlabel('Period(days)');ax.set_ylabel('Delta log likelihood');ax.set_title(f"TIC96166003 {row['window']}d detrending, discovery43/44")
fig.tight_layout();fig.savefig(O/'profiles.png',dpi=150)
