from pathlib import Path
import json
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;base=Path('results/qlp-faint-midradius-one-reserved-pilot-20261011');read=lambda p:json.loads(p.read_text());s=read(out/'selection.json');t=read(out/'selected.json');p=read(out/'plan.json')
assert sha(base/'eligible.json')==s['source_sha256'] and sha(base/'selected.json')==s['pilot_sha256'] and sha(base/'verification.json')==s['pilot_verification_sha256']
assert read(base/'eligible.json')[16:]==t==p['targets'] and len(t)==2810 and len({r['tic'] for r in t})==2810
assert sha(out/'selected.json')==s['selected_sha256']==p['source_sha256'] and sha(out/'freeze.py')==s['script_sha256'] and sha(out/'run.py')==p['script_sha256']
for name,h in p['source_hashes'].items():assert sha(Path('src/exoplanet')/name)==h
for r in t:
 assert len(r['training_sectors'])==len(r['heldout_sectors'])==1 and abs(r['training_sectors'][0]-r['heldout_sectors'][0])>=8
for suffix in ['followup','coverage-followup']:
 d=Path(f'results/qlp-faint-midradius-one-reserved-remaining-{suffix}-20261011');fp=read(d/'plan.json');assert fp['campaign_run_sha256_at_start']==sha(out/'plan.json');assert 'max_sectors=1' in (d/'watch.py').read_text()
save_json(out/'selection-verification.json',{'script_sha256':sha(Path(__file__)),'selected_sha256':sha(out/'selected.json'),'plan_sha256':sha(out/'plan.json'),'status':'All2810 frozen identities/slice, one discovery and one distant reserved sector, pipeline source hashes and follow-up campaign identity verified. Pre-run cache absence recorded by freeze.py; no claim that currently eligible opened follow-ups remain blind.'});print('Verified2810 frozen targets and one-reserved policy.')
