from pathlib import Path
import json,numpy as np
from exoplanet.followup import fixed_measure
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());p=read(out/'plan.json');r=read(out/'results.json')
assert p['script_sha256']==sha(out/'run.py')
for path,h in p['inputs'].items():assert sha(Path(path))==h
for name,h in p['source_hashes'].items():assert sha(Path('src/exoplanet')/name)==h
assert r['plot_sha256']==sha(out/'folds.png') and [x['sector'] for x in r['rows']]==p['sectors']
for row in r['rows']:
 assert [x['parity'] for x in row['parities']]==[0,1]
 for d in row['data']:assert sha(Path(f"data/qlp/377129640-s{d['sector']:04d}.fits"))==d['source']['sha256']
period=p['short_period'];epoch=p['epoch'];duration=p['duration'];t=np.arange(epoch-10,epoch+10,.002);phase=(t-epoch+period/2)%period-period/2;cycles=np.rint((t-epoch)/period).astype(int);checks=[]
for depths in [[.03,.03],[.03,.015]]:
 y=np.ones_like(t)
 for parity,depth in enumerate(depths):y[(cycles%2==parity)&(abs(phase)<duration/2)]-=depth
 for parity,expected in enumerate(depths):
  m=fixed_measure(t,y,np.full_like(y,.001),2*period,epoch+parity*period,duration);delta=abs(m['total']['depth']-expected);assert delta<1e-10
  checks.append({'depths':depths,'parity':parity,'recovered':m['total']['depth'],'expected':expected,'error':delta})
save_json(out/'verification.json',{'script_sha256':sha(Path(__file__)),'results_sha256':sha(out/'results.json'),'controls':checks,'status':'Input/plot hashes and noiseless equal/unequal parity recovery verified; not physical eclipse or independent validation.'})
print('Verified fixed-clock comparison and four parity controls.')
