"""One predeclared ephemeris, independent adjacent epoch, no retuning."""
from pathlib import Path
import json
from exoplanet.pipeline import save_json,sha,now
from exoplanet.qlp_campaign import load_qlp
from exoplanet.campaign import load_training
from exoplanet.followup import fixed_measure,prediction_spread
out=Path(__file__).parent
discovery=Path('results/qlp-faint-sector31-pilot-20261010/targets/170590556.json')
target=json.loads(discovery.read_text())['target']
paths=[Path(f'results/qlp-faint-sector31-pilot-followup-20261010/170590556-peak{i}/frozen.json') for i in range(1)]
frozen=[json.loads(p.read_text()) for p in paths]
assert 32 in target['sectors'] and 32 not in target['heldout_sectors']
assert not (out/'plan.json').exists()
assert not Path('data/qlp/170590556-s0032.fits').exists()
save_json(out/'plan.json',{'utc':now(),'sector':32,'discovery_sha256':sha(discovery),'script_sha256':sha(Path(__file__)),'frozen':[{'path':str(p),'sha256':sha(p),'best':f['best']} for p,f in zip(paths,frozen)],'policy':'Freeze Sector31 fit before opening unreserved adjacent Sector32. No period/phase retuning or profile maximization. Conditional timing-spread heuristic retained; same-sector reductions are not independent epochs. Reserved4/5 already evaluated; no retuning.'})
rows=[]
for name,loader in [('qlp',load_qlp),('spoc',load_training)]:
 try:
  t,y,e,evidence=loader(dict(target,training_sectors=[32]),Path('data'))
  for i,f in enumerate(frozen):
   b=f['best'];m=fixed_measure(t,y,e,b['period'],b['transit_time'],b['duration']);spread=prediction_spread(t,b,f['timing_ranges'])
   row={'reduction':name,'peak':i,'status':'measured','data':evidence,'measurement':m,'prediction_spread_days':spread,'timing_precise':spread<b['duration']/2,'limits':'No automatic confirmation/exclusion; timing profile conditional on discovery events.'};rows.append(row);print(name,i,m['total'],spread,flush=True)
 except Exception as exc:
  rows.append({'reduction':name,'status':'error','error':repr(exc)});print(name,repr(exc),flush=True)
 save_json(out/'results.json',rows)
