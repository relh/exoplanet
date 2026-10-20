from pathlib import Path
import json,csv
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());plan=read(out/'plan.json');ids={str(int(t['GAIA'])) for t in plan['targets'] if t.get('GAIA') is not None}
for table in ['dr2_neighbourhood','gaia_source','vari_classifier_result','vari_eclipsing_binary']:
 p=Path(f'data/catalogs/gaia-322826591-scene-{table}-20261011.csv');assert sha(p)==read(out/f'{table}-source.json')['sha256'];assert list(csv.DictReader(p.open()))==read(out/f'{table}.json')
m=read(out/'dr2_neighbourhood.json');assert all(r['dr2_source_id'] in ids for r in m);mapped={r['dr3_source_id'] for r in m};sources=read(out/'gaia_source.json');assert {r['source_id'] for r in sources}==mapped
assert all(r['source_id'] in mapped for table in ['vari_classifier_result','vari_eclipsing_binary'] for r in read(out/f'{table}.json'))
save_json(out/'verification.json',{'script_sha256':sha(Path(__file__)),'n_tic':len(plan['targets']),'n_dr2':len(ids),'n_mappings':len(m),'n_dr3':len(mapped),'status':'CSV/JSON hashes and all returned DR2/DR3 identities reconciled. Variability rows checked for mapped identities; classifications do not establish the TESS source, absence does not exclude variability.'});print(len(ids),len(m),len(mapped))
