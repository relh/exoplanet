from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import csv,json
from exoplanet.pipeline import fetch,save_json,sha,now
out=Path(__file__).parent

def get(n):
 p=Path(f'data/catalogs/dtarps-2024-table{n}.csv');m=fetch('https://tapvizier.cds.unistra.fr/TAPVizieR/tap/sync',p,{'REQUEST':'doQuery','LANG':'ADQL','FORMAT':'csv','QUERY':f'SELECT * FROM "J/AJ/167/203/table{n}"'})
 save_json(out/f'dtarps-table{n}-source.json',m)
 rows=list(csv.DictReader(p.open()));assert len(rows)=={1:462,4:310}[n]
 print('DTARPS',n,'columns',list(rows[0]),flush=True)
 for r in rows:
  if r.get('TIC') in ['296179330','378761120']:print('DTARPS match',r,flush=True)
 return p,rows
with ThreadPoolExecutor(max_workers=2) as ex:dt=list(ex.map(get,[1,4]))
catalogs=[]
for name,key in [('toi','tid'),('confirmed','tic_id'),('ctoi','TIC ID'),('eb','tess_id')]:
 p=Path('results/selection-small-stars-20261009')/f'catalog_{name}.csv';catalogs.append((name,p,key,list(csv.DictReader(p.open()))))
for n in [3,4]:
 p=Path(f'data/catalogs/kostov2025-table{n}.csv');catalogs.append((f'Kostov2025-{n}',p,'TIC',list(csv.DictReader(p.open()))))
p=Path('results/eb-catalog-refresh-20261010/villanova-parsed.json');catalogs.append(('Villanova',p,'tic',json.loads(p.read_text())))
for p,rows in dt:catalogs.append((p.stem,p,'TIC',rows))
results=[]
for tic in [378761120,296179330]:
 p=out/f'{tic}-neighbors.json';neighbors=json.loads(p.read_text());ids={int(r['ID']) for r in neighbors};matches=[]
 for name,source,key,rows in catalogs:
  for row in rows:
   raw=row.get(key)
   if raw is None:raise ValueError(f'Missing {key} in {name}')
   value=int(str(raw).replace('TIC','').strip())
   if value in ids:matches.append({'catalog':name,'tic':value,'exact_target':value==tic,'row':row})
 results.append({'tic':tic,'neighbors_sha256':sha(p),'n_neighbors':len(ids),'matches':matches})
save_json(out/'catalog-matches.json',{'utc':now(),'catalogs':[{'name':n,'path':str(p),'sha256':sha(p)} for n,p,_,_ in catalogs],'results':results,'limits':'Exact TIC matching across216arcsec neighbor cone. Absence does not establish novelty, exclude unlisted binaries, or fix alias/proper-motion mismatches.'})
for r in results:print(r['tic'],[(m['catalog'],m['tic'],m['exact_target']) for m in r['matches']],flush=True)
