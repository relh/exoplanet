from pathlib import Path
import json
from concurrent.futures import ThreadPoolExecutor,as_completed
from exoplanet.pipeline import fetch,read_curve,save_json,sha,now
from exoplanet.qlp_campaign import load_qlp,bin_curve
from exoplanet.search import flatten
from exoplanet.campaign import process_target,SETTINGS
out=Path(__file__).parent

def loader(target,root,window=1.5,bin_minutes=10):
 if target['discovery_collection']=='QLP':return load_qlp(target,root,window,bin_minutes)
 assert target['training_sectors']==[106] and target['tic']==146343560
 sector=106;obs=[r for r in target['other_products'] if r['sequence_number']==sector and r['provenance_name']=='SPOC'];assert len(obs)==1
 path=root/'alternate-epochs'/f'{target["tic"]}-s{sector:04d}.fits';source=fetch('https://mast.stsci.edu/api/v0.1/Download/file/?uri='+obs[0]['dataURL'],path)
 t,f,e,star=read_curve(path);assert int(star['ticid'])==target['tic'] and int(star['sector'])==sector
 assert all(h['checksum']=='verified' for h in star['fits_integrity'])
 n=len(t)
 if bin_minutes:t,f,e=bin_curve(t,f,e,width=bin_minutes/1440)
 t,f,e=flatten(t,f,e,window=window)
 return t,f,e,[{'sector':sector,'source':source,'star':star,'n_raw_quality_points':n,'n_clean_points':len(t),'bin_minutes':bin_minutes}]

if __name__=='__main__':
 targets=json.loads((out/'selected.json').read_text());assert not (out/'plan.json').exists()
 save_json(out/'plan.json',{'utc':now(),'targets':targets,'selected_sha256':sha(out/'selected.json'),'script_sha256':sha(Path(__file__)),'source_hashes':{p.name:sha(p) for p in Path('src/exoplanet').glob('*.py')},'settings':{**SETTINGS,'bin_minutes':10,'max_training_baseline_days':120},'policy':'Frozen nine discovery targets. Reserved photometry not loaded. SPOC adapter uses existing read_curve, bin_curve and flatten; QLP unchanged.'})
 (out/'targets').mkdir(exist_ok=True);rows=[]
 with ThreadPoolExecutor(max_workers=3) as pool:
  futures=[pool.submit(process_target,t,Path('data'),out,loader,120) for t in targets]
  for f in as_completed(futures):
   r=f.result();rows.append({k:r.get(k) for k in ['tic','status','error','disposition']});save_json(out/'progress.json',rows)
 save_json(out/'results.json',rows)
