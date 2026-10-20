from pathlib import Path
import json,csv
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());r=read(out/'results.json');g=Path('results/gaia-429034844-scene-20261011')
for p,h in r['inputs'].items():assert sha(Path(p))==h
assert r['script_sha256']==sha(out/'run.py')
for table in ['gaia_source','dr2_neighbourhood']:
 raw=Path(f'data/catalogs/gaia-429034844-scene-{table}-20261011.csv');assert sha(raw)==read(g/f'{table}-source.json')['sha256']
 assert list(csv.DictReader(raw.open()))==read(g/f'{table}.json')
f=r['fields'];assert f['source_id']=='2750531317313142528' and len(r['mapping'])==1
assert f['rv_nb_transits']=='22' and f['rv_nb_deblended_transits']=='19'
assert float(f['rv_chisq_pvalue'])<.01 and float(f['rv_renormalised_gof'])>4 and int(f['rv_nb_transits'])>=10
assert 3900<=float(f['rv_template_teff'])<=8000 and all(r['rv_variability_cuts'].values()) and r['passes_all']
assert f['has_epoch_rv']=='false'
doc=Path('data/literature/gaia-dr3-source-rv-429034844.html');assert sha(doc)==read(out/'documentation-source.json')['sha256']
assert all(k in doc.read_text() for k in ['rv_amplitude_robust','rv_nb_deblended_transits','rv_chisq_pvalue'])
save_json(out/'verification.json',{'script_sha256':sha(Path(__file__)),'artifacts':{str(p):sha(p) for p in [out/'run.py',out/'results.json',out/'documentation-source.json',out/'ASSESSMENT.md']},'status':'Raw CSV/JSON equality, source identity/mapping, RV variability cuts, epoch availability and documentation hash verified. Not orbital or binary validation.'})
print('Verified RV context and provenance.')
