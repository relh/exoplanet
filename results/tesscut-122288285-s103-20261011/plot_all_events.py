from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;fig,axes=plt.subplots(3,2,figsize=(10,12),constrained_layout=True);inputs={}
for row,(sector,suffix,peak) in enumerate([(103,'',0),(102,'-peak1',1),(103,'-peak1',1)]):
 p=Path(f'results/tesscut-122288285-s{sector}{suffix}-20261011');a=json.loads((p/'analysis.json').read_text());images=np.load(p/'images.npz')['event_differences']
 for ax,n,im in zip(axes[row],a['event_numbers'],images):
  z=ax.imshow(im,origin='lower');fig.colorbar(z,ax=ax);ax.plot(*a['target_xy'],'rx');ax.set_title(f'Peak {peak}, S{sector}, event {n}')
 for name in ('analysis.json','images.npz'):inputs[str(p/name)]=sha(p/name)
fig.savefig(out/'individual-events.png',dpi=130)
save_json(out/'individual-events.json',{'inputs':inputs,'script_sha256':sha(Path(__file__)),'plot_sha256':sha(out/'individual-events.png'),'limits':'Unmodified individual differences, independent color scales. No background correction or significance claim.'})
