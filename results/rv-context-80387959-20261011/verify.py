from pathlib import Path
import json,csv
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());request=read(out/'request.json');r=read(out/'results.json')
assert request['script_sha256']==sha(out/'run.py')
for p,h in request['inputs'].items():assert sha(Path(p))==h
raw=Path('data/catalogs/rv-80387959-dr2-neighbourhood.csv');assert sha(raw)==read(out/'mapping-source.json')['sha256'];assert list(csv.DictReader(raw.open()))==read(out/'mapping.json')
source=list(csv.DictReader(Path('results/gaia-80387959-20261009/gaia_source.csv').open()))
assert len(r['rows'])==4
for row in r['rows']:
 match=next(s for s in source if s['source_id']==row['mapping']['dr3_source_id'])
 for k,v in row['fields'].items():assert v==(match[k] or None)
 if row['tic']==80387959:
  assert row['status']=='does_not_pass_variability_cuts' and not row['variability_cuts']['p_lt_0_01'] and not row['variability_cuts']['gof_gt_4'] and row['variability_cuts']['n_ge_10']
 else:assert row['status']=='diagnostic_unavailable' and row['variability_cuts'] is None
 assert row['fields']['has_epoch_rv']=='false' and row['fields']['has_rvs']=='false'
save_json(out/'verification.json',{'script_sha256':sha(Path(__file__)),'artifacts':{str(p):sha(p) for p in out.iterdir() if p.is_file() and p.name!='verification.json'},'status':'Input hashes, raw mapping CSV, four unique identities, exact source-field extraction and available/missing diagnostic distinction checked. Not companion exclusion or host validation.'});print('Verified RV context for four host hypotheses.')
