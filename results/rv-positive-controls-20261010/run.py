import csv,json
from pathlib import Path
import numpy as np
from exoplanet.rv_campaign import nightly
from exoplanet.rv_search import scan,refine
from exoplanet.pipeline import save_json,now,sha
out=Path(__file__).parent;catalog=list(csv.DictReader(open('data/rv/known-planets-20261010.csv')));results=[]
for name in ['HD40307','HD69830']:
 p=Path('data/rv/coverage-selected')/({'HD40307':'GJ2046','HD69830':'GJ302'}[name]+'.csv');t,y,e,g=nightly(p)
 expected=[dict(planet=r['pl_name'],period=float(r['pl_orbper'])) for r in catalog if r['hostname'].replace(' ','')==name]
 frequency=np.arange(1/300,1/.8,1/(8*np.ptp(t)));known=[];steps=[]
 for step in range(3):
  power=scan(t,y,e,g,frequency,known);known.append(float(1/frequency[np.nanargmax(power)]));solution=refine(t,y,e,g,known,fraction=.001);known=list(solution['periods']);steps.append(dict(periods=known,amplitudes=solution['amplitudes'].tolist()))
 matched=[r for r in expected if min(abs(np.array(known)/r['period']-1))<.02]
 result=dict(name=name,input_sha256=sha(p),nights=len(t),steps=steps,expected=expected,recovered=matched);results.append(result);print(name,'recovered',matched,flush=True)
save_json(out/'controls.json',dict(created_utc=now(),results=results,script_sha256=sha(Path(__file__)),limitations='Known-planet positive controls; recoverability is not completeness. Circular search and fixed2m/s white jitter; no assertion that every cataloged companion is recovered.'))
