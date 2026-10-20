from pathlib import Path
import json
from exoplanet.pipeline import save_json,sha,now
from exoplanet.qlp_campaign import load_qlp
from exoplanet.followup import fixed_measure
out=Path(__file__).parent;disc=Path('results/qlp-faint-expanded-20261010/targets/207468582.json');sec=Path('results/qlp-faint-expanded-followup-20261010/207468582-peak0/secondary.json')
b=json.loads(disc.read_text())['screened_peaks'][0]['best'];s=json.loads(sec.read_text())['diagnostic']['best_dip'];epoch=b['transit_time']+s['phase']*b['period']
obs=Path('results/neighbor-207468583-20261010/observations.json');products={str(int(x['sequence_number'])):x for x in json.loads(obs.read_text())}
assert not (out/'plan.json').exists()
save_json(out/'plan.json',{'utc':now(),'discovery_sha256':sha(disc),'secondary_sha256':sha(sec),'script_sha256':sha(Path(__file__)),'period':b['period'],'secondary_epoch':epoch,'duration':s['duration'],'sectors':[76,79,83,86],'policy':'Post-hoc check of previously selected target secondary in neighbor aperture. All these primary light curves already inspected; no blind-validation claim. Exact original secondary phase/period/duration, no retuning. Same training epochs76/79 and later83/86 distinguished. No exclusion without secondary timing model.'})
rows=[]
for sector in [76,79,83,86]:
 t,y,e,data=load_qlp({'tic':207468583,'training_sectors':[sector],'qlp_products':products,'estimate_missing_errors':True},Path('data'),bin_minutes=0)
 m=fixed_measure(t,y,e,b['period'],epoch,s['duration']);rows.append({'sector':sector,'data':data,'measurement':m});save_json(out/'results.json',rows);print(sector,m['total'],m['supported_events'],flush=True)
