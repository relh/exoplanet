from pathlib import Path
import json
from exoplanet.campaign import load_training
from exoplanet.followup import fixed_measure
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent;p=out/'followup/frozen.json';b=json.loads(p.read_text())['best'];d=json.loads((out/'discovery.json').read_text());rows=[]
for s in [17,18,52]:
 target=dict(d['target'],training_sectors=[s]);t,y,e,data=load_training(target,Path('data'))
 rows.append({'sector':s,'data':data,'measurement':fixed_measure(t,y,e,b['period'],b['transit_time'],b['duration'])})
save_json(out/'spoc-check.json',{'utc':now(),'frozen_sha256':sha(p),'rows':rows,'policy':'Fixed ephemeris, independent reduction of already-opened QLP epochs; not independent observations.'})
print([(r['sector'],r['measurement']['total']) for r in rows])
