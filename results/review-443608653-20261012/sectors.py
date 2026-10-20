from pathlib import Path
import json,numpy as np
from exoplanet.pipeline import read_curve,save_json,sha,now
from exoplanet.search import flatten
from exoplanet.followup import fixed_measure
O=Path(__file__).parent;b=json.loads((O/'discovery.json').read_text())['screened_peaks'][0]['best'];rows=[]
for window in [1.5,2.5]:
 for sector in [45,46]:
  p=Path(f'data/lightcurves/s{sector:04d}-443608653.fits');t,y,e,_=read_curve(p);t,y,e=flatten(t,y,e,window=window);m=fixed_measure(t,y,e,b['period'],b['transit_time'],b['duration']);ph=(t-b['transit_time']+b['period']/2)%b['period']-b['period']/2;a=abs(ph)<b['duration']/2;c=(abs(ph)>b['duration'])&(abs(ph)<3*b['duration']);wa=1/e[a]**2;wc=1/e[c]**2;d=y[c]@wc/wc.sum()-y[a]@wa/wa.sum();err=np.sqrt(1/wa.sum()+1/wc.sum());np.testing.assert_allclose([d,err],[m['total']['depth'],m['total']['error']],atol=1e-10);rows.append(dict(window=window,sector=sector,raw_sha256=sha(p),measurement=m))
save_json(O/'sectors.json',dict(created_utc=now(),script_sha256=sha(Path(__file__)),rows=rows,verification='Independent weighted sums reproduce four fixed-clock sector totals; no new clock or sector.'));print([(r['window'],r['sector'],r['measurement']['total']) for r in rows])
