from pathlib import Path
import json,numpy as np
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;rows=[];inputs={}
for tic,sector in [(422626648,91),(241928959,92),(196681132,91)]:
 ap=Path(f'results/tesscut-{tic}-s{sector}-20261011/analysis.json');fp=Path(f'results/qlp-faint-midradius-single-review-20261011/{tic}-peak0/frozen.json');a=json.loads(ap.read_text());b=json.loads(fp.read_text())['best'];target=next(r for r in a['neighbors'] if r['tic']==tic);neighbors=[]
 inputs[str(ap)]=sha(ap);inputs[str(fp)]=sha(fp)
 for r in a['neighbors']:
  distance=float(np.hypot(r['x']-target['x'],r['y']-target['y']))
  if r['tic']==tic or distance>3 or r['Tmag'] is None:continue
  ratio=10**(-.4*(r['Tmag']-target['Tmag']));maximum=ratio/(1+ratio);needed=b['depth']/maximum
  neighbors.append({'tic':r['tic'],'distance_from_target_pixels':distance,'Tmag':r['Tmag'],'flux_ratio_equal_throughput':ratio,'max_observed_depth_total_eclipse':maximum,'required_eclipse_fraction':needed,'minimum_neighbor_to_target_throughput_ratio_for_total_eclipse':b['depth']/((1-b['depth'])*ratio),'viable_under_equal_throughput_two_star_assumption':needed<=1})
 rows.append({'tic':tic,'depth':b['depth'],'target_Tmag':target['Tmag'],'neighbors':neighbors})
save_json(out/'results.json',{'script_sha256':sha(Path(__file__)),'inputs':inputs,'rows':rows,'limits':'Illustrative two-source Tmag dilution only, within3pixels of catalog target. No measured aperture throughput, catalog errors, source variability, unseen companions or proper-motion propagation. A >100% required eclipse rules out only this restrictive model, not actual contamination. No host probability.'})
for r in rows:print(r['tic'],r['depth'],[(n['tic'],round(n['required_eclipse_fraction'],3),round(n['distance_from_target_pixels'],3)) for n in r['neighbors']])
