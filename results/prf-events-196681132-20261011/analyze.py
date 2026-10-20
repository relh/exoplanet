"""Fixed-template event consistency; same-sector diagnostic, not validation."""
from pathlib import Path
import json
import numpy as np
from astropy.io import fits
from exoplanet.pipeline import sha,save_json,now
from exoplanet.pixel_vet import individual_difference_events,difference_events
from exoplanet.prf_fit import fit_templates
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
out=Path(__file__).parent
parent=Path('results/prf-196681132-s91-20261011')
frozen=Path('results/qlp-faint-midradius-single-review-20261011/196681132-peak0/frozen.json')
read=lambda p:json.loads(p.read_text())
m=read(parent/'models.json')['sectors'][0]; b=read(frozen)['best']
assert sha(Path(m['pixel_path']))==m['pixel_sha256']
z=np.load(parent/'s91-images.npz'); ids=['196681132','196683452']; templates={k:z['template_'+k] for k in ids}
with fits.open(m['pixel_path']) as h:
 d=h[1].data; v=np.isfinite(d['TIME']); args=[np.array(d[k][v],dtype=int if k=='QUALITY' else float) for k in ['TIME','FLUX','FLUX_ERR','QUALITY']]
 images,variances,numbers=individual_difference_events(*args,b)
 stack,error,_,_=difference_events(*args,b)
np.testing.assert_allclose(stack,z['difference']);np.testing.assert_allclose(error,z['error'])
w=np.divide(1,variances,out=np.zeros_like(variances),where=variances>0)
def combine(keep):
 weight=w[keep].sum(axis=0)
 return (w[keep]*images[keep]).sum(axis=0)/weight,np.sqrt(1/weight)
def compare(im,err):
 fs={k:fit_templates(im,err,[templates[k]]) for k in ids}
 return {'hypotheses':{k:{'chi2':f['chi2'],'amplitude':float(f['coefficients'][0]),'dof':f['dof']} for k,f in fs.items()},'winner':min(fs,key=lambda k:fs[k]['chi2']),'neighbor_minus_target_chi2':fs[ids[1]]['chi2']-fs[ids[0]]['chi2']}
rows=[];loo=[]
for i,n in enumerate(numbers):
 rows.append({'event':n,**compare(images[i],np.sqrt(variances[i]))})
 keep=np.arange(len(numbers))!=i
 loo.append({'excluded_event':n,**compare(*combine(keep))})
# Fixed chronological halves test dependence on early versus late observations.
halves=[]
for inds in np.array_split(np.arange(len(numbers)),2):
 halves.append({'events':[numbers[i] for i in inds],**compare(*combine(inds))})
# Deterministic event-specific Gaussian controls at fitted nonnegative amplitude.
rng=np.random.default_rng(196681132);controls=[]
for i,row in enumerate(rows):
 for tic in ids:
  amp=max(0,row['hypotheses'][tic]['amplitude']);wins=0
  for j in range(20):
   trial=amp*templates[tic]+rng.normal(size=images[i].shape)*np.sqrt(variances[i])
   wins+=compare(trial,np.sqrt(variances[i]))['winner']==tic
  controls.append({'event':row['event'],'injected_tic':tic,'amplitude':amp,'correct':wins,'trials':20})
result={'created_utc':now(),'inputs':{str(p):sha(p) for p in [frozen,parent/'models.json',parent/'fits.json',parent/'s91-images.npz',Path(m['pixel_path']),Path('src/exoplanet/pixel_vet.py'),Path('src/exoplanet/prf_fit.py'),Path(__file__)]},'events':rows,'leave_one_out':loo,'chronological_halves':halves,'controls':controls,'limits':'Fixed registration and identical PRF throughout; no per-event motion correction or model mismatch. Diagonal formal errors. Correlated same-sector observations; no independent confirmation or host probabilities. Negative fitted amplitude is not a dimming source.'}
save_json(out/'results.json',result)
np.savez_compressed(out/'events.npz',images=images,variances=variances,numbers=numbers)
fig,ax=plt.subplots(2,1,figsize=(10,7),constrained_layout=True)
ax[0].plot(numbers,[r['neighbor_minus_target_chi2'] for r in rows],'o',label='Individual event')
ax[0].axhline(0,color='k',lw=.7);ax[0].set_ylabel('Neighbor chi-square minus target');ax[0].legend()
for tic in ids:ax[1].plot(numbers,[r['hypotheses'][tic]['amplitude'] for r in rows],'o-',label=tic)
ax[1].axhline(0,color='k',lw=.7);ax[1].set_ylabel('Fitted difference amplitude');ax[1].set_xlabel('Frozen-clock event number');ax[1].legend()
fig.savefig(out/'event-consistency.png',dpi=140)
print(json.dumps({'individual_target_wins':sum(r['winner']==ids[0] for r in rows),'n_events':len(rows),'loo_target_wins':sum(r['winner']==ids[0] for r in loo),'halves':halves,'controls_correct':sum(r['correct'] for r in controls),'controls_total':sum(r['trials'] for r in controls)},indent=2))
