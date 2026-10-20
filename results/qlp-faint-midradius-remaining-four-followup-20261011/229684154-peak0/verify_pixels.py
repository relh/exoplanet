"""Verify the frozen-source diagnostics without converting moments into hosts."""
from pathlib import Path
import json
from exoplanet.pipeline import sha,save_json,now
out=Path(__file__).parent
read=lambda p:json.loads(p.read_text())
np=Path('results/neighbors-229684154-20261011/neighbors.json')
rows=[]
for sector in [84,85,86]:
    folder=Path(f'results/tesscut-229684154-s{sector}-20261011')
    files=read(folder/'files.json');assert len(files)==1
    assert sha(Path(files[0]['path']))==files[0]['sha256']
    a=read(folder/'analysis.json')
    if sector in [84,85]:
        assert a['fit_sha256']==sha(out/'frozen.json') and a['neighbor_sha256']==sha(np)
        plot=folder/'difference.png';nevents=a['n_events']
        review='Entirely negative broad residual; no dimming-source localization.' if sector==84 else 'Broad positive and patchy residual; no repeatable compact stellar source established.'
        quality=Path(f'results/spoc-quality-229684154-s{sector}-20261011/quality.json')
        q=read(quality);raw=Path(f'data/lightcurves/s{sector:04d}-229684154.fits')
        assert q['source_sha256']==sha(raw) and q['frozen_sha256']==sha(out/'frozen.json')
    else:
        assert len(a['rows'])==1
        r=a['rows'][0];assert r['frozen_sha256']==sha(out/'frozen.json') and r['pixel_sha256']==files[0]['sha256']
        plot=folder/r['plot'];nevents=1
        review='Single-event map: broad positive field-wide change; insufficient to establish a stellar dimming source or repeatability.'
    rows.append({'sector':sector,'raw_sha256':files[0]['sha256'],'analysis_sha256':sha(folder/'analysis.json'),'plot_sha256':sha(plot),'n_events':nevents,'visual_review':review})
save_json(out/'source_review.json',{'utc':now(),'script_sha256':sha(Path(__file__)),
    'frozen_sha256':sha(out/'frozen.json'),'neighbors_sha256':sha(np),'rows':rows,
    'sector86_processed_error_sha256':sha(Path('results/spoc-quality-229684154-s86-20261011/error.json')),
    'limits':'All three plots inspected. Formal pixel SNR and image moments are not calibrated localization. Sector86 processed product unavailable at requested URL; retained as missing evidence, not a nondetection.'})
print('Verified three raw-image checks and two processed quality products')
