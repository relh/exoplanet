"""Chronological split diagnostic using the unchanged difference-image method."""
from pathlib import Path
import json
import numpy as np
from astropy.io import fits
from exoplanet.pixel_vet import difference_events, centroid
from exoplanet.pipeline import save_json, sha, now
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

out=Path(__file__).parent
parent=Path('results/tesscut-306101698-s104-20261010')
prior=json.loads((parent/'analysis.json').read_text())
raw=Path(prior['source']['path']);assert sha(raw)==prior['source']['sha256']
fp=Path('results/qlp-faint-sector104-followup-20261010/306101698-peak0/frozen.json')
assert sha(fp)==prior['fit_sha256']
best=json.loads(fp.read_text())['best']
numbers=prior['event_numbers'];assert len(numbers)==8 and numbers==sorted(numbers)
groups={'first_four':numbers[:4],'last_four':numbers[4:]}
assert not (out/'plan.json').exists()
save_json(out/'plan.json',{'utc':now(),'raw_sha256':sha(raw),'prior_analysis_sha256':sha(parent/'analysis.json'),
    'fit_sha256':sha(fp),'script_sha256':sha(Path(__file__)),'groups':groups,
    'fixed_centroid_region_center':prior['peak_xy'],
    'policy':'Two disjoint chronological halves, unchanged frozen ephemeris and local difference method. Region selected by prior full image and fixed for both halves. Post-selection repeatability diagnostic, not independent validation or calibrated astrometry. Preserve all outcomes; no phase or background-model tuning.'})
with fits.open(raw) as h:
    d=h[1].data;good=np.isfinite(d['TIME'])
    t=np.array(d['TIME'][good],float);f=np.array(d['FLUX'][good],float)
    e=np.array(d['FLUX_ERR'][good],float);q=d['QUALITY'][good]
full,sigma,events,ns=difference_events(t,f,e,q,best)
saved=np.load(parent/'images.npz')
np.testing.assert_array_equal(full,saved['difference'])
np.testing.assert_array_equal(sigma,saved['error'])
assert ns==numbers
cycle=np.rint((t-best['transit_time'])/best['period']).astype(int)
target=np.array(prior['target_xy']);center=prior['peak_xy'];rows=[];arrays={}
fig,axes=plt.subplots(1,2,figsize=(10,4),constrained_layout=True)
for ax,(label,chosen) in zip(axes,groups.items()):
    keep=np.isin(cycle,chosen)
    diff,err,ev,actual=difference_events(t[keep],f[keep],e[keep],q[keep],best)
    assert actual==chosen
    peak=float(np.nanmax(diff/err))
    row={'group':label,'events':actual,'maximum_formal_snr':peak}
    if peak>0:
        moment=centroid(diff,center)
        row.update(status='positive_difference',moment_xy=moment.tolist(),offset_pixels=float(np.linalg.norm(moment-target)))
        ax.plot(*moment,'w+')
    else:row['status']='no_positive_difference_no_localization'
    arrays[label+'_difference']=diff;arrays[label+'_error']=err
    im=ax.imshow(diff/err,origin='lower');fig.colorbar(im,ax=ax,shrink=.7)
    ax.plot(*target,'rx');ax.set_title(label.replace('_',' '))
    rows.append(row)
fig.suptitle('TIC 306101698, Sector 104: fixed-region split-event diagnostic')
fig.savefig(out/'split.png',dpi=140)
np.savez_compressed(out/'images.npz',**arrays)
save_json(out/'results.json',{'utc':now(),'plan_sha256':sha(out/'plan.json'),
    'full_image_reproduction_exact':True,'groups':rows,
    'limits':'Same discovery sector and selected ephemeris/region. Formal errors omit correlated background and PRF mismatch. Offsets do not identify one of the closely spaced neighbors or supply calibrated confidence.'})
print(rows)
