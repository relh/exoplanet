from pathlib import Path
import json,csv
from exoplanet.pipeline import sha,read_curve,save_json,now
p=Path(__file__).parent;src=Path('results/solar-radius-ranks4432-4944-20261011/targets/322826591.json');assert sha(src)==sha(p/'discovery.json');r=json.loads(src.read_text());assert r['screened_peaks'][0]['flags']==[]
for d in r['data']:
 raw=Path(f"data/lightcurves/s{d['sector']:04d}-322826591.fits");assert sha(raw)==d['source']['sha256'];*_,s=read_curve(raw);assert s['ticid']==322826591 and s['sector']==d['sector']
for filename in ['results.json','identity.json']:
 for entry in json.loads((p/filename).read_text()):
  assert entry['status']=='success' and sha(Path(entry['path']))==entry['sha256'];assert list(csv.DictReader(Path(entry['path']).open()))==entry['rows']
ids={x['id'] for x in json.loads((p/'identity.json').read_text())[0]['rows']};assert {'TIC 322826591','Gaia DR3 5332801170510042880'}<=ids
assert not Path('data/lightcurves/s0064-322826591.fits').exists()
save_json(p/'verification.json',dict(status='passed',verified_utc=now(),n_discovery_products=2,catalog_hashes_and_exact_tic_gaia_identity_checked=True,reserved_unopened=True,limits='Record and raw-data integrity, not a rerun of global discovery or proof of novelty. Main batch still running when review began.'))
