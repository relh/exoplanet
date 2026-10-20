from pathlib import Path
import json,numpy as np
from scipy.linalg import lstsq
from astropy.io import fits
from exoplanet.pipeline import sha,save_json
p=Path(__file__).parent;plan=json.loads((p/'plan.json').read_text());r=json.loads((p/'results.json').read_text());assert sha(p/'run.py')==plan['script_sha256']
for q,h in plan['input_sha256'].items():assert sha(Path(q))==h
count=0;rows=[]
for row in r['rows']:
 path=Path(row['pixel_path']);assert sha(path)==row['pixel_sha256'];tic=row['tic'];s=row['sector'];bs=[json.loads(Path(q).read_text())['best'] for q in plan['clock_paths'][str(tic)]]
 with fits.open(path) as h:
  a=h[1].data;t=np.asarray(a['TIME'],float);ok=np.isfinite(t)&(a['QUALITY']==0)
  for b in bs:
   nearest=np.rint((t-b['transit_time'])/b['period']);dist=np.abs(t-(b['transit_time']+nearest*b['period']));ok&=dist>max(.5,3*b['duration'])
  ts=t[ok];f=np.asarray(a['FLUX'][ok],float).reshape(len(ts),-1);pos=np.column_stack([a['POS_CORR1'][ok],a['POS_CORR2'][ok]]).astype(float);anchor=np.nanmin(t)
 assert len(ts)==row['non_event_rows']
 if row['status']=='pointing_unavailable_or_placeholder':assert np.max(np.std(pos,axis=0))<1e-10;continue
 z=np.load(p/f'{tic}-s{s}-diagnostic.npz');np.testing.assert_array_equal(z['time'],ts);np.testing.assert_array_equal(z['pointing'],pos);train=(np.floor((ts-anchor)/2).astype(int)%2)==0;np.testing.assert_array_equal(train,z['train']);good=np.all(np.isfinite(f),axis=0);np.testing.assert_array_equal(good,z['good_pixels']);x=np.column_stack([np.ones(len(ts)),(pos-pos[train].mean(axis=0))/pos[train].std(axis=0)]);y=f[:,good]
 coef,_,rank,_=lstsq(x[train],y[train],lapack_driver='gelsy');np.testing.assert_allclose(coef,z['coef'],rtol=1e-9,atol=1e-8);assert rank==3;count+=coef.shape[1]
 baseline=np.sqrt(np.sum((y[~train]-np.sum(y[train],axis=0)/train.sum())**2)/y[~train].size);rms=np.sqrt(np.sum((y[~train]-x[~train]@coef)**2)/y[~train].size)
 np.testing.assert_allclose([baseline,rms,rms/baseline],[row['constant_test_rms'],row['linear_motion_test_rms'],row['rms_ratio']],rtol=1e-9)
 rows.append(dict(tic=tic,sector=s,pixels=coef.shape[1]))
# Independent per-source templates are not identified by their fixed weighted sum.
# This illustrative positive normalized two-component scene has an exact null direction.
u=np.full((11,11),1/121);v=u.copy();h=np.zeros_like(u);h[4,4]=.0001;h[6,6]=-.0001;ratio=.1
u2=u+h;v2=v-h/ratio;assert np.all(u2>=0) and np.all(v2>=0)
np.testing.assert_allclose(u+ratio*v,u2+ratio*v2,atol=1e-16);np.testing.assert_allclose([u2.sum(),v2.sum()],[1,1]);assert np.max(abs(u-u2))>0
save_json(p/'verification.json',dict(status='passed',input_hashes_checked=len(plan['input_sha256']),raw_stamp_hashes_checked=len(r['rows']),independent_QR_pixel_regressions=count,independent_frozen_event_masks_and_splits=True,scene_decomposition_null_direction_demonstrated=True,limits='Null-direction example permits independent source templates; a imposed common parametric PSF adds assumptions and may remove this algebraic degeneracy, but is not independently calibrated here. No event or host-fit validation performed.',rows=rows))
print(count)
