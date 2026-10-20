"""Post-hoc training-only harmonic measurement; no independent validation."""
from pathlib import Path
import json
from exoplanet.pipeline import save_json,sha,now
from exoplanet.qlp_campaign import load_qlp
from exoplanet.followup import fixed_measure
out=Path(__file__).parent
source=Path('results/qlp-faint-expanded-20261010/targets/31869709.json')
frozen=Path('results/qlp-faint-expanded-followup-20261010/31869709-peak2/frozen.json')
target=json.loads(source.read_text())['target'];b=json.loads(frozen.read_text())['best']
assert not (out/'plan.json').exists()
save_json(out/'plan.json',{'utc':now(),'source_sha256':sha(source),'frozen_sha256':sha(frozen),'script_sha256':sha(Path(__file__)),'policy':'Post-hoc training-only comparison of frozen period P and P/3. Measure three fixed phases 0,1/3,2/3 at original P, and pooled P/3. No optimization, new reserved data, source attribution, independent validation or novelty inference. Original failed detrending gate retained.','best':b,'sectors':target['training_sectors']})
rows=[]
for sector in [*target['training_sectors'],'combined']:
 t,y,e,data=load_qlp(target if sector=='combined' else dict(target,training_sectors=[sector]),Path('data'),bin_minutes=0)
 phases=[{'phase':i/3,'measurement':fixed_measure(t,y,e,b['period'],b['transit_time']+i*b['period']/3,b['duration'])} for i in range(3)]
 short=fixed_measure(t,y,e,b['period']/3,b['transit_time'],b['duration'])
 row={'sector':sector,'data':data,'phases':phases,'short_period':b['period']/3,'short_measurement':short};rows.append(row)
 print(sector,[(x['phase'],x['measurement']['total']) for x in phases], 'short',short['total'],flush=True)
save_json(out/'results.json',{'finished_utc':now(),'rows':rows})
