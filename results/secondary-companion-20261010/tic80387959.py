"""Retrospective off-phase search of already-opened 80387959 SPOC data."""
from pathlib import Path
import json
from exoplanet.campaign import load_training
from exoplanet.secondary import scan_secondary
from exoplanet.followup import fixed_measure
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent
p=Path('results/campaign-small-stars-batch11-20261009/targets/80387959.json')
f=Path('results/followup-80387959-qlp90-100-20261009/frozen.json')
target=json.loads(p.read_text())['target'];target['training_sectors']=[10,36,37,63]
b=json.loads(f.read_text())['best']
t,y,e,data=load_training(target,Path('data'),bin_minutes=10)
r=scan_secondary(t,y,e,b);dip=r['best_dip'];checks=[]
for s in target['training_sectors']:
 one=dict(target,training_sectors=[s]);tt,yy,ee,dd=load_training(one,Path('data'),bin_minutes=10)
 checks.append({'sector':s,'measurement':fixed_measure(tt,yy,ee,b['period'],b['transit_time']+dip['phase']*b['period'],dip['duration'])})
save_json(out/'80387959.json',{'utc':now(),'seed_sha256':sha(f),'script_sha256':sha(Path(__file__)),'source_sha256':sha(Path('src/exoplanet/secondary.py')),'policy':'Retrospective diagnostic on already-opened SPOC Sectors10/36/37/63, using existing primary ephemeris. The phase is selected on all four sectors; per-sector depths are not independent validation. No planetary or source-attribution inference from absence of a convincing secondary.','data':data,'seed':b,'diagnostic':r,'per_sector':checks})
print(r['best_dip'],r['best_brightening'],r['selected_dip_events']['supported_events'])
print([(c['sector'],c['measurement']['total']) for c in checks])
