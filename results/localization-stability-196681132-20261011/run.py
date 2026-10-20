from pathlib import Path
import json,numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from exoplanet.pipeline import sha,save_json
from exoplanet.pixel_vet import centroid
out=Path(__file__).parent;root=Path('results/tesscut-196681132-s91-20261011');ap=root/'analysis.json';npth=root/'images.npz';a=json.loads(ap.read_text());images=np.load(npth)['event_differences'];target=np.array(a['target_xy']);n=next(r for r in a['neighbors'] if r['tic']==196683452);neighbor=np.array([n['x'],n['y']]);assert len(images)==len(a['event_numbers'])==22
save_json(out/'plan.json',{'script_sha256':sha(Path(__file__)),'inputs':{str(ap):sha(ap),str(npth):sha(npth)},'target_xy':target.tolist(),'neighbor_xy':neighbor.tolist(),'policy':'All22 event maps, existing background-subtracted positive moment algorithm; apertures centered independently at target and neighbor, halfwidth2/3. Sensitivity diagnostic only, no PRF confidence, no event rejection.'})
rows=[];fig,axes=plt.subplots(2,2,figsize=(10,9),constrained_layout=True)
for ci,(label,center) in enumerate([('target',target),('neighbor',neighbor)]):
 for wi,width in enumerate([2,3]):
  ax=axes[ci,wi];group=[]
  for event,im in zip(a['event_numbers'],images):
   try:
    c=centroid(im,center,halfwidth=width);dt=float(np.linalg.norm(c-target));dn=float(np.linalg.norm(c-neighbor));row={'event':event,'aperture_center':label,'halfwidth':width,'xy':c.tolist(),'distance_target':dt,'distance_neighbor':dn,'closer_to_target':dt<dn};group.append(row);ax.plot(*c,'o',ms=3);ax.annotate(str(event),c,fontsize=7)
   except ValueError as e:row={'event':event,'aperture_center':label,'halfwidth':width,'error':str(e)}
   rows.append(row)
  ax.plot(*target,'rx',ms=10,label='Target');ax.plot(*neighbor,'k+',ms=10,label='Neighbor');ax.set_aspect('equal');ax.set_xlim(4,9);ax.set_ylim(3,7);ax.set_title(f'{label} center, halfwidth{width}');ax.legend();print(label,width,sum(r['closer_to_target'] for r in group),len(group))
fig.savefig(out/'comparison.png',dpi=140);save_json(out/'results.json',{'rows':rows,'limits':'Same raw photons and catalog WCS. Moments depend on window/background/positive clipping; correlated errors and PRF shape omitted. Counts are not probabilities or calibrated host exclusions.'})
