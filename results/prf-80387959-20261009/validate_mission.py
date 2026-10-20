"""Deterministic checks against downloaded mission interpolation grids."""
import json
from pathlib import Path
import numpy as np
from PRF import TESS_PRF
from exoplanet.prf_fit import fit_shift
from exoplanet.pipeline import save_json
p=Path(__file__).parent
rows=[]
for m in json.loads((p/'models.json').read_text())['sectors']:
    prf=TESS_PRF(m['camera'],m['ccd'],m['sector'],m['col'],m['row'],localdatadir='data/prf/start_s0004')
    for x,y in [(6.499,6.499),(6.501,6.501),(6.1,5.8)]:
        template=prf.locate(x,y,(15,15))
        assert abs(template.sum()-1)<1e-10
        fit=fit_shift(80*template+3,np.ones((15,15)),[[6,6]],prf.locate,bound=.8,nonnegative=False)
        error=float(np.linalg.norm(fit['shift']-[x-6,y-6]))
        assert error<1e-4,error
        rows.append(dict(sector=m['sector'],position=[x,y],sum=float(template.sum()),recovery_error_pixels=error))
save_json(p/'mission-injection-validation.json',rows)
print(len(rows),'mission PRF injections passed')
