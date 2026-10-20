"""Compare fixed-aperture moments for the two injected source hypotheses."""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from exoplanet.pipeline import save_json,sha,now

out=Path('results/inspection-batch9-20261009');fig,axes=plt.subplots(1,3,figsize=(13,4),constrained_layout=True)
rows=[];sources={}
for ax,sector in zip(axes,[24,25,58]):
    paths=[Path(f'results/{prefix}-399450592-s{sector}-20261009/result.json') for prefix in ['pixel-controls','pixel-neighbor-controls']]
    target,neighbor=[json.loads(p.read_text()) for p in paths];origin=np.array(target['header_target_xy'])
    sources.update({str(p):sha(p) for p in paths})
    for result,color,label in [(target,'tab:blue','Target injections'),(neighbor,'tab:orange','Neighbor injections')]:
        points=np.array([r['centroid_xy'] for r in result['controls'] if r['status']=='measured'])-origin
        ax.scatter(points[:,0],points[:,1],s=15,alpha=.5,color=color,label=label)
    actual=np.array(target['observed_centroid_xy'])-origin
    ax.scatter(*actual,marker='*',s=140,color='red',label='Observed dip',zorder=5)
    ax.plot(0,0,'k+',ms=10,label='Catalog target')
    ax.plot(*neighbor['source_offset_pixels'],'x',color='darkorange',ms=9,label='Catalog neighbor')
    ax.set(title=f'Sector {sector}',xlabel='Detector x offset, pixels',ylabel='Detector y offset, pixels',aspect='equal')
    ax.grid(alpha=.2)
    rows.append({'sector':sector,'target_offset_pixels':target['observed_offset_from_control_median_pixels'],
                 'neighbor_offset_pixels':neighbor['observed_offset_from_control_median_pixels'],
                 'target_controls_at_least_observed_offset':target['n_controls_at_least_observed_offset'],
                 'neighbor_controls_at_least_observed_offset':neighbor['n_controls_at_least_observed_offset'],
                 'n_controls_each':target['n_controls']})
axes[0].legend(fontsize=7)
fig.suptitle('TIC 399450592: conditional pixel-injection diagnostics; no calibrated astrometric confidence')
fig.savefig(out/'399450592-localization-controls.png',dpi=160);plt.close(fig)
save_json(out/'399450592-localization-controls-summary.json',{'created_utc':now(),'source_sha256':sources,'rows':rows,
 'note':'Same fixed target-centered moment estimator for all hypotheses. Phase controls share data and templates assume common PSF. Tail counts are not planet or source probabilities.'})
