from pathlib import Path
import json,numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from exoplanet.qlp_campaign import load_qlp
from exoplanet.followup import fixed_measure
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent
fp=Path('results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/169785835-peak0/frozen.json');dp=Path('results/qlp-faint-midradius-remaining-two-20261011/targets/169785835.json');gp=Path('results/gaia-169785835-neighbors-20261011/vari_eclipsing_binary.json')
b=json.loads(fp.read_text())['best'];d=json.loads(dp.read_text());g=json.loads(gp.read_text())[0];period=1/float(g['frequency']);epoch=b['transit_time']+b['period'];duration=b['duration'];sectors=[11,37,99,100]
assert not (out/'plan.json').exists()
save_json(out/'plan.json',{'script_sha256':sha(Path(__file__)),'inputs':{str(p):sha(p) for p in [fp,dp,gp]},'period':period,'epoch':epoch,'duration':duration,'sectors':sectors,'method':'Fixed Gaia period and half-period; epoch anchored to first imaged S100 frozen dip. No period/phase optimization. Already-opened data, exploratory only; Gaia epoch not used, no physical eclipse ephemeris validation.'})
fig,axes=plt.subplots(4,2,figsize=(12,12),constrained_layout=True);rows=[]
for j,s in enumerate(sectors):
 t,y,e,data=load_qlp(dict(d['target'],training_sectors=[s]),Path('data'),bin_minutes=0)
 row={'sector':s,'data':data,'fits':{}}
 for k,(label,p) in enumerate([('Gaia period',period),('Half Gaia period',period/2)]):
  ph=(t-epoch+p/2)%p-p/2;ax=axes[j,k];ax.scatter(ph,y,s=2,alpha=.4);ax.axvline(0,color='red',lw=.6);ax.set_title(f'S{s}: {label}');ax.set_xlabel('Days from anchored center');ax.set_ylim(.98,1.02)
  row['fits'][label]=fixed_measure(t,y,e,p,epoch,duration)
 rows.append(row)
fig.savefig(out/'folds.png',dpi=140)
save_json(out/'results.json',{'rows':rows,'plot_sha256':sha(out/'folds.png'),'limits':'Posthoc catalog-period comparison, no independent validation or false-alarm calibration. Uncertain catalog frequency extrapolates over years. Secondary eclipse need not occur at half phase. Blended QLP is not source-resolved.'})
print([(r['sector'],{k:v['supported_events'] for k,v in r['fits'].items()}) for r in rows])
