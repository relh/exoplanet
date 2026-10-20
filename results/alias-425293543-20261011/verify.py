from pathlib import Path
import json
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());p=read(out/'plan.json');m=read(out/'manifest.json');r=read(out/'results.json')
assert p['script_sha256']==m['script_sha256']==sha(out/'run.py')
assert p['joint_fits_sha256']==sha(Path('results/timing-425293543-20261011/fits.json'))
assert m['results_sha256']==sha(out/'results.json') and m['plot_sha256']==sha(out/'diagnostics.png')
assert [v['sector'] for v in r]==[53,54,80,81]
for row in r:
 for d in row['data']:assert d['source']['sha256']==sha(Path(f"data/qlp/425293543-s{row['sector']:04d}.fits"))
 assert len(row['even_odd'])==2 and all(v['total'] is not None for v in row['even_odd'])
save_json(out/'verification.json',{'script_sha256':sha(Path(__file__)),'manifest_sha256':sha(out/'manifest.json'),'visual_review':'All8panels inspected: deep rounded eclipses, alternating parity curves offset in time on opposite sides of joint center in all4sectors; depth difference less consistent. Full-orbit panels show no comparably deep additional eclipse away from primary.','limits':'Posthoc evidence favors testing doubled-period eclipsing interpretation, but no formal timing fit or unique host/physical classification. Secondary maxima selected and uncalibrated; no exclusion of faint secondary.','doubled_period_hypothesis_days':2*p['best']['period']})
print('Alias diagnostic inputs and outputs verified.')
