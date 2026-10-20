from pathlib import Path
import json,numpy as np
from exoplanet.pipeline import save_json,sha
from exoplanet.followup import fixed_measure
p=Path(__file__).parent;q=Path('results/sap-pdc-469309982-20261011');b=json.loads((q/'plan.json').read_text())['clock'];rows=[]
for kind in ['SAP','PDCSAP']:
 for window in [1.5,2.5]:
  path=q/f'{kind}-{window}.npz';z=np.load(path);t,y,e=[z[k] for k in ['t','y','e']];cycle=np.rint((t-b['transit_time'])/b['period']).astype(int)
  for omit in [[],[515],[522],[515,522]]:
   keep=~np.isin(cycle,omit);m=fixed_measure(t[keep],y[keep],e[keep],b['period'],b['transit_time'],b['duration']);rows.append(dict(kind=kind,window=window,omitted_cycles=omit,npz_sha256=sha(path),measurement=m))
save_json(p/'omission.json',dict(rows=rows,policy='Posthoc sensitivity test of whole cycles515/522 selected from telemetry. Fixed prior clock and existing flattening; no refitting or independent confirmation. Retain all-data reference.'))
print([(r['kind'],r['window'],r['omitted_cycles'],round(r['measurement']['total']['snr'],3)) for r in rows])
