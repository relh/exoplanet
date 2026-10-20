from pathlib import Path
import json,numpy as np
from astropy.io import fits
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());p=read(out/'plan.json');r=read(out/'results.json')
assert sha(out/'run.py')==p['script_sha256']
for group in ['inputs','sources','raw']:
 for path,h in p[group].items():assert sha(Path(path))==h
assert [r['sector'] for r in r['rows']]==p['sectors']
checks=[]
for row in r['rows']:
 assert sha(Path(row['plot']))==row['plot_sha256']
 with fits.open(f"data/qlp/365744968-s{row['sector']:04d}.fits") as hd:
  d=hd[1].data
  for curve in row['curves'][:2]:
   t=np.asarray(d['TIME'],float);y=np.asarray(d[curve['label']],float)
   k=(d['QUALITY']==0)&np.isfinite(t)&np.isfinite(y)&(y>0);t=t[k];y=y[k];y/=np.median(y)
   assert len(t)==curve['n'];np.testing.assert_allclose(np.percentile(y,[1,50,99]),curve['percentiles_1_50_99'])
   phase=((t-p['epoch'])/p['period']+.5)%1-.5
   # Independently reconstruct bin assignments and medians.
   ix=np.floor((phase+.5)*80).astype(int);med=[float(np.median(y[ix==i])) for i in range(80) if np.sum(ix==i)>=3]
   np.testing.assert_allclose(med,curve['phase_medians'])
   checks.append({'sector':row['sector'],'column':curve['label'],'n':len(t),'bins':len(med)})
save_json(out/'verification.json',{'script_sha256':sha(Path(__file__)),'results_sha256':sha(out/'results.json'),'checks':checks,'status':'Raw/input/source/plot hashes and six unflattened curves verified; visual diagnostics, not a detection or physical classification.'})
print('Verified provenance and six independent fold reconstructions.')
