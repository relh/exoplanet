"""Known-planet controls on early and late QLP pairs; retain failed screens."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json,csv
import numpy as np
from exoplanet.archive import qlp_observations
from exoplanet.targeting import fetch_small_stars
from exoplanet.qlp_campaign import load_qlp
from exoplanet.campaign import process_target
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent;assert not (out/'search-plan.json').exists();tics=[259168516,271971130,389900760,8348911]
p=Path('results/selection-small-stars-20261009/catalog_confirmed.csv');periods={}
for r in csv.DictReader(p.open()):
 tic=int(r['tic_id'].replace('TIC','').strip())
 if tic in tics and r['pl_orbper']:periods.setdefault(tic,{}).setdefault(r['pl_name'],[]).append(float(r['pl_orbper']))
truth={tic:{name:float(np.median(v)) for name,v in names.items()} for tic,names in periods.items()}
stars=json.loads((out/'stars.json').read_text());tic_source=json.loads((out/'stars-source.json').read_text());by_id={int(s['ID']):s for s in stars};assert all(t in by_id for t in tics)
obs=json.loads((out/'observations.json').read_text());evidence=json.loads((out/'observations-source.json').read_text())
products={}
for r in obs:products.setdefault(int(r['target_name']),{})[int(r['sequence_number'])]=r
items=[]
for tic in tics:
 sectors=sorted(products[tic]);pairs=[[s,s+1] for s in sectors if s+1 in sectors]
 assert pairs,tic
 for label,pair in [('early',pairs[0]),('late',pairs[-1])]:
  if label=='late' and pair==pairs[0]:continue
  items.append({'label':label,'target':{'tic':tic,'star':by_id[tic],'sectors':sectors,'training_sectors':pair,'heldout_sectors':[],'estimate_missing_errors':True,'qlp_products':{str(s):r for s,r in products[tic].items()}}})
save_json(out/'search-plan.json',{'utc':now(),'truth':truth,'catalog_path':str(p),'catalog_sha256':sha(p),'tic_source':tic_source,'observations':evidence,'items':items,'source_sha256':{p.name:sha(p) for p in Path('src/exoplanet').glob('*.py')},'policy':'Known positive controls, never discoveries. Two hosts slightly exceed13.5mag and are boundary controls, not discovery selection members. Earliest and latest available adjacent QLP sectors, selected before photometry. Test period recovery within1% among top3 peaks and retain every screen flag. No completeness estimate or threshold tuning.'})
def run(item):
 folder=out/item['label'];(folder/'targets').mkdir(parents=True,exist_ok=True)
 r=process_target(item['target'],Path('data'),folder,loader=load_qlp,max_baseline=120)
 matches=[]
 for peak in r.get('peaks',[]):
  for name,period in truth[r['tic']].items():
   if abs(peak['period']/period-1)<.01:matches.append({'planet':name,'known_period':period,'peak':peak})
 return {'tic':r['tic'],'label':item['label'],'training_sectors':item['target']['training_sectors'],'status':r['status'],'error':r.get('error'),'disposition':r.get('disposition'),'period_matches':matches,'screen_flags':[p['flags'] for p in r.get('screened_peaks',[])]}
with ThreadPoolExecutor(max_workers=2) as executor:results=list(executor.map(run,items))
save_json(out/'results.json',results)
for r in results:print(r['tic'],r['label'],r['training_sectors'],[m['planet'] for m in r['period_matches']],r['screen_flags'],r['error'],flush=True)
