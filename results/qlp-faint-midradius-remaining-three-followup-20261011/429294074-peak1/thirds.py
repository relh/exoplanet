from pathlib import Path
import json
from exoplanet.pipeline import save_json,sha,now
from exoplanet.qlp_campaign import load_qlp
from exoplanet.followup import fixed_measure
out=Path(__file__).parent
source=Path('results/qlp-faint-midradius-remaining-three-20261011/targets/429294074.json')
d=json.loads(source.read_text());f=json.loads((out/'frozen.json').read_text());b=f['best']
t,y,e,data=load_qlp(d['target'],Path('data'),bin_minutes=0)
rows=[]
for phase in [0.,1/3,2/3]:
 m=fixed_measure(t,y,e,b['period'],b['transit_time']+phase*b['period'],b['duration'])
 rows.append({'phase':phase,'measurement':m})
save_json(out/'thirds.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'discovery_sha256':sha(source),'frozen_sha256':sha(out/'frozen.json'),'data':data,'selected_period':b['period'],'period_over_three':b['period']/3,'rows':rows,'limits':'Post-selection diagnostic motivated by inspected folded plot. Existing fixed-event measurement unchanged. No independent validation or calibrated alias confidence; period/3 falls below original 0.5-day grid minimum.'})
print([(r['phase'],r['measurement']['total'],r['measurement']['supported_events']) for r in rows])
