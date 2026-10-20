from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import csv
from exoplanet.pipeline import fetch,save_json,sha,TAP,QUERIES
out=Path(__file__).parent
queries={'toi':(TAP,{'query':QUERIES['toi']+' where tid=422626648','format':'csv'},'tid'),'confirmed':(TAP,{'query':"select tic_id,pl_name,pl_orbper from ps where tic_id='TIC 422626648'",'format':'csv'},'tic_id'),'ctoi':('https://exofop.ipac.caltech.edu/tess/download_ctoi.php?sort=ctoi&output=csv',None,'TIC ID'),'eb':('https://archive.stsci.edu/hlsps/tess-ebs/hlsp_tess-ebs_tess_lcf-ffi_s0001-s0026_tess_v1.0_cat.csv',None,'tess_id')}
def query(item):
 name,(url,params,key)=item;p=Path(f'data/catalogs/422626648-{name}-20261011.csv')
 try:
  source=fetch(url,p,params);reader=csv.DictReader(p.open());assert key in reader.fieldnames;rows=list(reader);matches=[r for r in rows if r[key].replace('TIC','').strip()=='422626648'];return {'catalog':name,'source':source,'n_rows':len(rows),'matches':matches,'status':'complete'}
 except Exception as e:return {'catalog':name,'status':'error','error':repr(e)}
with ThreadPoolExecutor(max_workers=4) as pool:rows=list(pool.map(query,queries.items()))
save_json(out/'results.json',{'script_sha256':sha(Path(__file__)),'rows':rows,'limits':'Exact TIC matches only; nonmatches do not establish novelty or exclude binaries. Archived EB list covers sectors1–26.'});print([(r['catalog'],r['status'],len(r.get('matches',[]))) for r in rows])
