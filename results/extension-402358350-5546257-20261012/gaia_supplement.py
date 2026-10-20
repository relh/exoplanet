from pathlib import Path
import json,csv,numpy as np
from exoplanet.pipeline import save_json,now,sha
p=Path(__file__).parent;plan=json.loads((p/'plan.json').read_text());z=np.load(p/'gaia-arrays.npz');g=plan['gaia_model']
sp=p/'supplement-plan.json'
if not sp.exists():save_json(sp,dict(created_utc=now(),reason='Post-inspection clue: allsixG>16.80mag points clusternearunchangedexpandedTESSphasezero; oneoutofcatalogmodeldipalso dimBP/RP. This thresholdchosenafterinspection, no detectionprobability.',inputs={str(p/f):sha(p/f) for f in ['plan.json','gaia-arrays.npz','gaia-results.json']},policy='No newdata/no clockoptimization. Recordeverygoodpoint andbothoriginal/expanded phases pluscatalogphase. FitthreefixedGaussianwidths atunchangedTESSphasezero (sigma duration/[2.355,4,6]), onlymagnitudeintercept/amplitudefitted. Comparecatalogmodeldescriptivelynotas equalcomplexitymodels. Fullsavedperiod/epochprofiles: rangeofpointphaseoffsets andnumberofpredeclaredwindowinpoints usingeachprofilepair; do notselectbestprofile. BP/RP outliercheckdescriptive qualityflagsretained. No claimsformalFAP or independentGaia binaryconfirmation.'))
rows=list(csv.DictReader(Path(json.loads((p/'epoch-source.json').read_text())['path']).open()));valid=[r for r in rows if r['g_transit_time'] and any(abs(float(r['g_transit_time'])-v)<1e-8 for v in z['tc'])];assert len(valid)==len(z['tc']);points=[];fits=[]
for i,r in enumerate(valid):
 item=dict(index=i,tc=float(z['tc'][i]),mag=float(z['mag'][i]),magerr=float(z['me'][i]),catalog_phase=float(z['phase'][i]),catalog_residual_mag=float(z['mag'][i]-z['pred'][i]),bands={k:r[k] for k in ['bp_mag','rp_mag','variability_flag_bp_reject','variability_flag_rp_reject','g_other_flags','bp_other_flags','rp_other_flags']})
 for c in plan['candidate554']:
  b=c['best'];item[c['name']+'_phase']=float(((z['t'][i]-b['transit_time'])/b['period']+.5)%1-.5)
 points.append(item)
for c in plan['candidate554']:
 b=c['best'];dist=(z['t']-b['transit_time']+b['period']/2)%b['period']-b['period']/2
 for divisor in [2.355,4,6]:
  shape=np.exp(-.5*(dist/(b['duration']/divisor))**2);X=np.column_stack([np.ones(len(shape)),shape]);coef=np.linalg.lstsq(X/z['me'][:,None],z['mag']/z['me'],rcond=None)[0];cov=np.linalg.inv((X/z['me'][:,None]).T@(X/z['me'][:,None]));fits.append(dict(clock=c['name'],sigma_duration_divisor=divisor,intercept=float(coef[0]),depth_mag=float(coef[1]),depth_error=float(np.sqrt(cov[1,1])),chi2=float(np.sum(((z['mag']-X@coef)/z['me'])**2))))
c=plan['candidate554'][1];profiles=[]
for per,epoch in c['ranges']['profile_timing_pairs']:
 d=abs((z['t']-epoch+per/2)%per-per/2);inside=d<c['best']['duration']/2;profiles.append(dict(period=per,epoch=epoch,n_inside=int(inside.sum()),indices=np.where(inside)[0].tolist(),n_posthoc_deep_inside=int(np.sum(inside&(z['mag']>16.80)))))
save_json(p/'gaia-supplement.json',dict(points=points,fixed_gaussians=fits,profiles=profiles,limits='Magnitude16.80 threshold chosenafterinspection, notstatisticaltest. Widthalternativesretained notselected. Clockprofiles conditionalonTESS box andignoremodelmismatch; noposteriorprobability.'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
fig,axs=plt.subplots(1,2,figsize=(11,4),constrained_layout=True)
for ax,c in zip(axs,plan['candidate554']):
 phase=np.array([x[c['name']+'_phase'] for x in points]);ax.errorbar(phase,z['mag'],yerr=z['me'],fmt='.');ax.axvspan(-c['best']['duration']/c['best']['period']/2,c['best']['duration']/c['best']['period']/2,color='orange',alpha=.2);ax.invert_yaxis();ax.set(xlabel='Unchanged TESS phase',ylabel='Resolved-neighbor Gaia G',title=c['name']+'; no timing refit')
fig.savefig(p/'gaia-candidate-clocks.png',dpi=130);print(fits);print('profiles',len(profiles),'deepcounts',min(q['n_posthoc_deep_inside'] for q in profiles),max(q['n_posthoc_deep_inside'] for q in profiles))
