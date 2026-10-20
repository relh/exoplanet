"""Frozen follow-up of a snapshot of residual review passes."""
from pathlib import Path
import json
from functools import partial
from exoplanet.pipeline import save_json,sha,now
from exoplanet.qlp_followup import follow_qlp
from exoplanet.qlp_campaign import load_qlp
from exoplanet.plots import plot_discovery
out=Path(__file__).parent;assert not (out/'plan.json').exists();items=[]
prior=json.loads(Path('results/qlp-residual2-followup-20261010/plan.json').read_text());seen={(x['path'],x['peak_index']) for x in prior['items']}
for p in sorted(Path('results/qlp-full-pool-residual2-20261010').glob('case-*/round-*/targets/*.json')):
 d=json.loads(p.read_text())
 for i,k in enumerate(d.get('screened_peaks',[])):
  if set(k['flags'])<={'crowding_or_missing_crowding'} and (str(p),i) not in seen:items.append({'path':str(p),'sha256':sha(p),'tic':d['tic'],'peak_index':i,'case':p.parents[2].name,'round':p.parents[1].name})
save_json(out/'plan.json',{'utc':now(),'items':items,'script_sha256':sha(Path(__file__)),'policy':'Snapshot during residual survey. Native QLP refinement and first2 assigned reserved sectors. Original dominant-signal masks retained and explicitly recorded; their ephemerides are not independently validated. Additional search trials uncalibrated. Cache flags distinguish prior opening. No automatic source/planet/novelty claim.'})
rows=[]
for item in items:
 dest=out/f"{item['tic']}-{item['round']}-peak{item['peak_index']}"
 try:
  checks=follow_qlp(Path(item['path']),dest,peak_index=item['peak_index'],max_sectors=2)
  plot_discovery(Path(item['path']),dest/'discovery.png',peak_index=item['peak_index'],loader=partial(load_qlp,bin_minutes=0))
  rows.append({**item,'status':'complete','heldout':[{'sector':c['sector'],'conclusion':c.get('conclusion',c.get('error'))} for c in checks]})
 except Exception as exc:rows.append({**item,'status':'error','error':repr(exc)})
 save_json(out/'results.json',rows)
print(rows,flush=True)
