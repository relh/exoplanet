"""Check retained source evidence and compare moments across two epochs."""
from pathlib import Path
import json
from astropy.coordinates import SkyCoord
from exoplanet.pipeline import sha, save_json, now

out = Path(__file__).parent
old = Path('results/tesscut-438792601-s99-20261011/analysis.json')
new = out/'analysis.json'
a, b = [json.loads(p.read_text()) for p in (old, new)]
fit = Path('results/qlp-faint-midradius-four-pilot-followup-20261011/438792601-peak0/frozen.json')
neighbors = Path('results/neighbors-438792601-20261011/neighbors.json')
for row in (a, b):
    assert sha(Path(row['source']['path'])) == row['source']['sha256']
    assert row['fit_sha256'] == sha(fit)
    assert row['neighbor_sha256'] == sha(neighbors)
sep = SkyCoord(*a['difference_sky'], unit='deg').separation(SkyCoord(*b['difference_sky'], unit='deg')).arcsec
save_json(out/'verification.json', {
    'utc': now(), 'script_sha256': sha(Path(__file__)),
    'analysis_sha256': sha(new), 'prior_analysis_sha256': sha(old),
    'raw_sha256': b['source']['sha256'], 'frozen_sha256': sha(fit),
    'neighbor_sha256': sha(neighbors), 'plot_sha256': sha(out/'difference.png'),
    'moment_separation_arcsec': float(sep),
    'plot_review': 'Inspected: compact positive residual visibly displaced from target. Both epoch moments lie near the same faint blended group. No exact variable identification or calibrated astrometric confidence.',
})
print('Verified raw and frozen-input hashes; moment separation arcsec:', sep)
