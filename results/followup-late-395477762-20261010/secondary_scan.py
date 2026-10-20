"""Exploratory secondary-phase search after visual inspection, training only."""
import json
from pathlib import Path
import numpy as np
from exoplanet.campaign import load_training
from exoplanet.followup import fixed_measure
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent
p=next(Path('results').glob('campaign-late-sectors-batch*-20261010/targets/395477762.json'))
row=json.loads(p.read_text());b=row['screened_peaks'][0]['best']
t,y,dy,data=load_training(row['target'],Path('data'));trials=[]
for phase in np.linspace(.1,.9,401):
 for duration in [.06,.09,.12,.15,.18]:
  m=fixed_measure(t,y,dy,b['period'],b['transit_time']+phase*b['period'],duration)
  if m['total']:trials.append({'phase':float(phase),'duration':duration,'measurement':m})
best=max(trials,key=lambda r:r['measurement']['total']['snr'])
save_json(out/'secondary-scan.json',{'created_utc':now(),'discovery_sha256':sha(p),'script_sha256':sha(Path(__file__)),'policy':'Exploratory phase/duration scan after visible second eclipse; not independent prediction or calibrated significance. Discovery sectors only.','data':data,'best':best,'trials':trials});print(best)
