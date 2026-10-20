"""Post-hoc exact cadence-ID comparison at frozen ephemeris."""
from pathlib import Path
import json
import numpy as np
from astropy.io import fits
from exoplanet.pipeline import save_json,sha,now
from exoplanet.integrity import verify_hdus
from exoplanet.qlp_campaign import load_qlp
from exoplanet.campaign import load_training
from exoplanet.search import flatten
from exoplanet.followup import fixed_measure
out=Path(__file__).parent;source=Path('results/qlp-faint-midradius-remaining-two-20261011/targets/142396584.json');frozen=Path('results/qlp-faint-midradius-remaining-two-followup-20261011/142396584-peak0/frozen.json');target=json.loads(source.read_text())['target'];target=dict(target,training_sectors=[76]);b=json.loads(frozen.read_text())['best'];path=Path('data/lightcurves/s0076-142396584.fits')
assert not (out/'plan.json').exists()
save_json(out/'plan.json',{'utc':now(),'frozen_sha256':sha(frozen),'discovery_sha256':sha(source),'spoc_sha256':sha(path),'match_key':'CADENCENO', 'qlp_sha256':sha(Path('data/qlp/142396584-s0076.fits')), 'script_sha256':sha(Path(__file__)),'policy':'Post-hoc same-exposure check at fixed ephemeris. Match unique native CADENCENO identities, retaining each original timestamp. No retuning. Compare common/excluded points and raw SAP versus PDCSAP with same detrending. Same images, no independent validation or new reserved epochs.'})
q=load_qlp(target,Path('data'),bin_minutes=0);p=load_training(target,Path('data'))
with fits.open(path) as h:
 integrity=verify_hdus(path,h);assert h[0].header['TICID']==target['tic'] and h[0].header['SECTOR']==76
 d=h[1].data;t,y,e=(np.array(d[k],float) for k in ['TIME','SAP_FLUX','SAP_FLUX_ERR']);keep=(d['QUALITY']==0)&np.isfinite(t)&np.isfinite(y)&np.isfinite(e)&(y>0)&(e>0);t,y,e=t[keep],y[keep],e[keep];order=np.argsort(t);t,y,e=t[order],y[order],e[order];assert np.all(np.diff(t)>0);sap=flatten(t,y,e)
def measure(arr):
 return fixed_measure(*arr[:3],b['period'],b['transit_time'],b['duration']) if len(arr[0]) else None
with fits.open('data/qlp/142396584-s0076.fits') as h:
 native=h[1].data
 qids={float(t):int(c) for t,c in zip(native['TIME'],native['CADENCENO']) if np.isfinite(t)}
with fits.open(path) as h:
 native=h[1].data
 pids={float(t):int(c) for t,c in zip(native['TIME'],native['CADENCENO']) if np.isfinite(t)}
def compare(other):
 qc=np.array([qids[float(t)] for t in q[0]])
 pc=np.array([pids[float(t)] for t in other[0]])
 assert len(set(qc))==len(qc) and len(set(pc))==len(pc)
 lookup={int(c):i for i,c in enumerate(pc)}
 matched=np.array([int(c) in lookup for c in qc]);near=np.array([lookup[int(c)] for c in qc[matched]])
 delta=(other[0][near]-q[0][matched])*86400
 assert len(near)>0 and len(set(near))==len(near)
 return {'n_qlp':len(q[0]),'n_other':len(other[0]),'n_matched':int(matched.sum()),'matched_offset_seconds_range':[float(delta.min()),float(delta.max())],'qlp_common':measure([a[matched] for a in q[:3]]),'other_common':measure([a[near] for a in other[:3]]),'qlp_unmatched':measure([a[~matched] for a in q[:3]])}
save_json(out/'results.json',{'utc':now(),'qlp_full':measure(q),'spoc_pdcsap_full':measure(p),'spoc_sap_full':measure(sap),'pdcsap_comparison':compare(p),'sap_comparison':compare(sap),'qlp_evidence':q[3],'spoc_evidence':p[3],'spoc_integrity':integrity})
for name,other in [('pdcsap',p),('sap',sap)]:
 r=compare(other);print(name,'matches',r['n_matched'])
 for k in ['qlp_common','other_common','qlp_unmatched']:print(k,None if r[k] is None else r[k]['total'])
