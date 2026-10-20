from pathlib import Path
import json,numpy as np
from astropy.io import fits
from exoplanet.pipeline import sha,save_json,now
O=Path(__file__).parent;p=json.loads((O/'plan.json').read_text());r=json.loads((O/'results.json').read_text());assert r['plan_sha256']==sha(O/'plan.json');b=p['clock'];verified=0
for path,h in p['inputs'].items():assert sha(Path(path))==h
# Independent centered scalar least-squares, not the run's matrix solver.
def check(dt,y,saved):
 global verified
 a=np.isfinite(y)&(abs(dt)<b['duration']/2);c=np.isfinite(y)&(abs(dt)>b['duration'])&(abs(dt)<3*b['duration'])
 if a.sum()<2 or c.sum()<5:assert saved is None;return
 xx=dt[c];yy=y[c];slope=np.dot(xx-xx.mean(),yy-yy.mean())/np.dot(xx-xx.mean(),xx-xx.mean());intercept=yy.mean()-slope*xx.mean();res=y-intercept-slope*dt;offset=float(np.mean(res[a]));scatter=float(np.std(res[c],ddof=2));assert saved['n_in']==int(a.sum()) and saved['n_out']==int(c.sum());np.testing.assert_allclose([offset,scatter],[saved['offset'],saved['scatter']],rtol=1e-6,atol=1e-10)
 if saved['ratio'] is not None and scatter>1e-10:np.testing.assert_allclose(offset/scatter,saved['ratio'],rtol=1e-6,atol=1e-7)
 verified+=1
for row in r['events']:
 with fits.open(f"data/lightcurves/s{row['sector']:04d}-402358350.fits",checksum=False) as h:
  data=h[1].data;good=(data['QUALITY']==0)&np.isfinite(data['TIME']);t=np.asarray(data['TIME'][good],float);phase=(t-b['transit_time']+b['period']/2)%b['period']-b['period']/2;allowed=abs(phase)>=b['duration'];assert row['center_btjd']==b['transit_time']+row['event']*b['period']
  for key,z in row['channels'].items():
   y=np.asarray(data[key][good],float);check(t-row['center_btjd'],y,z['measurement']);assert z['constant_channel']==bool(np.nanmax(y)==np.nanmin(y));eligible=[]
   for c in z['controls']:
    check((t-row['center_btjd']-c['shift']*b['period'])[allowed],y[allowed],c['measurement']);m=z['measurement'];v=c['measurement'];matched=bool(m is not None and v is not None and .8<=v['n_in']/m['n_in']<=1.2 and .8<=v['n_out']/m['n_out']<=1.2);assert matched==c['matched_counts']
    if matched and v['ratio'] is not None:eligible.append(v['ratio'])
   assert len(eligible)==z['n_matched'];rank=None if z['constant_channel'] or m is None or m['ratio'] is None or not eligible else sum(abs(v)>=abs(m['ratio']) for v in eligible);assert rank==z['n_control_abs_ratio_ge_event']
save_json(O/'verification.json',dict(status='passed',created_utc=now(),script_sha256=sha(Path(__file__)),independent_measurements=verified,scope='Independent centered scalar regressions, coverage/count matching, constant-channel flags and control ranks; rawhashes/fixedclock. Control windows correlated and not a false-alarm probability.'));print('verified',verified)
