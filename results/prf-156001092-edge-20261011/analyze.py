from pathlib import Path
import json,numpy as np
from astropy.io import fits
from astropy.wcs import WCS
from PRF import TESS_PRF
from exoplanet.prf_fit import fit_shift,fit_templates
from exoplanet.pixel_vet import individual_difference_events
from exoplanet.pipeline import sha,save_json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
out=Path(__file__).parent;mp=Path('results/prf-156001092-20261011/models.json');meta=json.loads(mp.read_text())['sectors'][0];fp=Path('results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/156001092-peak0/frozen.json');best=json.loads(fp.read_text())['best'];npth=Path('results/neighbors-156001092-20261011/neighbors.json');stars=json.loads(npth.read_text());pixel=Path(meta['pixel_path']);assert sha(pixel)==meta['pixel_sha256']
assert not (out/'plan.json').exists()
save_json(out/'plan.json',{'script_sha256':sha(Path(__file__)),'module_sha256':sha(Path('src/exoplanet/prf_fit.py')),'inputs':{str(p):sha(p) for p in [mp,fp,npth]},'method':'S69 mission PRF scene fit using T<17 neighbors within three pixels of stamp; expanded edge-scene sensitivity; common registration from out-of-event median only. Fixed registered PRFs with signed per-source event amplitudes plus plane. Compare inclusion of scene-model derivatives. Unpropagated TIC positions and common registration are exploratory; no physical host/false-alarm confidence. All sources/events retained.'})
with fits.open(pixel) as h:
 d=h[1].data;t=np.asarray(d['TIME'],float);ok=np.isfinite(t);t=t[ok];flux=np.asarray(d['FLUX'][ok],float);err=np.asarray(d['FLUX_ERR'][ok],float);q=d['QUALITY'][ok];w=WCS(h[2].header)
shape=flux.shape[1:];ids=[];positions=[]
for s in sorted(stars,key=lambda r:r.get('Tmag') or 99):
 if s.get('Tmag') is None or s['Tmag']>=17:continue
 pos=np.array(w.world_to_pixel_values(s['ra'],s['dec']))
 if np.all(pos>-3) and pos[0]<shape[1]+2 and pos[1]<shape[0]+2 and all(np.linalg.norm(pos-p)>.12 for p in positions):ids.append(str(s['ID']));positions.append(pos)
assert '156001092' in ids
prf=TESS_PRF(meta['camera'],meta['ccd'],69,meta['col'],meta['row'],localdatadir='data/prf/start_s0004')
phase=(t-best['transit_time']+best['period']/2)%best['period']-best['period']/2;outside=(q==0)&(abs(phase)>3*best['duration']);scene=np.nanmedian(flux[outside],axis=0);alignment=fit_shift(scene,np.ones(shape),positions,prf.locate)
templates=[prf.locate(*(p+alignment['shift']),shape) for p in positions];gy,gx=np.gradient(alignment['model']);maps,variances,numbers=individual_difference_events(t,flux,err,q,best)
fig,axes=plt.subplots(3,3,figsize=(12,11),constrained_layout=True);arrays={'scene':scene,'scene_model':alignment['model']};rows=[]
for ax,im,label in zip(axes[0],[scene,alignment['model'],scene-alignment['model']],['Out-of-event scene','Registered PRF scene','Scene residual']):
 z=ax.imshow(im,origin='lower');fig.colorbar(z,ax=ax);ax.set_title(label)
controls=[]
for j,(n,im,var) in enumerate(zip(numbers,maps,variances)):
 se=np.sqrt(var);fitsout=[]
 for motion in [False,True]:
  ts=templates+([gx,gy] if motion else []);f=fit_templates(im,se,ts);amps={tic:float(v) for tic,v in zip(ids,f['coefficients'])};fitsout.append({'motion':motion,'chi2':f['chi2'],'dof':f['dof'],'amplitudes':amps})
  if motion:
   arrays[f'event{n}_model']=f['model'];arrays[f'event{n}_difference']=im
   for ax,z,label in zip(axes[j+1],[im,f['model'],im-f['model']],[f'Event{n}', 'All-source PRFs + motion + plane','Residual']):
    c=ax.imshow(z,origin='lower');fig.colorbar(c,ax=ax);ax.set_title(label)
 # Exact-model source injection checks signed blend recovery, not calibration.
 for source in ['156001092','156001090','156001088']:
  ti=ids.index(source);truth=np.zeros(len(templates));truth[ti]=5.;synthetic=5*templates[ti]+.001*gx-.002*gy+2
  f=fit_templates(synthetic,se,templates+[gx,gy]);error=float(abs(f['coefficients'][:len(ids)]-truth).max());assert error<1e-6
  controls.append({'event':n,'source':source,'max_amplitude_error':error})
 rows.append({'event':n,'fits':fitsout});print(n,fitsout,flush=True)
for tic,tpl in zip(ids,templates):arrays['template_'+tic]=tpl
np.savez_compressed(out/'images.npz',**arrays);fig.savefig(out/'comparison.png',dpi=140)
save_json(out/'fits.json',{'scene_ids':ids,'unpropagated_positions':np.asarray(positions).tolist(),'alignment':alignment['shift'].tolist(),'alignment_boundary':alignment['boundary'],'scene_fractional_rms':float(np.sqrt(np.mean((scene-alignment['model'])**2))/np.max(scene)),'rows':rows,'controls':controls,'plot_sha256':sha(out/'comparison.png'),'images_sha256':sha(out/'images.npz'),'limits':'Conditional simultaneous signed amplitudes; registration/PRF mismatch/correlated errors not propagated. Exact mission-template controls prove plumbing only. No host probabilities or validation.'})
