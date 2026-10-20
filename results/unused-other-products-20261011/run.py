from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
from collections import Counter
import json
from exoplanet.archive import mast_query
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent;source=Path('results/qlp-faint-midradius-unused-coverage-audit-20261011/inventory.json')
targets=[r for r in json.loads(source.read_text()) if r['category'] in ['single_sector_only','no_qlp_product']]
assert len(targets)==1885 and not (out/'plan.json').exists()
save_json(out/'plan.json',{'utc':now(),'source':str(source),'source_sha256':sha(source),'script_sha256':sha(Path(__file__)),'targets':targets,'policy':'Metadata only exact numeric target_name query for SPOC/TESS-SPOC. No photometry opened. Alternative naming and other products may be missed; empty response is not absence of observations.'})
def query(i,group):
 request={'service':'Mast.Caom.Filtered','params':{'columns':'obs_id,target_name,provenance_name,sequence_number,dataURL','filters':[{'paramName':'target_name','values':[str(r['tic']) for r in group]},{'paramName':'provenance_name','values':['SPOC','TESS-SPOC']}]},'format':'json','pagesize':50000,'page':1}
 path=out/f'chunk-{i}.json'
 try:
  rows,meta=mast_query(request,path);return {'chunk':i,'ids':[r['tic'] for r in group],'status':'complete','path':str(path),'sha256':sha(path),'n_rows':len(rows)}
 except Exception as e:return {'chunk':i,'ids':[r['tic'] for r in group],'status':'error','error':repr(e)}
records=[]
with ThreadPoolExecutor(max_workers=3) as pool:
 futures=[pool.submit(query,i,targets[i:i+100]) for i in range(0,len(targets),100)]
 for f in as_completed(futures):
  r=f.result();records.append(r);save_json(out/'progress.json',records);print(r['chunk'],r['status'],r.get('n_rows'),flush=True)
save_json(out/'results.json',records)
