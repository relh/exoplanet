"""Retrospective off-phase checks of current late-sector screening passes."""
from pathlib import Path
import json
from exoplanet.campaign import load_training
from exoplanet.secondary import scan_secondary
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent
items=[]
for p in Path('results').glob('campaign-late-sectors-batch*-20261010/targets/*.json'):
 try:d=json.loads(p.read_text())
 except json.JSONDecodeError:continue
 if d.get('disposition')=='followup_priority':items.append((p,d))
save_json(out/'plan.json',{'utc':now(),'policy':'Companion diagnostic; original discovery settings/results preserved. All unflagged late-sector passes available when invoked, training sectors only, ten-minute binning. Selected SNR not calibrated.','sources':{p.name:sha(p) for p in [Path('src/exoplanet/secondary.py'),Path('src/exoplanet/campaign.py')]},'targets':[{'tic':d['tic'],'discovery':str(p),'sha256':sha(p)} for p,d in items]})
for p,d in items:
 i=next(i for i,x in enumerate(d['screened_peaks']) if not x['flags']);b=d['screened_peaks'][i]['best']
 t,y,e,data=load_training(d['target'],Path('data'),bin_minutes=10)
 r=scan_secondary(t,y,e,b)
 save_json(out/f"{d['tic']}.json",{'tic':d['tic'],'discovery_sha256':sha(p),'seed':b,'data':data,'diagnostic':r})
 print(d['tic'],r['best_dip'],r['selected_dip_events']['supported_events'],flush=True)
