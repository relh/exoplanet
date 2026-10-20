from pathlib import Path
import json
from exoplanet.pipeline import sha,save_json
p=Path(__file__).parent;out=Path('results/solar-radius-positive-controls-run-20261011');rows=[];catalog=json.loads((p/'catalog.json').read_text())
for c in json.loads((p/'selected-controls.json').read_text()):
 path=out/'targets'/f"{c['tic']}.json";r=json.loads(path.read_text());period=float(c['catalog_planet']['pl_orbper']);matches=[dict(peak_index=i,**peak) for i,peak in enumerate(r.get('peaks',[])) if abs(peak['period']/period-1)<.01];screened=[dict(peak_index=i,period=x['best']['period'],flags=x['flags']) for i,x in enumerate(r.get('screened_peaks',[])) if abs(x['best']['period']/period-1)<.01];other=[]
 for cp in catalog:
  if int(cp['tic_id'].replace('TIC','').strip())!=c['tic'] or cp['pl_name']==c['catalog_planet']['pl_name']:continue
  ps=[i for i,x in enumerate(r.get('peaks',[])) if abs(x['period']/float(cp['pl_orbper'])-1)<.01]
  if ps:other.append(dict(name=cp['pl_name'],catalog_period=float(cp['pl_orbper']),matching_peak_indices=ps))
 rows.append(dict(tic=c['tic'],name=c['catalog_planet']['pl_name'],catalog_period=period,depth_proxy_ppm=c['depth_proxy_ppm'],disposition=r.get('disposition'),best=r.get('best'),selected_planet_period_matches=matches,selected_planet_screened_matches=screened,selected_planet_pass=any(not x['flags'] for x in screened),other_known_planet_matches=other,target_file_sha256=sha(path)))
save_json(p/'evaluation.json',dict(rows=rows,n_period_matches=sum(bool(x['selected_planet_period_matches']) for x in rows),n_full_passes=sum(x['selected_planet_pass'] for x in rows),limits='Preselected planet matched at1% relative period tolerance. Not exhaustive multisystem recovery or validation of physical identity by period alone. Other-planet matches kept separate.'))
for r in rows:print(r['name'],r['catalog_period'],r['best']['period'],r['selected_planet_pass'],r['other_known_planet_matches'])
