from pathlib import Path
import json
from exoplanet.pipeline import sha,save_json,now
from exoplanet.targeting import training_sectors
p=Path(__file__).parent;cp=p/'catalog.json';ip=Path('results/nearby-solar-radius-inventory-20261011/opportunities.json');ep=Path('results/solar-radius-pilot-selection-20261011/eligible.json');cat=json.loads(cp.read_text());op={r['tic']:r for r in json.loads(ip.read_text())};excluded_search={r['tic'] for r in json.loads(ep.read_text())};eligible=[]
for c in cat:
 tic=int(c['tic_id'].replace('TIC','').strip())
 if tic not in op:continue
 r=op[tic];s=r['star'];train=training_sectors(r['sectors'])
 if not train or s.get('contratio') is None or not 0<=s['contratio']<=.2:continue
 if any(Path(f'data/lightcurves/s{x:04d}-{tic}.fits').exists() for x in train+[r['reserved_sector']]):continue
 depth=1e6*(float(c['pl_rade'])/(109.076*s['rad']))**2
 eligible.append(dict(tic=tic,catalog_planet=c,depth_proxy_ppm=depth,target=dict(tic=tic,star=s,sectors=r['sectors'],training_sectors=train,heldout_sectors=[r['reserved_sector']])))
eligible.sort(key=lambda r:(abs(r['depth_proxy_ppm']-200),r['tic'],r['catalog_planet']['pl_name']));selected=[];used=set()
for r in eligible:
 if r['tic'] in used:continue
 assert r['tic'] not in excluded_search,'Control overlaps frozen unknown-object search'
 selected.append(r);used.add(r['tic'])
 if len(selected)==5:break
assert len(selected)==5
save_json(p/'eligible-controls.json',eligible);save_json(p/'selected-controls.json',selected);save_json(p/'selected.json',[r['target'] for r in selected])
save_json(p/'plan.json',dict(created_utc=now(),inputs={str(x):sha(x) for x in [cp,ip,ep,Path(__file__)]},selected_sha256=sha(p/'selected.json'),policy='Five distinct previously uncached hosts from the same solar-radius opportunity pool with confirmed transiting planets of0.5..3Earth radii and0.5..20day periods. Rank planet depth proxies by absolute distance from200ppm, then TIC/name; same adjacency/contamination requirements. Positive controls excluded from unknown-object pool. Pass only if target planet has a top-three period within1% AND no original screening flags. Other known planets and harmonics reported separately; no threshold changes. No held-out data is opened. Nonrandom controls, not completeness.'))
print([(r['tic'],r['catalog_planet']['pl_name'],r['depth_proxy_ppm']) for r in selected])
