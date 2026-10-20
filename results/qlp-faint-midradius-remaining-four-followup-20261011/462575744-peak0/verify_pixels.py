"""Retain provenance and explicit visual limits for the two raw-image checks."""
from pathlib import Path
import json
from exoplanet.pipeline import sha,save_json,now
out=Path(__file__).parent
neighbors=Path('results/neighbors-462575744-20261011/neighbors.json')
rows=[]
for sector in [74,75]:
    folder=Path(f'results/tesscut-462575744-s{sector}-20261011')
    p=folder/'analysis.json';d=json.loads(p.read_text())
    assert sha(Path(d['source']['path']))==d['source']['sha256']
    assert d['fit_sha256']==sha(out/'frozen.json') and d['neighbor_sha256']==sha(neighbors)
    rows.append({'sector':sector,'analysis_sha256':sha(p),'raw_sha256':d['source']['sha256'],
        'plot_sha256':sha(folder/'difference.png'),'n_events':d['n_events'],
        'visual_review':'Inspected: broadly positive, spatially varying background residual. No repeatable compact dimming source established. Peak-pixel SNR and moments are not source localization or calibrated confidence.'})
save_json(out/'pixel_verification.json',{'utc':now(),'script_sha256':sha(Path(__file__)),
    'frozen_sha256':sha(out/'frozen.json'),'neighbor_sha256':sha(neighbors),'rows':rows})
print('Verified two raw-image analyses; both plots reviewed as nonlocalizing')
