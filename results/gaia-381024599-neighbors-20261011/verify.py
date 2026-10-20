"""Verify catalog provenance without treating catalog nonmatches as exclusions."""
from pathlib import Path
import json
from exoplanet.pipeline import sha, save_json, now

out=Path(__file__).parent
read=lambda p:json.loads(p.read_text())
plan=read(out/'plan.json')
assert sha(Path('results/neighbors-381024599-20261011/neighbors.json'))==plan['neighbors_sha256']
for p,h in plan['image_analysis_hashes'].items():assert sha(Path(p))==h
inventory=[]
for table in ['dr2_neighbourhood','gaia_source','vari_classifier_result','vari_eclipsing_binary']:
    raw=Path(f'data/catalogs/gaia-381024599-neighbors-{table}-20261011.csv')
    source=read(out/f'{table}-source.json')
    assert sha(raw)==source['sha256'] and raw.stat().st_size==source['bytes']
    inventory.append({'table':table,'raw_sha256':sha(raw),'json_sha256':sha(out/f'{table}.json'),'source_sha256':sha(out/f'{table}-source.json')})
classes=read(out/'vari_classifier_result.json')
assert len(classes)==2
assert any(r['source_id']=='19447818074802816' and r['best_class_name']=='RS' for r in classes)
assert any(r['source_id']=='19447783715197952' and r['best_class_name']=='SOLAR_LIKE' for r in classes)
assert len(read(out/'vari_eclipsing_binary.json'))==0
assert len(read(out/'dr2_neighbourhood.json'))==3 and len(read(out/'gaia_source.json'))==3
save_json(out/'verification.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'inventory':inventory,'limits':'Target and two neighbors mapped to three DR3 sources; target SOLAR_LIKE and TIC381024603 RS classifier labels, no eclipsing-binary rows. Classifier scores are retained and not posterior probabilities or confirmation of the source/period. Not an exclusion of variability or proof of novelty.'})
print('Verified Gaia provenance and catalog evidence')
