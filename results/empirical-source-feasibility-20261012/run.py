from pathlib import Path
import json,numpy as np
from astropy.io import fits
from exoplanet.pipeline import save_json,sha,now
p=Path(__file__).parent
sources={80387959:['results/prf-80387959-20261009/models.json'],402358350:['results/prf-402358350-20261011/models.json','results/prf-402358350-s54-20261011/models.json','results/prf-402358350-s81-20261011/models.json']}
clocks={80387959:['results/followup-80387959-qlp90-100-20261009/frozen.json'],402358350:['results/source-check-402358350-20261011/frozen.json','results/prf-402358350-s81-20261011/frozen.json']}
assert not (p/'plan.json').exists()
plan=dict(created_utc=now(),script_sha256=sha(Path(__file__)),models=sources,clock_paths=clocks,input_sha256={q:sha(Path(q)) for qs in [*sources.values(),*clocks.values()] for q in qs},policy='Cached stamp-only feasibility; no downloads, candidate event flux comparisons, empirical individual-source PRF claims or host rankings. Exclude at least0.5day and3durations around every supplied frozen clock. Alternate2day blocks anchored at first finite time for out-of-event train/test. Fixed intercept+POS_CORR1/2 pixel regressions versus constant training mean; no tuning, no event evaluation. Placeholder or missing pointing means unavailable. This is aggregate-scene predictive adequacy, not source-response identification. Go to source model only after independent response identifiability and positive/negative host controls; no such successful controls presumed.')
save_json(p/'plan.json',plan);rows=[]
for tic,ms in sources.items():
 bs=[json.loads(Path(q).read_text())['best'] for q in clocks[tic]]
 for mp in ms:
  for meta in json.loads(Path(mp).read_text())['sectors']:
   path=Path(meta['pixel_path']);assert sha(path)==meta['pixel_sha256']
   with fits.open(path) as h:
    a=h[1].data;t=np.asarray(a['TIME'],float);ok=np.isfinite(t)&(a['QUALITY']==0)
    for b in bs:
     phase=np.remainder(t-b['transit_time']+b['period']/2,b['period'])-b['period']/2;ok&=abs(phase)>max(.5,3*b['duration'])
    anchor=float(np.nanmin(t));idx=np.flatnonzero(ok);ts=t[ok];flux=np.asarray(a['FLUX'][ok],float).reshape(len(ts),-1)
    cols=a.columns.names;pos=np.column_stack([np.asarray(a[c][ok],float) for c in ['POS_CORR1','POS_CORR2']]) if all(c in cols for c in ['POS_CORR1','POS_CORR2']) else None
   row=dict(tic=tic,sector=meta['sector'],pixel_path=str(path),pixel_sha256=sha(path),non_event_rows=len(ts),stamp_pixels=flux.shape[1],pointing_present=pos is not None)
   if pos is None or not np.all(np.isfinite(pos)) or np.max(np.std(pos,axis=0))<1e-10:
    row.update(status='pointing_unavailable_or_placeholder',pointing_nonfinite=None if pos is None else int((~np.isfinite(pos)).sum()));rows.append(row);continue
   train=(np.floor((ts-anchor)/2).astype(int)%2)==0;test=~train
   center=pos[train].mean(axis=0);scale=pos[train].std(axis=0);row.update(pointing_percentile_span_pixels=(np.percentile(pos,99,axis=0)-np.percentile(pos,1,axis=0)).tolist(),n_train=int(train.sum()),n_test=int(test.sum()),pointing_scale=scale.tolist())
   if np.min(scale)<1e-10:row.update(status='pointing_axis_degenerate');rows.append(row);continue
   x=np.column_stack([np.ones(len(ts)),(pos-center)/scale]);good=np.all(np.isfinite(flux),axis=0);y=flux[:,good];coef=np.linalg.lstsq(x[train],y[train],rcond=None)[0];mu=y[train].mean(axis=0);pred=x[test]@coef
   baseline=np.sqrt(np.mean((y[test]-mu)**2));rms=np.sqrt(np.mean((y[test]-pred)**2));sv=np.linalg.svd(x[train],compute_uv=False)
   within=np.all((pos[test]>=np.min(pos[train],axis=0))&(pos[test]<=np.max(pos[train],axis=0)),axis=1)
   row.update(status='aggregate_scene_diagnostic_only',good_pixels=int(good.sum()),design_condition=float(sv[0]/sv[-1]),test_within_train_pointing_box_fraction=float(within.mean()),constant_test_rms=float(baseline),linear_motion_test_rms=float(rms),rms_ratio=float(rms/baseline),pixel_response_design_rank=int(np.linalg.matrix_rank(x[train])))
   np.savez_compressed(p/f'{tic}-s{meta["sector"]}-diagnostic.npz',time=ts,pointing=pos,train=train,good_pixels=good,coef=coef,center=center,scale=scale,mean=mu)
   rows.append(row)
save_json(p/'results.json',dict(created_utc=now(),rows=rows,conclusion='NO-GO for an independently identified per-source empirical response from this simple aggregate-scene model. Pointing derivatives describe the sum of scene responses; they cannot decompose overlapping source PSFs without additional assumptions or calibration. No host attribution tested.'))
print([(r['tic'],r['sector'],r['status'],r.get('rms_ratio')) for r in rows])
