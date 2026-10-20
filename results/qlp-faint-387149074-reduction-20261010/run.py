"""Same-epoch reduction check at an already frozen candidate ephemeris."""
from pathlib import Path
import json
import numpy as np
from exoplanet.pipeline import save_json,sha,now
from exoplanet.campaign import load_training
from exoplanet.qlp_campaign import load_qlp
from exoplanet.followup import fixed_measure
out=Path(__file__).parent;discovery=Path('results/qlp-faint-sector72-expanded-20261010/targets/387149074.json');frozen=Path('results/qlp-faint-sector72-followup-20261010/387149074-peak0/frozen.json');d=json.loads(discovery.read_text());f=json.loads(frozen.read_text());b=f['best'];target=d['target']
assert not (out/'plan.json').exists()
save_json(out/'plan.json',{'utc':now(),'discovery_sha256':sha(discovery),'frozen_sha256':sha(frozen),'best':b,'sectors':target['training_sectors'],'script_sha256':sha(Path(__file__)),'policy':'Same training epochs only, QLP versus TESS-SPOC. Fixed native QLP ephemeris, no retuning or new reserved sectors. Same images, different processing; not independent observations or source attribution. Retain download errors.'})
rows=[]
for name,loader in [('qlp',load_qlp),('spoc',load_training)]:
 parts=[]
 for sector in target['training_sectors']:
  row={'reduction':name,'sector':sector}
  try:
   t,y,e,evidence=loader(dict(target,training_sectors=[sector]),Path('data'));m=fixed_measure(t,y,e,b['period'],b['transit_time'],b['duration']);parts.append((t,y,e))
   row.update(status='measured',data=evidence,measurement=m,expected_formal_snr=None if m['total'] is None else b['depth']/m['total']['error'])
  except Exception as exc:row.update(status='error',error=repr(exc))
  rows.append(row);save_json(out/'progress.json',rows);print(name,sector,row['status'],row.get('measurement',{}).get('total',row.get('error')),flush=True)
 if parts:
  t,y,e=[np.concatenate([p[k] for p in parts]) for k in range(3)];order=np.argsort(t);m=fixed_measure(t[order],y[order],e[order],b['period'],b['transit_time'],b['duration']);rows.append({'reduction':name,'sector':'combined_available','n_sectors':len(parts),'status':'measured','measurement':m,'expected_formal_snr':None if m['total'] is None else b['depth']/m['total']['error']})
save_json(out/'results.json',rows)
