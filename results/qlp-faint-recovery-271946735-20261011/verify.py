from pathlib import Path
import json
from exoplanet.pipeline import sha,save_json,now
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());plan=read(out/'plan.json');checks=read(out/'sector-checks.json')
assert sha(Path(plan['original_path']))==plan['original_sha256'] and sha(out/'run.py')==plan['script_sha256']
assert read(out/'selection.json')['usable_sectors']==[] and read(out/'result.json')['status']=='insufficient_training_coverage'
assert {r['sector'] for r in checks}=={99,100,101} and all(r['status']=='error' for r in checks)
for r in checks:assert sha(Path(f"data/qlp/271946735-s{r['sector']:04d}.fits"))==r['raw_sha256']==r['download_provenance']['sha256']
assert all(not Path(f'data/qlp/271946735-s{s:04d}.fits').exists() for s in plan['target']['heldout_sectors'])
save_json(out/'verification.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'sector_checks_sha256':sha(out/'sector-checks.json'),'result_sha256':sha(out/'result.json'),'limits':'No usable assigned sector; no alternate period search. Failures are not nondetections; reserved epochs remain unopened.'})
print('Verified insufficient training coverage and reserved-data absence.')
