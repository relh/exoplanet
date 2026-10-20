"""Verify catalog provenance without treating catalog nonmatches as exclusions."""
from pathlib import Path
import json
from exoplanet.pipeline import sha, save_json, now

out=Path(__file__).parent
read=lambda p:json.loads(p.read_text())
plan=read(out/'plan.json')
assert sha(Path('results/neighbors-429294074-20261011/neighbors.json'))==plan['neighbors_sha256']
for p,h in plan['image_analysis_hashes'].items():assert sha(Path(p))==h
inventory=[]
for table in ['dr2_neighbourhood','gaia_source','vari_classifier_result','vari_eclipsing_binary']:
    raw=Path(f'data/catalogs/gaia-429294074-neighbors-{table}-20261011.csv')
    source=read(out/f'{table}-source.json')
    assert sha(raw)==source['sha256'] and raw.stat().st_size==source['bytes']
    inventory.append({'table':table,'raw_sha256':sha(raw),'json_sha256':sha(out/f'{table}.json'),'source_sha256':sha(out/f'{table}-source.json')})
assert len(read(out/'vari_classifier_result.json'))==1
eb=read(out/'vari_eclipsing_binary.json');assert len(eb)==1 and eb[0]['source_id']=='6125563343462988160'
assert any(r['dr2_source_id']=='6125563343462988160' and r['dr3_source_id']==eb[0]['source_id'] for r in read(out/'dr2_neighbourhood.json'))
assert len(read(out/'dr2_neighbourhood.json'))==33 and len(read(out/'gaia_source.json'))==31
comparison=read(out/'period-comparison.json')
frozen=Path('results/qlp-faint-midradius-remaining-three-followup-20261011/429294074-peak1/frozen.json')
assert comparison['frozen_sha256']==sha(frozen) and comparison['eb_sha256']==sha(out/'vari_eclipsing_binary.json')
period=read(frozen)['best']['period'];catalog_period=1/float(eb[0]['frequency'])
assert comparison['qlp_period_days']==period and comparison['gaia_period_days']==catalog_period
assert comparison['half_minus_third_seconds']==(catalog_period/2-period/3)*86400
save_json(out/'verification.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'inventory':inventory,'limits':'All31catalog entries within42arcsec yielded33mapping rows and31uniqueDR3 sources, with two distant crosslinks retained; one ECL/EB TIC429294064 period0.989860779days. Half-period close to QLPperiod/3; not a calibrated joint source confidence. Not an exclusion of variability or proof of novelty.'})
print('Verified Gaia provenance and catalog evidence')
