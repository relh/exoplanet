from pathlib import Path
import json
from exoplanet.pipeline import sha,save_json,now
out=Path(__file__).parent;src=out/'results.json';rows=[]
for r in json.loads(src.read_text()):
 p=Path(r['path']);d=json.loads(p.read_text());maximum=min(20,d['clean_baseline_days']/2.5)
 rows.append({'tic':r['tic'],'period':r['period'],'radius_earth':r['radius_earth'],'maximum_search_period_days':maximum,'inside':.5<=r['period']<=maximum,'source_sha256':sha(p)})
save_json(out/'grid-audit.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'input_sha256':sha(src),'n_inside_requested_grid':sum(r['inside'] for r in rows),'rows':rows,'limits':'Requested period bounds only; not completeness or recovery.'})
print(sum(r['inside'] for r in rows),'of',len(rows),'inside')
