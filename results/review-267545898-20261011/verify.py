from pathlib import Path
import json,csv,io
from exoplanet.pipeline import sha,read_curve,save_json
p=Path(__file__).parent;r=json.loads((p/'results.json').read_text())[0];d=json.loads((p/'discovery.json').read_text())
assert r['status']=='success' and sha(Path(r['path']))==r['sha256']
assert list(csv.DictReader(io.StringIO(Path(r['path']).read_text())))==r['rows']==[]
for item in d['data']:
 raw=Path(f"data/lightcurves/s{item['sector']:04d}-267545898.fits")
 assert sha(raw)==item['source']['sha256']
 _,_,_,star=read_curve(raw);assert star['ticid']==267545898 and star['sector']==item['sector']
assert not Path('data/lightcurves/s0068-267545898.fits').exists()
assert sha(p/'discovery.json')==sha(Path('results/solar-radius-ranks1872-2384-20261011/targets/267545898.json'))
save_json(p/'verification.json',dict(status='passed',training_products_checked=len(d['data']),catalog_hash_checked=True,copied_discovery_matches_campaign=True,reserved_cache_absent=True))
