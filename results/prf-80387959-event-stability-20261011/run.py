"""Fixed-template per-event and leave-one-event-out host diagnostics."""
from pathlib import Path
from collections import Counter
import json
import numpy as np
from astropy.io import fits
from exoplanet.pixel_vet import difference_events
from exoplanet.prf_fit import fit_templates
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent;base=Path('results/prf-80387959-20261009')
mp=base/'models.json';fp=base/'fits.json';bp=Path('results/followup-80387959-qlp90-100-20261009/frozen.json')
meta=json.loads(mp.read_text());old=json.loads(fp.read_text());best=json.loads(bp.read_text())['best']
assert not (out/'plan.json').exists()
save_json(out/'plan.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'model_manifest_sha256':sha(mp),'fits_sha256':sha(fp),'frozen_sha256':sha(bp),'fit_module_sha256':sha(Path('src/exoplanet/prf_fit.py')),'policy':'Keep frozen ephemeris, original sector registration and archived host templates. Reproduce original full stack before per-event and leave-one-out fits. All event removals retained; no favorable subset selection, no probabilities or host promotion.'})
rows=[]
for m in meta['sectors']:
 sector=m['sector'];imagep=base/f's{sector}-images.npz';z=np.load(imagep)
 templates={k.removeprefix('template_'):z[k] for k in z.files if k.startswith('template_')}
 with fits.open(m['pixel_path']) as h:
  d=h[1].data;t=np.asarray(d['TIME'],float);valid=np.isfinite(t);t=t[valid];q=d['QUALITY'][valid]
  flux=np.asarray(d['FLUX'][valid],float);err=np.asarray(d['FLUX_ERR'][valid],float)
 diff,sigma,events,numbers=difference_events(t,flux,err,q,best)
 np.testing.assert_allclose(diff,z['difference'],rtol=1e-10,atol=1e-10)
 np.testing.assert_allclose(sigma,z['error'],rtol=1e-10,atol=1e-10)
 phase=(t-best['transit_time']+best['period']/2)%best['period']-best['period']/2
 en=np.rint((t-best['transit_time'])/best['period']).astype(int)
 variances=[];counts=[]
 for n in numbers:
  inside=(q==0)&(en==n)&(abs(phase)<best['duration']/2)
  outside=(q==0)&(en==n)&(abs(phase)>best['duration'])&(abs(phase)<3*best['duration'])
  variances.append(np.nansum(err[outside]**2,axis=0)/outside.sum()**2+np.nansum(err[inside]**2,axis=0)/inside.sum()**2)
  counts.append({'event':int(n),'inside':int(inside.sum()),'outside':int(outside.sum())})
 variances=np.array(variances)
 def evaluate(im,se):
  fs={k:fit_templates(im,se,[v]) for k,v in templates.items()}
  chi={k:f['chi2'] for k,f in fs.items()}
  return {'winner':min(chi,key=chi.get),'chi2':chi,'amplitudes':{k:float(f['coefficients'][0]) for k,f in fs.items()},'target_delta_chi2':chi['80387959']-min(chi.values())}
 full=evaluate(diff,sigma)
 previous=next(r for r in old['sectors'] if r['sector']==sector)
 for hyp in previous['hypotheses']:np.testing.assert_allclose(full['chi2'][hyp['tic']],hyp['chi2'],rtol=1e-9)
 individual=[];jackknife=[]
 for i,n in enumerate(numbers):
  individual.append({'event':int(n),**evaluate(events[i],np.sqrt(variances[i]))})
  keep=np.arange(len(numbers))!=i;v=variances[keep];w=np.divide(1,v,out=np.zeros_like(v),where=v>0);total=w.sum(axis=0)
  im=np.divide((w*events[keep]).sum(axis=0),total,out=np.zeros_like(total),where=total>0)
  se=np.sqrt(np.divide(1,total,out=np.full_like(total,np.inf),where=total>0))
  jackknife.append({'omitted_event':int(n),'n_remaining':int(keep.sum()),**evaluate(im,se)})
 row={'sector':sector,'pixel_path':m['pixel_path'],'pixel_sha256':sha(Path(m['pixel_path'])),'images_sha256':sha(imagep),'original_stack_reproduced':True,'counts':counts,'full':full,'individual':individual,'leave_one_out':jackknife,'single_winners':dict(Counter(r['winner'] for r in individual)),'leave_one_out_winners':dict(Counter(r['winner'] for r in jackknife))}
 rows.append(row);save_json(out/'results.json',rows);print(sector,'full',full['winner'],'single',row['single_winners'],'omit',row['leave_one_out_winners'],flush=True)
