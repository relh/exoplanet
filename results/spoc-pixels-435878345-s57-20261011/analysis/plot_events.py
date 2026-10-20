from pathlib import Path
import json,numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;a=json.loads((out/'localization.json').read_text());maps=np.load(out/'images.npz')['event_differences'];plots=[]
assert len(maps)==len(a['event_numbers'])
neighbor=next(s for s in a['neighbors_by_distance'] if s['tic']==435878345)
for start in range(0,len(maps),12):
 fig,axes=plt.subplots(4,3,figsize=(12,16),constrained_layout=True)
 for ax,n,im in zip(axes.flat,a['event_numbers'][start:start+12],maps[start:start+12]):
  c=ax.imshow(im,origin='lower');fig.colorbar(c,ax=ax,shrink=.8);ax.plot(*a['header_target_xy'],'rx',label='target');ax.plot(neighbor['x'],neighbor['y'],'wo',mfc='none',label='435878345');ax.set_title(f'Processed event {n}');ax.legend(fontsize=7)
 for ax in list(axes.flat)[len(maps[start:start+12]):]:ax.set_visible(False)
 p=out/f'events-{start//12+1}.png';fig.savefig(p,dpi=120);plt.close(fig);plots.append(str(p))
save_json(out/'event-plots.json',{'script_sha256':sha(Path(__file__)),'inputs':{n:sha(out/n) for n in ['localization.json','images.npz']},'plots':{p:sha(Path(p)) for p in plots},'limits':'Unmodified individual differences; separate scales, not calibrated individual event significance.'})
print(len(maps), 'events',len(plots),'plots')
