"""Targeted phase/duration search at externally reported RV period."""
from pathlib import Path
import json
import numpy as np
from astropy.timeseries import BoxLeastSquares
from exoplanet.pipeline import save_json,sha,now
from exoplanet.qlp_campaign import load_qlp
from exoplanet.campaign import peak_at
from exoplanet.followup import fixed_measure
out=Path(__file__).parent;original=Path('results/hd32564-tess-sector98-20261010/plan.json');target=json.loads(original.read_text())['target']
period=23.597;durations=[.04,.08,.12,.18,.24]
assert not (out/'plan.json').exists()
save_json(out/'plan.json',{'utc':now(),'period_days':period,'durations_days':durations,'parent_plan_sha256':sha(original),'script_sha256':sha(Path(__file__)),'policy':'Post-hoc targeted search at rounded external RV period23.597days, all phases and listed box durations, native QLP Sector98. No RV conjunction assumption, period refinement, independent validation or calibrated false-alarm probability. Already-opened Sectors5/32 measured at selected frozen model, with timing propagation unquantified. Does not test all RV period uncertainties or exclude planets.'})
t,y,e,data=load_qlp(target,Path('data'),bin_minutes=0)
r=BoxLeastSquares(t,y,e).power(np.array([period]),np.array(durations),objective='likelihood',oversample=20);b=peak_at(r,int(np.argmax(r.power)))
freeze={'utc':now(),'best':b,'data':data,'measurement':fixed_measure(t,y,e,b['period'],b['transit_time'],b['duration'])};save_json(out/'frozen.json',freeze)
rows=[]
for sector in [5,32]:
 row={'sector':sector,'already_opened':True}
 try:
  tt,yy,ee,dd=load_qlp(dict(target,training_sectors=[sector]),Path('data'),bin_minutes=0);row.update(status='measured',data=dd,measurement=fixed_measure(tt,yy,ee,b['period'],b['transit_time'],b['duration']))
 except Exception as exc:row.update(status='error',error=repr(exc))
 rows.append(row)
save_json(out/'results.json',{'finished_utc':now(),'selected':b,'training_measurement':freeze['measurement'],'earlier_sectors':rows})
print('best',b,'training',freeze['measurement']['total'],'events',freeze['measurement']['events'])
for row in rows:print(row['sector'],row.get('measurement',{}).get('total'),row.get('error'))
