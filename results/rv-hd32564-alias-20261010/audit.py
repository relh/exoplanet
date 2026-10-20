"""Aggregate disjoint held-year errors; retain fold disagreements and boundaries."""
from pathlib import Path
from collections import defaultdict
import json
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent;path=out/'results.json';rows=json.loads(path.read_text());assert len(rows)==384
groups=defaultdict(list)
for r in rows:
 v=r['variant'];groups[(r['reduction'],r['features'],v['component'],v['sampling'],v['sign'])].append(r)
summary=[]
for key,items in groups.items():
 assert len(items)==4 and {r['year'] for r in items}=={2010,2011,2012,2013}
 good=[r for r in items if r['status']=='complete']
 summary.append({'reduction':key[0],'features':key[1],'component':key[2],'sampling':key[3],'sign':key[4],'original_period':items[0]['variant']['original_period'],'alias_seed_period':items[0]['variant']['seeds'][key[2]],'n_errors':4-len(good),'sum_held_chi2_alias_minus_parent':sum(r['held_chi2_alias_minus_parent'] for r in good) if len(good)==4 else None,'year_deltas':{str(r['year']):r['held_chi2_alias_minus_parent'] for r in good},'bound_years':[r['year'] for r in good if r['alias_bound_hit']]})
save_json(out/'audit.json',{'utc':now(),'results_sha256':sha(path),'n_checks':len(rows),'n_errors':sum(r['status']=='error' for r in rows),'groups':summary,'limits':'Positive aggregate favors parent. Omitted years share training data; sum is not a calibrated significance. Bound-limited alternative fits and per-year reversals retained. Local optimization, selected aliases and circular models only.'})
for red in ['RV_mlc_nzp','RV_drs_nzp']:
 for feat in ['none','all_six']:
  print(red,feat,[(i,min((r['sum_held_chi2_alias_minus_parent'],r['alias_seed_period']) for r in summary if r['reduction']==red and r['features']==feat and r['component']==i)) for i in range(4)])
