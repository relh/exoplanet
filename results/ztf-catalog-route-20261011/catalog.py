from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import requests,csv,io,json
from exoplanet.pipeline import sha,save_json,now
out=Path(__file__).parent;prior=Path('results/ztf-single-signals-20261011/plan.json');targets=json.loads(prior.read_text())['targets'];plans=[]
for row in targets:
 ra,dec=row['position'];query=f"SELECT TOP 100 * FROM ztf_objects_dr24 WHERE CONTAINS(POINT('ICRS',ra,dec),CIRCLE('ICRS',{ra},{dec},{3/3600}))=1"
 assert sha(Path(row['frozen_path']))==row['frozen_sha256']
 plans.append({**row,'query':query})
save_json(out/'catalog-plan.json',{'created':now(),'script_sha256':sha(Path(__file__)),'prior_plan_sha256':sha(prior),'targets':plans,'table':'ztf_objects_dr24','radius_arcsec':3,'limits':'Metadata only. No period adjustment. Catalog association is provisional pending positions and proper-motion checks.'})
def query(row):
 p=Path(f'data/ztf/catalog-route-{row["tic"]}.csv');params={'REQUEST':'doQuery','LANG':'ADQL','FORMAT':'csv','QUERY':row['query']}
 try:
  r=requests.get('https://irsa.ipac.caltech.edu/TAP/sync',params=params,timeout=45);r.raise_for_status();p.write_bytes(r.content);rows=list(csv.DictReader(io.StringIO(r.text)))
  if not rows or 'oid' not in rows[0]:
   assert r.text.startswith('oid,') or 'oid' in r.text.splitlines()[0],r.text[:500]
  return {'tic':row['tic'],'status':'downloaded','url':r.url,'path':str(p),'sha256':sha(p),'n_rows':len(rows),'rows':rows,'possibly_truncated':len(rows)==100}
 except Exception as e:return {'tic':row['tic'],'status':'error','error':repr(e)}
with ThreadPoolExecutor(max_workers=3) as pool:rows=list(pool.map(query,plans))
save_json(out/'catalog-results.json',rows)
for r in rows:print({k:v for k,v in r.items() if k!='rows'})
