from pathlib import Path
import itertools,json,numpy as np
from scipy.ndimage import gaussian_filter
from astropy.io import fits
from PRF import TESS_PRF
from exoplanet.prf_fit import fit_templates
from exoplanet.pixel_vet import individual_difference_events
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;base=Path('results/prf-156001092-astrometry-20261011');mp=Path('results/prf-156001092-20261011/models.json');ap=Path('results/gaia-156001092-scene-20261011/astrometry-audit.json');fp=Path('results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/156001092-peak0/frozen.json');read=lambda p:json.loads(p.read_text());r=read(base/'fits.json');m=read(mp)['sectors'][0];b=read(fp)['best'];a=next(x for x in read(ap)['rows'] if x['tic']==156001088);ids=r['scene_ids'];positions=np.array(r['input_positions']);registration=np.array(r['alignment']);z=np.load(base/'images.npz');scene=z['scene'];shape=scene.shape
assert not (out/'plan.json').exists()
save_json(out/'plan.json',{'script_sha256':sha(Path(__file__)),'module_sha256':sha(Path('src/exoplanet/prf_fit.py')),'inputs':{str(p):sha(p) for p in [base/'fits.json',base/'images.npz',mp,ap,fp]},'offsets':[-.1,0.,.1],'gaussian_broadening_pixels':[0.,.4],'mapping_dr3_ids':[x['mapping']['dr3_source_id'] for x in a['mappings']],'policy':'36 explicit model variants, all retained. Perturb common registration, optionally convolve sampled templates with sigma0.4 pixel Gaussian, test both ambiguous088 mappings. Off-stamp flux is not renormalized. Fixed stellar membership; refit scene fluxes nonnegative plus plane, then signed event amplitudes+scene derivatives+plane. No selection by event outcome; perturbations are sensitivity settings, not a probability distribution. Inject original archived target/090 PRFs with flux5 to test cross-model leakage.'})
with fits.open(m['pixel_path']) as h:
 d=h[1].data;t=np.asarray(d['TIME'],float);ok=np.isfinite(t);maps,variances,numbers=individual_difference_events(t[ok],np.asarray(d['FLUX'][ok],float),np.asarray(d['FLUX_ERR'][ok],float),d['QUALITY'][ok],b)
prf=TESS_PRF(m['camera'],m['ccd'],69,m['col'],m['row'],localdatadir='data/prf/start_s0004');rows=[]
for mapping,dx,dy,width in itertools.product(range(2),[-.1,0.,.1],[-.1,0.,.1],[0.,.4]):
 pos=positions.copy();pos[ids.index('156001088')]=a['mappings'][mapping]['propagated_xy'];templates=[]
 for p in pos:
  tpl=prf.locate(*(p+registration+[dx,dy]),shape)
  if width:tpl=gaussian_filter(tpl,width,mode='constant',cval=0.)
  templates.append(tpl)
 sf=fit_templates(scene,np.ones(shape),templates,nonnegative=True);gy,gx=np.gradient(sf['model']);row={'mapping':mapping,'dx':dx,'dy':dy,'width':width,'scene_rms_fraction':float(np.sqrt(np.mean((scene-sf['model'])**2))/scene.max()),'events':[]}
 for n,im,v in zip(numbers,maps,variances):
  se=np.sqrt(v);f=fit_templates(im,se,templates+[gx,gy]);injections=[]
  for source in ['156001092','156001090']:
   inj=fit_templates(5*z['template_'+source],se,templates+[gx,gy]);injections.append({'source':source,'target_amplitude':float(inj['coefficients'][ids.index('156001092')]),'neighbor090_amplitude':float(inj['coefficients'][ids.index('156001090')])})
  row['events'].append({'event':n,'target_amplitude':float(f['coefficients'][ids.index('156001092')]),'neighbor090_amplitude':float(f['coefficients'][ids.index('156001090')]),'chi2':f['chi2'],'dof':f['dof'],'injections':injections})
 rows.append(row)
save_json(out/'results.json',{'rows':rows,'limits':'Misspecified-template injections are deterministic sensitivity checks, not astrophysical calibration. No photon noise, realistic focus evolution or full correlated background distribution. Fitted coefficients are conditional flux, not depths or host probabilities.'})
for n in numbers:
 ev=[e for row in rows for e in row['events'] if e['event']==n];print(n,'target range',min(e['target_amplitude'] for e in ev),max(e['target_amplitude'] for e in ev),'090range',min(e['neighbor090_amplitude'] for e in ev),max(e['neighbor090_amplitude'] for e in ev))
