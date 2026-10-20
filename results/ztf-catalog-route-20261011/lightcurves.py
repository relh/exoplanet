from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import requests,json,csv,io
from exoplanet.pipeline import sha,save_json,now
out=Path(__file__).parent;catalog=out/'catalog-results.json';rows=json.loads(catalog.read_text());plans=[]
for r in rows:
 assert r['status']=='downloaded' and not r['possibly_truncated']
 plans.append({'tic':r['tic'],'oids':[x['oid'] for x in r['rows']]})
save_json(out/'lightcurve-plan.json',{'created':now(),'catalog_sha256':sha(catalog),'script_sha256':sha(Path(__file__)),'targets':plans,'collection':'ztf_dr24','policy':'Retrieve all catalog-associated object IDs; preserve bad flags for later audit. No retiming. 60-second bounded request per target, no automatic retry.'})
def get(row):
 params=[('ID',oid) for oid in row['oids']]+[('COLLECTION','ztf_dr24'),('FORMAT','csv')];p=Path(f'data/ztf/id-route-{row["tic"]}.csv')
 url=requests.Request('GET','https://irsa.ipac.caltech.edu/cgi-bin/ZTF/nph_light_curves',params=params).prepare().url
 try:
  response=requests.get(url,timeout=60);response.raise_for_status();p.write_bytes(response.content);reader=csv.DictReader(io.StringIO(response.text));data=list(reader)
  assert {'oid','mjd','mag','magerr','catflags'}<=set(reader.fieldnames or []),response.text[:400]
  return {'tic':row['tic'],'status':'downloaded','path':str(p),'url':url,'sha256':sha(p),'n_rows':len(data),'columns':reader.fieldnames}
 except Exception as e:return {'tic':row['tic'],'status':'error','url':url,'error':repr(e)}
with ThreadPoolExecutor(max_workers=3) as pool:result=list(pool.map(get,plans))
save_json(out/'lightcurve-results.json',result);print(result)
