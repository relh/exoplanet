from pathlib import Path
import json,csv
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());plan=read(out/'plan.json');ids={str(int(t['GAIA'])) for t in plan['targets'] if t.get('GAIA') is not None}
for table in ['dr2_neighbourhood','gaia_source','vari_classifier_result','vari_eclipsing_binary']:
 p=Path(f'data/catalogs/gaia-402358350-scene-{table}-20261011.csv');assert sha(p)==read(out/f'{table}-source.json')['sha256'];assert list(csv.DictReader(p.open()))==read(out/f'{table}.json')
assert sha(Path('results/neighbors-402358350-20261011/neighbors.json'))==plan['neighbors_sha256']
assert sha(out/'query.py')==plan['script_sha256']
for p,h in plan['image_analysis_hashes'].items():assert sha(Path(p))==h
m=read(out/'dr2_neighbourhood.json');assert all(r['dr2_source_id'] in ids for r in m);mapped={r['dr3_source_id'] for r in m};sources=read(out/'gaia_source.json');assert {r['source_id'] for r in sources}==mapped
assert all(r['source_id'] in mapped for table in ['vari_classifier_result','vari_eclipsing_binary'] for r in read(out/f'{table}.json'))
save_json(out/'verification.json',{'script_sha256':sha(Path(__file__)),'n_tic':len(plan['targets']),'n_dr2':len(ids),'n_mappings':len(m),'n_dr3':len(mapped),'status':'CSV/JSON hashes and all returned DR2/DR3 identities reconciled. Variability rows checked for mapped identities; classifications do not establish the TESS source, absence does not exclude variability.'});print(len(ids),len(m),len(mapped))

meta=read(out/'metadata.json');assert sha(Path(meta['path']))==meta['source']['sha256'];assert list(csv.DictReader(Path(meta['path']).open()))==meta['rows'];assert meta['rows'][0]['unit']=='mas'
vsx=read(Path('results/review-402358350-20261011/results.json'))[0];assert sha(Path(vsx['path']))==vsx['sha256'];assert list(csv.DictReader(Path(vsx['path']).open()))==vsx['rows'];v=vsx['rows'][0];assert v['Name'].strip()=='Gaia DR3 4318716236117290496'
classifier=read(out/'vari_classifier_result.json');assert len(classifier)==1 and classifier[0]['source_id']=='4318716236117290496' and classifier[0]['best_class_name']==v['Type'].strip()
assert not read(out/'vari_eclipsing_binary.json')
assert any(t['ID']==402358249 and t['GAIA']=='4318716236117290496' for t in plan['targets'])
save_json(out/'additional-verification.json',{'script_sha256':sha(Path(__file__)),'status':'passed','scope':'Gaia metadata units and prior raw VSX response hash/CSV/class identity reconciled; binary result is an empty successful query, not binary exclusion.'})
