from pathlib import Path
import json,numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;inputs={}
for label,path,meta,key in [('raw',out,'analysis.json','target_xy'),('processed',Path('results/spoc-pixels-377129640-s72-20261011/analysis'),'localization.json','header_target_xy')]:
 a=json.loads((path/meta).read_text());maps=np.load(path/'images.npz')['event_differences'];fig,axes=plt.subplots(3,3,figsize=(12,11),constrained_layout=True)
 for ax,n,im in zip(axes.flat,a['event_numbers'],maps):
  c=ax.imshow(im,origin='lower');fig.colorbar(c,ax=ax,shrink=.8);ax.plot(*a[key],'rx');ax.set_title(f'{label} event{n}')
 for ax in list(axes.flat)[len(maps):]:ax.set_visible(False)
 fig.savefig(out/f'{label}-events.png',dpi=120)
 inputs.update({str(path/n):sha(path/n) for n in [meta,'images.npz']})
save_json(out/'event-plots.json',{'script_sha256':sha(Path(__file__)),'inputs':inputs,'plots':{n:sha(out/n) for n in ['raw-events.png','processed-events.png']},'limits':'Unmodified event differences; separate scales, no background correction or per-event calibrated significance.'})
