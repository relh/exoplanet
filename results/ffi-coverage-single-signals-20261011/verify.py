from pathlib import Path
import json
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());r=read(out/'results.json');assert sha(out/'run.py')==r['script_sha256'];assert len(r['rows'])==3
for row in r['rows']:
 tic=row['tic'];p=out/f'{tic}.json';assert row['status']=='complete' and sha(p)==row['source']['sha256'];assert read(p)['results']==row['rows'];dp=Path(f'results/qlp-faint-midradius-single-remaining-20261011/targets/{tic}.json');assert sha(dp)==row['discovery_sha256'];target=read(dp)['target'];assert row['params']=={'ra':target['star']['ra'],'dec':target['star']['dec']};assert row['sectors']==target['training_sectors'] and row['additional_sectors']==[]
save_json(out/'verification.json',{'script_sha256':sha(Path(__file__)),'results_sha256':sha(out/'results.json'),'status':'All three request coordinates, response hashes and sole returned sectors verified. No claim about other missions, products or future coverage.'})
