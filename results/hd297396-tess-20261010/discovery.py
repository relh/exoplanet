import json
from pathlib import Path
import numpy as np
from astropy.timeseries import BoxLeastSquares
from exoplanet.qlp_campaign import load_qlp
from exoplanet.followup import fixed_measure
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent;obs_path=Path('results/hd297396-identity-20261010/observations.json');obs=json.loads(obs_path.read_text());target={'tic':293547742,'training_sectors':[8,9],'qlp_products':{str(o['sequence_number']):o for o in obs if o['provenance_name']=='QLP'},'estimate_missing_errors':True}
save_json(out/'configuration.json',dict(created_utc=now(),training_sectors=[8,9],reserved_sectors=[35,36,62,63,89,90,96],periods_days=[3.0178746,4.268863333652272],duration_grid_days=np.linspace(.03,.18,16).tolist(),note='Known TOI and RV periods supplied externally to photometry. Fit transit phase/duration only on8/9. Do not interpret no transit as exclusion of a nontransiting planet.',script_sha256=sha(Path(__file__))))
t,y,e,sources=load_qlp(target,Path('data'));save_json(out/'sources.json',sources);np.savez_compressed(out/'training.npz',time=t,flux=y,error=e)
results=[]
for period in [3.0178746,4.268863333652272]:
 result=BoxLeastSquares(t,y,e).power([period],np.linspace(.03,.18,16));best={k:float(result[k][0]) for k in ['period','transit_time','duration','depth','depth_err','depth_snr','power']};measure=fixed_measure(t,y,e,best['period'],best['transit_time'],best['duration']);results.append(dict(best=best,measurement=measure));print(best,flush=True)
save_json(out/'discovery.json',dict(created_utc=now(),results=results,limitations='Fixed supplied periods, training-fitted transit phase/duration. Trials and correlated noise not calibrated; no nontransiting-planet exclusion. OnlyQLP8/9photometryopened.'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
fig,axs=plt.subplots(2,1,figsize=(10,7),constrained_layout=True)
for ax,row in zip(axs,results):
 b=row['best'];phase=(t-b['transit_time']+b['period']/2)%b['period']-b['period']/2;ax.plot(phase,y,'.',ms=1,alpha=.4);ax.set(xlim=(-.5,.5),ylim=(np.percentile(y,.3),np.percentile(y,99.7)),title=f"P={b['period']:.6f}d; exploratory fixed-period phase fit",xlabel='Days from fitted transit',ylabel='Flattened flux')
fig.savefig(out/'discovery-folds.png',dpi=140)
