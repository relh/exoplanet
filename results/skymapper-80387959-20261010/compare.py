"""Per-filter fixed-event comparisons, with single-event limitations preserved."""
from pathlib import Path
import json
import numpy as np
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent;p=out/'analysis.json';d=json.loads(p.read_text());fp=Path('results/followup-80387959-qlp90-100-20261009/frozen.json');f=json.loads(fp.read_text());b=f['best'];ranges=f['timing_ranges'];floor=ranges.get('conditional_epoch_floor_days',0)
rows=[]
for r in d['detections']:
 predictions=np.array([e+r['event']*period for period,e in ranges['profile_timing_pairs']]);half=b['duration']/2-r['exptime_s']/172800
 rows.append({**r,'inside_all_profile_windows':bool(r['midpoint_btjd']>=predictions.max()+floor-half and r['midpoint_btjd']<=predictions.min()-floor+half)})
comparisons=[]
for obj in d['objects']:
 for policy in ['strict','relaxed']:
  for band in ['u','v','g','r','i','z']:
   rr=[r for r in rows if r['object_id']==obj['object_id'] and r['filter']==band and r[policy]];inside=[r for r in rr if r['inside_best']];outside=[r for r in rr if not r['inside_timing_envelope']]
   result={'object_id':obj['object_id'],'nearest_tic':obj['nearest_tic'],'policy':policy,'filter':band,'n_inside':len(inside),'n_outside':len(outside),'n_inside_robust_timing':sum(r['inside_all_profile_windows'] for r in inside),'n_inside_events':len({r['event'] for r in inside})}
   if inside and outside:
    def mean(x):
     w=np.array([1/r['error']**2 for r in x]);v=np.array([r['mag'] for r in x]);return float(np.average(v,weights=w)),float(1/w.sum())
    mi,vi=mean(inside);mo,vo=mean(outside);result.update(delta_mag=mi-mo,formal_error=float(np.sqrt(vi+vo)),baseline_median=float(np.median([r['mag'] for r in outside])),baseline_mad=float(1.4826*np.median(abs(np.array([r['mag'] for r in outside])-np.median([r['mag'] for r in outside])))))
   comparisons.append(result)
save_json(out/'comparisons.json',{'utc':now(),'analysis_sha256':sha(p),'script_sha256':sha(Path(__file__)),'rows':comparisons,'timing_checks':[{k:r[k] for k in ['object_id','filter','image_id','event','midpoint_btjd','inside_best','inside_all_profile_windows','strict','relaxed']} for r in rows if r['inside_timing_envelope']],'limits':'Single measurement per filter/event; formal PSF errors omit calibration and blending systematics. Each filter has its own baseline across other nights, not a simultaneous reference-star correction. No optimized phase, combined-color significance, planet claim or host exclusion.'})
for r in comparisons:
 if r['policy']=='relaxed' and r['n_inside']:print(r,flush=True)
