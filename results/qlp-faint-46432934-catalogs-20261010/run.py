"""Exact TIC crossmatch of the complete preexisting neighbor cone against dated snapshots."""
from pathlib import Path
import csv,json
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent
neighbors=Path('results/neighbors-46432934-20261010/neighbors.json')
rows=json.loads(neighbors.read_text());ids={int(r['ID']) for r in rows}
assert 46432934 in ids and len(ids)==102
catalogs=[]
for name,key in [('toi','tid'),('confirmed','tic_id'),('ctoi','TIC ID'),('eb','tess_id')]:
 p=Path('results/selection-small-stars-20261009')/f'catalog_{name}.csv';catalogs.append((name,p,key,list(csv.DictReader(p.open()))))
for n in [3,4]:
 p=Path(f'data/catalogs/kostov2025-table{n}.csv');catalogs.append((f'Kostov2025-{n}',p,'TIC',list(csv.DictReader(p.open()))))
p=Path('results/eb-catalog-refresh-20261010/villanova-parsed.json');catalogs.append(('Villanova',p,'tic',json.loads(p.read_text())))
for n in [1,4]:
 p=Path(f'data/catalogs/dtarps-2024-table{n}.csv');r=list(csv.DictReader(p.open()));assert len(r)=={1:462,4:310}[n];catalogs.append((f'DTARPS-{n}',p,'TIC',r))
matches=[]
for name,p,key,rs in catalogs:
 for r in rs:
  raw=r.get(key)
  if raw is None:raise ValueError(f'Missing {key} in {name}')
  tic=int(str(raw).replace('TIC','').strip())
  if tic in ids:matches.append({'catalog':name,'tic':tic,'row':r})
result={'utc':now(),'script_sha256':sha(Path(__file__)),'neighbors_path':str(neighbors),'neighbors_sha256':sha(neighbors),'n_neighbors':len(ids),'catalogs':[{'name':n,'path':str(p),'sha256':sha(p),'n_rows':len(rs)} for n,p,_,rs in catalogs],'matches':matches,'limits':'Exact TIC matches in the complete preexisting 180-arcsec cone around TIC46432934. Uses dated local snapshots, not a fresh remote catalog refresh. Nonmatches do not prove novelty, exclude unlisted binaries or alias identifiers, or establish host attribution. No positional/proper-motion crossmatch.'}
save_json(out/'results.json',result)
print('catalogs',len(catalogs),'neighbors',len(ids),'matches',[(m['catalog'],m['tic']) for m in matches])
