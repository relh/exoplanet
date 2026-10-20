from pathlib import Path
import json,csv
from exoplanet.pipeline import sha,read_curve,save_json
p=Path(__file__).parent;r=json.loads((p/'discovery.json').read_text());src=Path('results/solar-radius-ranks2384-2896-20261011/targets/30832104.json');assert sha(src)==sha(p/'discovery.json');cat=json.loads((p/'results.json').read_text())[0];assert cat['status']=='success';raw=Path(cat['path']);assert sha(raw)==cat['sha256'];assert list(csv.DictReader(raw.open()))==cat['rows'];identity=json.loads((p/'identity.json').read_text());assert identity['status']=='success';raw=Path(identity['path']);assert sha(raw)==identity['source']['sha256'];assert list(csv.DictReader(raw.open()))==identity['rows'];ids={x['id'] for x in identity['rows']};assert {'TIC 30832104','Gaia DR3 5331325449778763776'}<=ids;assert len({x['main_id'] for x in identity['rows']})==1
for d in r['data']:
 raw=Path(f"data/lightcurves/s{d['sector']:04d}-30832104.fits");assert sha(raw)==d['source']['sha256'];_,_,_,star=read_curve(raw);assert star['ticid']==30832104 and star['sector']==d['sector']
f=json.loads(Path('results/refinement-30832104-20261011/frozen.json').read_text());assert f['discovery_sha256']==sha(src) and f['heldout_sectors']==[];assert not Path('data/lightcurves/s0062-30832104.fits').exists()
save_json(p/'verification.json',dict(status='passed',raw_discovery_products_checked=len(r['data']),catalog_and_identity_csv_hashes_checked=True,exact_target_gaia_identity=True,discovery_copy_matches_batch=True,refinement_discovery_hash_checked=True,reserved_cache_absent=True))
