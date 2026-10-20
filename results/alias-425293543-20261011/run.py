from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from exoplanet.pipeline import sha,save_json
from exoplanet.qlp_campaign import load_qlp
from exoplanet.followup import fixed_measure
from exoplanet.secondary import scan_secondary
out=Path(__file__).parent;fp=Path('results/timing-425293543-20261011/fits.json');b=json.loads(fp.read_text())['joint']['best'];dp=Path('results/qlp-faint-midradius-remaining-two-20261011/targets/425293543.json');target=json.loads(dp.read_text())['target']
save_json(out/'plan.json',{'script_sha256':sha(Path(__file__)),'joint_fits_sha256':sha(fp),'discovery_sha256':sha(dp),'best':b,'policy':'Posthoc opened-data alias/secondary diagnostics. Existing fixed_measure and scan_secondary unchanged. Compare even/odd eclipses using doubled period and shifted epoch, with each parity local baseline. No calibrated binary odds or independent validation.'})
rows=[];fig,axes=plt.subplots(4,2,figsize=(12,12),constrained_layout=True)
for i,s in enumerate((53,54,80,81)):
 t,y,e,data=load_qlp(dict(target,training_sectors=[s]),Path('data'),bin_minutes=0)
 parity=[fixed_measure(t,y,e,2*b['period'],b['transit_time']+k*b['period'],b['duration']) for k in (0,1)]
 sec=scan_secondary(t,y,e,b);row={'sector':s,'data':data,'even_odd':parity,'secondary':sec};rows.append(row)
 for k,color in ((0,'tab:blue'),(1,'tab:orange')):
  phase=(t-b['transit_time']-k*b['period']+b['period'])%(2*b['period'])-b['period'];m=abs(phase)<.15
  axes[i,0].scatter(phase[m],y[m],s=5,alpha=.5,color=color,label=f'Parity {k}')
 phase=((t-b['transit_time'])/b['period'])%1;axes[i,1].scatter(phase,y,s=2,alpha=.5);axes[i,1].set_ylim(.75,1.08);axes[i,1].set_xlabel('Phase at joint period');axes[i,1].set_title(f'S{s}: full orbit');axes[i,0].set_title(f'S{s}: alternating eclipses');axes[i,0].legend();axes[i,0].set_xlabel('Days from eclipse center')
 save_json(out/'results.json',rows);print(s,[v['total'] for v in parity],sec['best_dip'],flush=True)
fig.savefig(out/'diagnostics.png',dpi=140)
save_json(out/'manifest.json',{'script_sha256':sha(Path(__file__)),'results_sha256':sha(out/'results.json'),'plot_sha256':sha(out/'diagnostics.png'),'limits':'Formal depth errors omit model/systematic/correlated uncertainties. Selected secondary maxima do not establish secondary eclipses. No alias rejection from absent odd/even difference.'})
