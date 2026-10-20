from pathlib import Path
import json,numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;a=json.loads((out/'analysis.json').read_text());maps=np.load(out/'images.npz')['event_differences'];assert len(maps)==len(a['event_numbers'])
fig,axes=plt.subplots(1,len(maps),figsize=(5*len(maps),5),squeeze=False,constrained_layout=True)
for ax,n,im in zip(axes[0],a['event_numbers'],maps):
 c=ax.imshow(im,origin='lower');fig.colorbar(c,ax=ax);ax.plot(*a['target_xy'],'rx');ax.set_title(f'S97 event{n}: out minus in')
fig.savefig(out/'individual-events.png',dpi=140)
save_json(out/'individual-events.json',{'script_sha256':sha(Path(__file__)),'inputs':{str(out/n):sha(out/n) for n in ['analysis.json','images.npz']},'plot_sha256':sha(out/'individual-events.png'),'limits':'Unmodified individual difference images; separate scales, no background or PRF confidence.'})
