"""Extend to fainter small nearby stars; freeze metadata pool before photometry."""
from pathlib import Path
from collections import Counter
import json,csv
from exoplanet.archive import mast_query
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent;assert not (out/'pool.json').exists()
assert json.loads((out/'split-run.json').read_text())['n_errors']==0
stars=json.loads((out/'catalog-rows.json').read_text());meta=json.loads((out/'catalog-sources.json').read_text())
assert len({r['ID'] for r in stars})==len(stars)
exclude=set();sources=[]
for name,key in [('toi','tid'),('confirmed','tic_id'),('ctoi','TIC ID'),('eb','tess_id')]:
 p=Path('results/selection-small-stars-20261009')/f'catalog_{name}.csv';exclude.update(int(r[key].replace('TIC','').strip()) for r in csv.DictReader(p.open()));sources.append({'path':str(p),'sha256':sha(p)})
for family,numbers in [('kostov2025',[3,4]),('dtarps-2024',[1,4])]:
 for n in numbers:
  p=Path(f'data/catalogs/{family}-table{n}.csv');exclude.update(int(r['TIC']) for r in csv.DictReader(p.open()));sources.append({'path':str(p),'sha256':sha(p)})
p=Path('results/eb-catalog-refresh-20261010/villanova-parsed.json');exclude.update(int(r['tic']) for r in json.loads(p.read_text()));sources.append({'path':str(p),'sha256':sha(p)})
for p in Path('data/qlp').glob('*-s*.fits'):exclude.add(int(p.stem.split('-s')[0]))
for p in Path('data/lightcurves').glob('s*-*.fits'):exclude.add(int(p.stem.split('-')[1]))
rows=[];counts=Counter()
for s in stars:
 assert .15<=s['rad']<=.5 and 12<=s['Tmag']<=13.5 and 0<=s['d']<=120
 tic=int(s['ID'])
 if s['Tmag']<=12:counts['original_brightness_boundary']+=1;continue
 if tic in exclude:counts['known_or_opened']+=1;continue
 if s.get('duplicate_id') or str(s.get('disposition') or '').upper() in {'ARTIFACT','DUPLICATE','SPLIT'}:counts['tic_disposition']+=1;continue
 if s.get('contratio') is None or s['contratio']>.2:counts['crowding']+=1;continue
 if s.get('Teff') is None or s['Teff']>4000:counts['temperature']+=1;continue
 rows.append({'tic':tic,'star':s,'priority_noise_proxy':s['rad']**2*10**(.2*(s['Tmag']-10))})
rows.sort(key=lambda r:(r['priority_noise_proxy'],r['tic']));save_json(out/'pool.json',rows)
save_json(out/'plan.json',{'utc':now(),'n_catalog_rows':len(stars),'n_pool':len(rows),'counts':dict(counts),'exclusion_sources':sources,'excluded_ids':sorted(exclude),'script_sha256':sha(Path(__file__)),'catalog_sources_sha256':sha(out/'catalog-sources.json'),'policy':'Metadata only. Radius/brightness proxy is not measured quietness or completeness. Exclude exact dated catalog IDs and already-opened raw light-curve IDs; nonmatches do not establish novelty. Query QLP coverage next and freeze separate discovery/reserved epochs before downloading photometry.'})
print(len(stars),'catalog',len(rows),'pool',dict(counts),flush=True)
