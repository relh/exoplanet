from pathlib import Path
import json,numpy as np
from astropy.io import fits
from exoplanet.pipeline import sha,save_json
p=Path(__file__).parent;plan=json.loads((p/'plan.json').read_text());result=json.loads((p/'results.json').read_text());f=json.loads(Path('results/followup-5546257-20261011/frozen.json').read_text());d=f['best']['duration'];checked=0
for path,digest in plan['inputs'].items():assert sha(Path(path))==digest
for event in result['events']:
 with fits.open(f"data/lightcurves/s{event['sector']:04d}-5546257.fits") as h:
  a=h[1].data;v=(a['QUALITY']==0)&np.isfinite(a['TIME']);dt=np.asarray(a['TIME'][v],float)-event['center_btjd']
  for name,m in event['channels'].items():
   y=np.asarray(a[name][v],float);inside=np.isfinite(y)&(abs(dt)<d/2);outside=np.isfinite(y)&(abs(dt)>d)&(abs(dt)<3*d)
   assert m is not None;assert inside.sum()==m['n_in'] and outside.sum()==m['n_out'];slope,intercept=np.polyfit(dt[outside],y[outside],1);res=y-(intercept+slope*dt);offset=np.mean(res[inside]);scale=np.std(res[outside],ddof=2)
   np.testing.assert_allclose([offset,scale],[m['offset'],m['outside_scatter']],rtol=1e-6,atol=1e-10);checked+=1
save_json(p/'verification.json',dict(status='passed',independent_polynomial_reconstructions=checked,inputs_hashed=True,limits='Descriptive residuals; offset/scatter is not a standard-error significance or causal test.'));print(checked)
