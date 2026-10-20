"""Verify immutable raw-image diagnostics and retain missing products."""
from pathlib import Path
import json
from exoplanet.pipeline import sha,save_json,now
out=Path(__file__).parent
read=lambda p:json.loads(p.read_text())
np=Path('results/neighbors-355707138-20261011/neighbors.json')
rows=[]
for sector in [102,103]:
    folder=Path(f'results/tesscut-355707138-s{sector}-20261011')
    files=read(folder/'files.json');assert len(files)==1
    assert sha(Path(files[0]['path']))==files[0]['sha256']
    a=read(folder/'analysis.json')
    assert a['script_sha256']==sha(folder/'analyze.py')
    if sector==102:
        assert a['fit_sha256']==sha(out/'frozen.json') and a['neighbor_sha256']==sha(np)
        assert a['n_events']==2
        plot=folder/'difference.png';nevents=2
        review='Weak positive residual near target and close neighbor; formal peak 3.21 and moment offset 0.27 pixel do not establish host localization.'
    else:
        assert len(a['rows'])==1
        r=a['rows'][0];assert r['frozen_sha256']==sha(out/'frozen.json') and r['pixel_sha256']==files[0]['sha256']
        plot=folder/r['plot'];nevents=1
        review='Single-event map has a negative target-area residual adjacent to positive structure, without repetition of a compact target dip. Not a calibrated exclusion.'
    qfolder=Path(f'results/spoc-quality-355707138-s{sector}-20261011')
    err=read(qfolder/'error.json');assert err['script_sha256']==sha(qfolder/'run.py') and '404' in err['error']
    rows.append({'sector':sector,'raw_sha256':files[0]['sha256'],'analysis_sha256':sha(folder/'analysis.json'),'plot_sha256':sha(plot),'n_events':nevents,'visual_review':review,'processed_error_sha256':sha(qfolder/'error.json')})
save_json(out/'source_review.json',{'utc':now(),'script_sha256':sha(Path(__file__)), 'frozen_sha256':sha(out/'frozen.json'),'neighbors_sha256':sha(np),'rows':rows,'limits':'Both plots inspected. Same photons as QLP; no independent observations. Formal pixel SNR and moments are not calibrated localization. Requested processed products returned HTTP404: missing evidence, not nondetection. No host or novelty established.'})
print('Verified both raw-image checks and retained both processed-product failures')
