from pathlib import Path
import json,numpy as np
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).parent;a=json.loads((R/'analysis.json').read_text());p=json.loads((R/'plan.json').read_text());fig,axs=plt.subplots(1,2,figsize=(9,3.7),sharey=True)
for ax,band in zip(axs,['i','z']):
 rr=[r for r in a['rows'] if r['strict'] and r['band']==band];c=next(x for x in json.loads((R/'comparisons.json').read_text()) if x['quality']=='strict' and x['band']==band)
 ax.errorbar([r['phase'] for r in rr],[r['mag']-c['baseline_weighted_mag'] for r in rr],yerr=[r['error'] for r in rr],fmt='o',color='#246178',ms=4);ax.axvspan(-p['clock']['duration']/2,p['clock']['duration']/2,color='#efc977',alpha=.4,label='Nominal transit window');ax.axhline(0,color='gray',lw=.8);ax.axhline(-2.5*np.log10(1-.0907249932820929),color='#a44444',ls='--',label='Illustrative 9.07% box');ax.set_title('SkyMapper '+band+' band');ax.set_xlabel('Days from fixed predicted midpoint');ax.set_ylim(.15,-.1);ax.grid(alpha=.15)
axs[0].set_ylabel('Magnitude minus other-night baseline');axs[1].legend(fontsize=7,loc='lower right');fig.suptitle('TIC 80387968: one event sampled; no repeated eclipse test');fig.tight_layout();fig.savefig(R/'skymapper-fixed-clock.png',dpi=160)
