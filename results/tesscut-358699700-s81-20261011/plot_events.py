from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent
fig,axes=plt.subplots(1,2,figsize=(10,9),constrained_layout=True);inputs={}
for row,s in enumerate((81,)):
 p=Path(f'results/tesscut-358699700-s{s}-20261011');a=json.loads((p/'analysis.json').read_text());im=np.load(p/'images.npz')['event_differences'];assert len(im)==2
 for j,(n,d) in enumerate(zip(a['event_numbers'],im)):
  ax=axes[j];z=ax.imshow(d,origin='lower');fig.colorbar(z,ax=ax);ax.plot(*a['target_xy'],'rx')
  for tic in (358699700,):
   v=next(v for v in a['neighbors'] if v['tic']==tic);ax.plot(v['x'],v['y'],'o',mfc='none',mec='orange');ax.annotate(str(tic),(v['x'],v['y']),fontsize=7)
  ax.set_title(f'Sector {s}, event {n}: out minus in')
 for name in ('analysis.json','images.npz'):inputs[str(p/name)]=sha(p/name)
fig.savefig(out/'individual-events.png',dpi=140)
save_json(out/'individual-events.json',{'inputs':inputs,'script_sha256':sha(Path(__file__)),'plot_sha256':sha(out/'individual-events.png'),'limits':'Unmodified individual difference arrays; separate color scales, no background correction or per-event significance claim.'})
