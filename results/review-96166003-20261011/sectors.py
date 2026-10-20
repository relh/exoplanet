from pathlib import Path
import json
import numpy as np
from exoplanet.pipeline import read_curve,save_json,sha
from exoplanet.search import flatten
from exoplanet.followup import fixed_measure
O=Path(__file__).parent;r=json.loads((O/'discovery.json').read_text());b=r['best'];rows=[]
for w in [1.5,2.5]:
 for d in r['data']:
  p=Path(f"data/lightcurves/s{d['sector']:04d}-{r['tic']}.fits");assert sha(p)==d['source']['sha256'];t,f,e,_=read_curve(p);t,y,e=flatten(t,f,e,window=w);m=fixed_measure(t,y,e,b['period'],b['transit_time'],b['duration']);ph=(t-b['transit_time']+b['period']/2)%b['period']-b['period']/2;a=abs(ph)<b['duration']/2;c=(abs(ph)>b['duration'])&(abs(ph)<min(3*b['duration'],b['period']/2));wi=1/e[a]**2;wo=1/e[c]**2;depth=y[c]@wo/wo.sum()-y[a]@wi/wi.sum();err=np.sqrt(1/wi.sum()+1/wo.sum());np.testing.assert_allclose([depth,err],[m['total']['depth'],m['total']['error']],atol=1e-10);rows.append(dict(window=w,sector=d['sector'],measurement=m,raw_sha256=sha(p)))
save_json(O/'sectors.json',dict(script_sha256=sha(Path(__file__)),rows=rows,verification='Independent weighted in/out sums reproduce each fixed-clock sector total and formal error. Shared flattening, no global-search significance.'))
print([(x['window'],x['sector'],x['measurement']['total'],x['measurement']['supported_events']) for x in rows])
