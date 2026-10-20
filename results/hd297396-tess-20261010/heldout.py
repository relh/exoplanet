import json
from pathlib import Path
import numpy as np
from exoplanet.qlp_campaign import load_qlp
from exoplanet.followup import fixed_measure
from exoplanet.pipeline import save_json,now,sha
out=Path(__file__).parent;discovery=out/'discovery.json';models=json.loads(discovery.read_text())['results'];obs=json.loads(Path('results/hd297396-identity-20261010/observations.json').read_text());rows=[]
save_json(out/'heldout-configuration.json',dict(created_utc=now(),discovery_sha256=sha(discovery),sectors=[35,36],policy='No refinement of period, phase, duration or extraction window based on held photometry. Empirical errors only if published uncertainties entirely unavailable. KnownTOI period is external;4.27RV period previouslyopenedbuttransitphasefrom8/9only.'))
for sector in [35,36]:
 target={'tic':293547742,'training_sectors':[sector],'qlp_products':{str(o['sequence_number']):o for o in obs if o['provenance_name']=='QLP'},'estimate_missing_errors':True}
 t,y,e,sources=load_qlp(target,Path('data'));np.savez_compressed(out/f'heldout-s{sector}.npz',time=t,flux=y,error=e)
 result=[]
 for m in models:
  b=m['best'];measurement=fixed_measure(t,y,e,b['period'],b['transit_time'],b['duration']);result.append(dict(best=b,measurement=measurement))
 rows.append(dict(sector=sector,sources=sources,results=result));save_json(out/'heldout.json',dict(created_utc=now(),results=rows));print(sector,[(r['best']['period'],r['measurement']['total']) for r in result],flush=True)
