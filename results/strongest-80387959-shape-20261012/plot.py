from pathlib import Path
import json,numpy as np,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
O=Path(__file__).parent;r=json.loads((O/'results.json').read_text())['rows'];fig,axs=plt.subplots(2,2,figsize=(12,8),constrained_layout=True);centers=[-.75,-.375,0,.375,.75]
for i,row in enumerate(r):
 c={a['name']:a for a in row['cases']};a=c['profile'];axs[0,0].errorbar(np.array(centers)+(i-2.5)*.008,a['depths_ppm'],yerr=a['errors_ppm'],fmt='.-',label=f'S{row["sector"]}',alpha=.8)
 a=c['primary'];axs[0,1].errorbar(i,a['depths_ppm'][0],yerr=a['errors_ppm'][0],fmt='o',color='tab:blue');axs[0,1].plot(i,a['unmasked_baseline_depth_ppm'],'x',color='tab:orange')
 a=c['parity'];axs[1,0].errorbar(i,a['even_minus_odd_ppm'],yerr=a['difference_error_ppm'],fmt='o',color='tab:blue');a=c['secondary'];axs[1,1].errorbar(i,a['depths_ppm'][0],yerr=a['errors_ppm'][0],fmt='o',color='tab:blue')
axs[0,0].set(xlabel='Time from fixed transit center / original duration',ylabel='Dimming, ppm',title='Fixed exposure-integrated profile bins');axs[0,0].legend(ncol=2)
axs[0,1].set(ylabel='Primary depth, ppm',title='Joint baseline (dots); unmasked baseline (crosses)')
axs[1,0].set(ylabel='Even − odd depth, ppm',title='Fixed-cycle parity comparison');axs[1,1].set(ylabel='Exact half-phase depth, ppm',title='No phase search')
for ax in [axs[0,1],axs[1,0],axs[1,1]]:ax.set_xticks(range(len(r)),[f'S{x["sector"]}' for x in r]);ax.axhline(0,color='k',lw=.7)
axs[0,0].axhline(0,color='k',lw=.7);fig.suptitle('Conditional residual-scaled errors; correlated/systematic uncertainties omitted')
fig.savefig(O/'diagnostic.png',dpi=140)
