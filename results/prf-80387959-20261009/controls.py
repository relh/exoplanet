"""Inject into shifted-phase real difference images, preserving pixel covariance."""
import json
from pathlib import Path
import numpy as np
from astropy.io import fits
from exoplanet.pixel_vet import difference_events
from exoplanet.prf_fit import fit_templates
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent
meta=json.loads((out/'models.json').read_text())
fit=json.loads((out/'fits.json').read_text())
best=json.loads(Path('results/followup-80387959-qlp90-100-20261009/frozen.json').read_text())['best']
rows=[]
for m,r in zip(meta['sectors'],fit['sectors']):
    with fits.open(m['pixel_path']) as h:
        d=h[1].data;t=np.array(d['TIME'],float);valid=np.isfinite(t);t=t[valid]
        flux=np.array(d['FLUX'][valid],float);err=np.array(d['FLUX_ERR'][valid],float);q=np.array(d['QUALITY'][valid])
    # Mask all true-event windows so a control's baseline cannot contain a dip.
    phase=(t-best['transit_time']+best['period']/2)%best['period']-best['period']/2
    q[abs(phase)<best['duration']]=1
    images=np.load(out/f"s{m['sector']}-images.npz")
    templates={k.removeprefix('template_'):images[k] for k in images.files if k.startswith('template_')}
    controls=[]
    for fraction in np.linspace(.1,.9,41):
        b={**best,'transit_time':best['transit_time']+fraction*best['period']}
        try: diff,sigma,events,nums=difference_events(t,flux,err,q,b)
        except ValueError:continue
        injections=[]
        for hypothesis in r['hypotheses']:
            tic=hypothesis['tic'];synthetic=diff+hypothesis['amplitude']*templates[tic]
            chi2={k:fit_templates(synthetic,sigma,[v])['chi2'] for k,v in templates.items()}
            injections.append(dict(tic=tic,chi2=chi2,winner=min(chi2,key=chi2.get)))
        controls.append(dict(fraction=float(fraction),n_events=len(events),injections=injections))
    summary={k:sum(next(i for i in c['injections'] if i['tic']==k)['winner']==k for c in controls) for k in templates}
    rows.append(dict(sector=m['sector'],controls=controls,n_controls=len(controls),correct_host=summary))
    print(m['sector'],len(controls),summary,flush=True)
    save_json(out/'empirical-controls.json',dict(created_utc=now(),fits_sha256=sha(out/'fits.json'),script_sha256=sha(Path(__file__)),sectors=rows,limitations='Shifted controls overlap and need not be exchangeable with real events. Identical mission PRF injections omit PRF mismatch; no calibrated host probabilities.'))
