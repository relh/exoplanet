"""Same-epoch single-event reduction comparison, no period inference."""
from pathlib import Path
import json
from exoplanet.pipeline import save_json,sha,now
from exoplanet.campaign import load_training
from exoplanet.qlp_campaign import load_qlp
from exoplanet.followup import fixed_measure
out=Path(__file__).parent;source=Path('results/qlp-faint-sector72-recovery-20261010/26587095/targets/26587095.json');r=json.loads(source.read_text());b=r['screened_peaks'][0]['best'];center=b['transit_time']+3*b['period']
assert not (out/'plan.json').exists()
save_json(out/'plan.json',{'utc':now(),'source_sha256':sha(source),'script_sha256':sha(Path(__file__)),'center_btjd':center,'duration_days':b['duration'],'target':r['target'],'policy':'Fixed observed event center and duration from recovery. Artificial100day period isolates this window only, not physical period inference. Compare same71epoch processing; reserve other sectors, no retuning.'})
rows=[]
for name,loader in [('qlp',load_qlp),('spoc',load_training)]:
 try:
  t,y,e,data=loader(r['target'],Path('data'));m=fixed_measure(t,y,e,100.,center,b['duration']);row={'reduction':name,'status':'measured','data':data,'measurement':m}
 except Exception as exc:row={'reduction':name,'status':'error','error':repr(exc)}
 rows.append(row);save_json(out/'results.json',rows);print(row.get('measurement',{}).get('total',row.get('error')),flush=True)
