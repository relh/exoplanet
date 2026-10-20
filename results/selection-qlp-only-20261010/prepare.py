"""Preselect an untouched target pool for QLP archive coverage queries only."""
from pathlib import Path
import json,csv
from collections import Counter
from exoplanet.targeting import fetch_small_stars
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent
stars,evidence=fetch_small_stars(Path('data/targeting'))
exclude=set();sources=[]
for p in [Path('results/selection-small-stars-20261009/eligible.json'),Path('results/selection-late-sectors-20261010/eligible.json')]:
 exclude.update(r['tic'] for r in json.loads(p.read_text()));sources.append({'path':str(p),'sha256':sha(p)})
for p in Path('data/lightcurves').glob('s*-*.fits'):
 try:exclude.add(int(p.stem.split('-')[1]))
 except ValueError:pass
for p in Path('data/qlp').glob('*-s*.fits'):
 try:exclude.add(int(p.stem.split('-s')[0]))
 except ValueError:pass
for name,key in [('toi','tid'),('confirmed','tic_id'),('ctoi','TIC ID'),('eb','tess_id')]:
 p=Path('results/selection-small-stars-20261009')/f'catalog_{name}.csv'
 exclude.update(int(r[key].replace('TIC','').strip()) for r in csv.DictReader(p.open()));sources.append({'path':str(p),'sha256':sha(p)})
for n in [3,4]:
 p=Path(f'data/catalogs/kostov2025-table{n}.csv');exclude.update(int(r['TIC']) for r in csv.DictReader(p.open()));sources.append({'path':str(p),'sha256':sha(p)})
p=Path('results/eb-catalog-refresh-20261010/villanova-parsed.json');exclude.update(r['tic'] for r in json.loads(p.read_text()));sources.append({'path':str(p),'sha256':sha(p)})
rows=[];counts=Counter()
for s in stars:
 tic=int(s['ID'])
 if tic in exclude:counts['excluded_known_or_opened_or_prior_scope']+=1;continue
 if str(s.get('disposition') or '').upper() in {'ARTIFACT','DUPLICATE','SPLIT'} or s.get('duplicate_id'):counts['tic_disposition']+=1;continue
 if s.get('contratio') is None or s['contratio']>.2:counts['crowding']+=1;continue
 if s.get('Teff') is None or s['Teff']>5300:counts['temperature']+=1;continue
 rows.append({'tic':tic,'star':s,'priority_noise_proxy':s['rad']**2*10**(.2*(s['Tmag']-10))})
rows.sort(key=lambda r:(r['priority_noise_proxy'],r['tic']))
save_json(out/'pool.json',rows);save_json(out/'query-targets.json',rows[:2000])
save_json(out/'plan.json',{'utc':now(),'tic_source':evidence,'exclusion_sources':sources,'excluded_ids':sorted(exclude),'n_pool':len(rows),'n_metadata_query_targets':min(2000,len(rows)),'exclusions':dict(counts),'rule':'Same small/nearby/cool/low-crowding TIC cuts. Exclude all prior selected/opened targets and exact catalog matches. Query QLP metadata for first2000 ranked by radius/brightness proxy before opening photometry. No claim that targets were not studied elsewhere. Later freeze adjacent training sectors and separate heldout sectors if QLP metadata makes them viable.','script_sha256':sha(Path(__file__))})
print('pool',len(rows),'query',min(2000,len(rows)),dict(counts))
