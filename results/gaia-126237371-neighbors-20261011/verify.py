"""Verify catalog provenance without treating catalog nonmatches as exclusions."""
from pathlib import Path
import json
from exoplanet.pipeline import sha, save_json, now

out=Path(__file__).parent
read=lambda p:json.loads(p.read_text())
plan=read(out/'plan.json')
assert sha(Path('results/neighbors-126237371-20261011/neighbors.json'))==plan['neighbors_sha256']
for p,h in plan['image_analysis_hashes'].items():assert sha(Path(p))==h
inventory=[]
for table in ['dr2_neighbourhood','gaia_source','vari_classifier_result','vari_eclipsing_binary']:
    raw=Path(f'data/catalogs/gaia-126237371-neighbors-{table}-20261011.csv')
    source=read(out/f'{table}-source.json')
    assert sha(raw)==source['sha256'] and raw.stat().st_size==source['bytes']
    inventory.append({'table':table,'raw_sha256':sha(raw),'json_sha256':sha(out/f'{table}.json'),'source_sha256':sha(out/f'{table}-source.json')})
assert read(out/'vari_classifier_result.json')==[] and read(out/'vari_eclipsing_binary.json')==[]
assert len(read(out/'dr2_neighbourhood.json'))==2 and len(read(out/'gaia_source.json'))==2
save_json(out/'verification.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'inventory':inventory,'limits':'Target and proposed neighboring source mapped to DR3; no entries in the two queried variability tables. Not an exclusion of variability or proof of novelty.'})
print('Verified Gaia provenance and explicit catalog nonmatches')
