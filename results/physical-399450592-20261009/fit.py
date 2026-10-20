"""Post-recovery shape fits using already-opened sectors only."""
import json,shutil,importlib.metadata
from pathlib import Path
import numpy as np
from astropy.constants import G,M_sun,R_sun
from exoplanet.campaign import load_training
from exoplanet.physical_fit import fit_circular
from exoplanet.vetting import correlated_noise
from exoplanet.pipeline import save_json,sha,now

out=Path('results/physical-399450592-20261009')
parent=Path('results/followup-399450592-expanded-20261009/frozen.json')
frozen=json.loads(parent.read_text());seed=frozen['best']
discovery=Path('results/inspection-batch9-20261009/399450592-discovery.json')
target=json.loads(discovery.read_text())['target']
target={**target,'training_sectors':[18,24,25,52,58]}
neighbors=Path('results/neighbors-399450592-20261009/tic-neighbors.json')
star=next(r for r in json.loads(neighbors.read_text()) if int(r['ID'])==399450592)
axis=float((G.value*M_sun.value*star['mass']*(seed['period']*86400)**2/(4*np.pi**2))**(1/3)/(R_sun.value*star['rad']))
sigma=float(np.hypot(star['e_mass']/star['mass']/3,star['e_rad']/star['rad']))
if (out/'run.json').exists():raise RuntimeError('Preserve existing fit')
(out/'source').mkdir()
for p in Path('src/exoplanet').glob('*.py'):shutil.copyfile(p,out/'source'/p.name)
for name in ['uv.lock','pyproject.toml']:shutil.copyfile(name,out/'source'/name)
run={'status':'running','started_utc':now(),'frozen_sha256':sha(parent),
     'neighbor_catalog_sha256':sha(neighbors),'script_sha256':sha(out/'fit.py'),
     'source_sha256':{p.name:sha(p) for p in (out/'source').iterdir()},
     'batman_distribution_version':importlib.metadata.version('batman-package'),
     'target':target,'stellar_axis_guess':axis,'stellar_axis_log_sigma':sigma,
     'stellar_mass_solar':star['mass'],'stellar_radius_solar':star['rad'],
     'note':'Post-recovery fitting, no new holdout opened. Circular, undiluted on-target model; fixed limb-darkening sensitivity choices. No validation or calibrated radius uncertainty; eccentricity/blending can invalidate stellar-density comparison.'}
save_json(out/'run.json',run)
t,y,dy,data=load_training(target,Path('data'));noise=correlated_noise(t,y,dy,seed)
beta=noise.get('beta') or 1;results=[]
for limb in [(.4,.2),(.2,.2),(.6,.1)]:
    for prior in [None,sigma]:
        fit=fit_circular(t,y,dy,seed,axis,beta=beta,limb=limb,axis_log_prior_sigma=prior)
        fit['radius_earth_if_on_target']=fit['best']['radius_ratio']*star['rad']*109.076
        results.append(fit);save_json(out/'fits.json',results)
        print(limb,prior,fit['best'],fit['conditional_data_chi2'],flush=True)
run.update(status='complete',finished_utc=now(),data=data,noise=noise)
save_json(out/'run.json',run)
