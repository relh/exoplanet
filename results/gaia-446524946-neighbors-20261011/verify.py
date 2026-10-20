"""Verify catalog provenance without treating catalog nonmatches as exclusions."""
from pathlib import Path
import json
from exoplanet.pipeline import sha, save_json, now

out=Path(__file__).parent
read=lambda p:json.loads(p.read_text())
plan=read(out/'plan.json')
assert sha(Path('results/neighbors-446524946-20261011/neighbors.json'))==plan['neighbors_sha256']
for p,h in plan['image_analysis_hashes'].items():assert sha(Path(p))==h
inventory=[]
for table in ['dr2_neighbourhood','gaia_source','vari_classifier_result','vari_eclipsing_binary']:
    raw=Path(f'data/catalogs/gaia-446524946-neighbors-{table}-20261011.csv')
    source=read(out/f'{table}-source.json')
    assert sha(raw)==source['sha256'] and raw.stat().st_size==source['bytes']
    inventory.append({'table':table,'raw_sha256':sha(raw),'json_sha256':sha(out/f'{table}.json'),'source_sha256':sha(out/f'{table}-source.json')})
assert len(read(out/'vari_classifier_result.json'))==1
eb=read(out/'vari_eclipsing_binary.json');assert len(eb)==1 and eb[0]['source_id']=='5357965212082497280'
assert any(r['dr2_source_id']=='5357965212082497280' and r['dr3_source_id']==eb[0]['source_id'] for r in read(out/'dr2_neighbourhood.json'))
assert len(read(out/'dr2_neighbourhood.json'))==14 and len(read(out/'gaia_source.json'))==12
save_json(out/'verification.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'inventory':inventory,'limits':'Target and neighboring-group sources mapped to DR3; one eclipsing-binary classifier for TIC446692470 at period2.229088455days. Not an exclusion of variability or proof of novelty.'})
print('Verified Gaia provenance and catalog evidence')
