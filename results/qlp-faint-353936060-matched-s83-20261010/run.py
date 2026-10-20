"""Post-hoc same-exposure comparison; no new epochs or ephemeris fitting."""
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
out=Path(__file__).parent;source=Path('results/qlp-faint-expanded-20261010/targets/353936060.json');frozen=Path('results/qlp-faint-expanded-followup-20261010/353936060-peak0/frozen.json');target=json.loads(source.read_text())['target'];target=dict(target,training_sectors=[83]);b=json.loads(frozen.read_text())['best'];path=Path('data/lightcurves/s0083-353936060.fits')
assert not (out/'plan.json').exists()
save_json(out/'plan.json',{'utc':now(),'frozen_sha256':sha(frozen),'discovery_sha256':sha(source),'spoc_sha256':sha(path),'match_tolerance_seconds':5,'script_sha256':sha(Path(__file__)),'policy':'Post-hoc same-exposure check at fixed ephemeris with a predeclared five-second matching tolerance. Unique nearest matches within5sec; retain each original time. Compare common/excluded points and raw SAP versus PDCSAP with same detrending. Same images, no independent validation or new reserved epochs.'})
q=load_qlp(target,Path('data'),bin_minutes=0);p=load_training(target,Path('data'))
with fits.open(path) as h:
 integrity=verify_hdus(path,h);assert h[0].header['TICID']==target['tic'] and h[0].header['SECTOR']==83
 d=h[1].data;t,y,e=(np.array(d[k],float) for k in ['TIME','SAP_FLUX','SAP_FLUX_ERR']);keep=(d['QUALITY']==0)&np.isfinite(t)&np.isfinite(y)&np.isfinite(e)&(y>0)&(e>0);t,y,e=t[keep],y[keep],e[keep];order=np.argsort(t);t,y,e=t[order],y[order],e[order];assert np.all(np.diff(t)>0);sap=flatten(t,y,e)
def measure(arr):
 return fixed_measure(*arr[:3],b['period'],b['transit_time'],b['duration']) if len(arr[0]) else None
def compare(other):
 idx=np.searchsorted(other[0],q[0]);left=np.clip(idx-1,0,len(other[0])-1);right=np.clip(idx,0,len(other[0])-1);near=np.where(abs(other[0][left]-q[0])<abs(other[0][right]-q[0]),left,right);delta=abs(other[0][near]-q[0])*86400;matched=delta<5;assert len(set(near[matched]))==int(matched.sum())
 return {'n_qlp':len(q[0]),'n_other':len(other[0]),'n_matched':int(matched.sum()),'matched_offset_seconds_range':[float(delta[matched].min()),float(delta[matched].max())],'qlp_common':measure([a[matched] for a in q[:3]]),'other_common':measure([a[near[matched]] for a in other[:3]]),'qlp_unmatched':measure([a[~matched] for a in q[:3]])}
save_json(out/'results.json',{'utc':now(),'qlp_full':measure(q),'spoc_pdcsap_full':measure(p),'spoc_sap_full':measure(sap),'pdcsap_comparison':compare(p),'sap_comparison':compare(sap),'qlp_evidence':q[3],'spoc_evidence':p[3],'spoc_integrity':integrity})
for name,other in [('pdcsap',p),('sap',sap)]:
 r=compare(other);print(name,'matches',r['n_matched'])
 for k in ['qlp_common','other_common','qlp_unmatched']:print(k,None if r[k] is None else r[k]['total'])
