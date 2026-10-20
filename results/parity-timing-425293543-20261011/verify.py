from pathlib import Path
import json
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());p=read(out/'plan.json');m=read(out/'manifest.json');r=read(out/'results.json');c=read(out/'control.json')
assert p['script_sha256']==m['script_sha256']==sha(out/'run.py') and c['script_sha256']==sha(out/'control.py')
assert m['results_sha256']==sha(out/'results.json') and m['plot_sha256']==sha(out/'comparison.png')
assert p['joint_fits_sha256']==sha(Path('results/timing-425293543-20261011/fits.json'))
for d in r['data']:assert d['source']['sha256']==sha(Path(f"data/qlp/425293543-s{d['sector']:04d}.fits"))
assert sum(v['n_points'] for v in r['fits'])==sum(d['n_clean_points'] for d in r['data'])
assert all(not v['ranges']['search_boundary_hit'] for v in r['fits'])
save_json(out/'verification.json',{'script_sha256':sha(Path(__file__)),'manifest_sha256':sha(out/'manifest.json'),'control_sha256':sha(out/'control.json'),'visual_review':'All8panels inspected: both separately fitted deep eclipse sequences align in all4sectors.','limits':'Separate posthoc box fits, narrow formal profiles not calibrated timing precision. Supports near3.94363day binary hypothesis, no physical orbital solution or unique-host confirmation. Deterministic control validates plumbing only.'})
print('Parity timing provenance and deterministic control verified.')
