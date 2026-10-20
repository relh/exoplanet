"""Record why the predeclared five-second matching run could not produce a comparison."""
import json
from pathlib import Path
import numpy as np
from exoplanet.pipeline import save_json,sha,now
from exoplanet.qlp_campaign import load_qlp
from exoplanet.campaign import load_training
out=Path(__file__).parent
p=Path('results/qlp-faint-expanded-20261010/targets/356346889.json');target=dict(json.loads(p.read_text())['target'],training_sectors=[80]);q=load_qlp(target,Path('data'),bin_minutes=0);s=load_training(target,Path('data'))
i=np.searchsorted(s[0],q[0]);left=np.clip(i-1,0,len(s[0])-1);right=np.clip(i,0,len(s[0])-1);delta=np.minimum(abs(s[0][left]-q[0]),abs(s[0][right]-q[0]))*86400
save_json(out/'coverage.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'plan_sha256':sha(out/'plan.json'),'n_qlp':len(q[0]),'n_spoc':len(s[0]),'n_matches_within_5sec':int((delta<5).sum()),'nearest_offsets_seconds_quantiles':np.quantile(delta,[0,.25,.5,.75,1]).tolist(),'qlp_evidence':q[3],'spoc_evidence':s[3],'status':'no_matches_at_predeclared_tolerance','original_run_error':'ValueError: zero-size array to reduction operation minimum which has no identity','policy':'Preserve failed matching attempt. Do not widen tolerance or infer a matched-exposure depth comparison.'})
print('matches',int((delta<5).sum()),'minimum offset',delta.min())
