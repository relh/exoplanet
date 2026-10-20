"""Two predeclared ephemerides, independent adjacent epoch, no retuning."""
from pathlib import Path
import json
from exoplanet.pipeline import save_json,sha,now
from exoplanet.qlp_campaign import load_qlp
from exoplanet.campaign import load_training
from exoplanet.followup import fixed_measure,prediction_spread
out=Path(__file__).parent
discovery=Path('results/qlp-faint-sector91-pilot-20261010/targets/386739254.json')
target=json.loads(discovery.read_text())['target']
paths=[Path(f'results/qlp-faint-sector91-pilot-coverage-followup-20261010/386739254-peak{i}/frozen.json') for i in range(2)]
frozen=[json.loads(p.read_text()) for p in paths]
assert 90 in target['sectors'] and 90 not in target['heldout_sectors']
assert not (out/'plan.json').exists()
save_json(out/'plan.json',{'utc':now(),'sector':90,'discovery_sha256':sha(discovery),'script_sha256':sha(Path(__file__)),'frozen':[{'path':str(p),'sha256':sha(p),'best':f['best']} for p,f in zip(paths,frozen)],'policy':'Freeze both Sector91 fits before opening unreserved adjacent Sector90. No period/phase retuning or profile maximization. Conditional timing-spread heuristic retained; same-sector reductions are not independent epochs. Reserved46/63 untouched.'})
rows=[]
for name,loader in [('qlp',load_qlp),('spoc',load_training)]:
 try:
  t,y,e,evidence=loader(dict(target,training_sectors=[90]),Path('data'))
  for i,f in enumerate(frozen):
   b=f['best'];m=fixed_measure(t,y,e,b['period'],b['transit_time'],b['duration']);spread=prediction_spread(t,b,f['timing_ranges'])
   row={'reduction':name,'peak':i,'status':'measured','data':evidence,'measurement':m,'prediction_spread_days':spread,'timing_precise':spread<b['duration']/2,'limits':'No automatic confirmation/exclusion; timing profile conditional on two discovery events.'};rows.append(row);print(name,i,m['total'],spread,flush=True)
 except Exception as exc:
  rows.append({'reduction':name,'status':'error','error':repr(exc)});print(name,repr(exc),flush=True)
 save_json(out/'results.json',rows)
