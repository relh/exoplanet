from pathlib import Path
import json,numpy as np
from astropy.io import fits
from astropy.wcs import WCS
from astropy.time import Time
from PRF import TESS_PRF
from exoplanet.prf_fit import fit_templates,fit_shift
from exoplanet.pixel_vet import difference_events,individual_difference_events
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent;tic=402358350
fp=Path(f'results/source-check-{tic}-20261011/frozen.json');best=json.loads(fp.read_text())['best']
npth=Path(f'results/neighbors-{tic}-20261011/neighbors.json');stars=json.loads(npth.read_text())
models=json.loads((out/'models.json').read_text());rows=[]
save_json(out/'plan.json',dict(created_utc=now(),frozen_sha256=sha(fp),neighbors_sha256=sha(npth),models_sha256=sha(out/'models.json'),script_sha256=sha(Path(__file__)),policy='Posthoc source diagnostic at unchanged original discovery clock. Scene includes catalog T<=18 stars inside stamp plus one-pixel margin, deduplicated at .01pixel, with relative flux fixed from Tmag rather than independent free fluxes; hypotheses all included sources within3pixels of target. Linear TIC proper motions from J2000; no parallax. Out-of-event scene registers common shift; fixed registration for event/leave-one-out fits. Each source fit additionally includes two catalog-scene spatial derivatives as motion nuisances; compare motion-only and source-only fits. Posthoc model sensitivity, not host probabilities.'))
assert [x['sector'] for x in models['sectors']]==[40,41]
for unopened in [54,81]:assert not Path(f'data/lightcurves/s{unopened:04d}-402358350.fits').exists()
for meta in models['sectors']:
 sector=meta['sector'];assert sha(Path(meta['pixel_path']))==meta['pixel_sha256']
 for mod in meta['models']:assert sha(Path(mod['path']))==mod['source']['sha256']
 with fits.open(meta['pixel_path']) as h:
  assert h[0].header['TICID']==tic and h[0].header['SECTOR']==sector
  a=h[1].data;wcs=WCS(h[2].header);t=np.asarray(a['TIME'],float);ok=np.isfinite(t);t=t[ok];flux=np.asarray(a['FLUX'][ok],float);err=np.asarray(a['FLUX_ERR'][ok],float);quality=a['QUALITY'][ok]
 year=Time(2457000+np.median(t),format='jd').jyear;shape=flux.shape[1:];positions={}
 for s in sorted(stars,key=lambda s:s.get('Tmag') or 99):
  if (s.get('Tmag') or 99)>18:continue
  ra=s['ra']+(year-2000)*(s.get('pmRA') or 0)/(3600000*np.cos(np.deg2rad(s['dec'])));dec=s['dec']+(year-2000)*(s.get('pmDEC') or 0)/3600000
  pos=np.array(wcs.world_to_pixel_values(ra,dec))
  if np.all(pos>-1) and np.all(pos<np.array(shape[::-1])) and all(np.linalg.norm(pos-q)>.01 for q in positions.values()):positions[str(s['ID'])]=pos
 assert str(tic) in positions
 host_ids=[k for k,v in positions.items() if np.linalg.norm(v-positions[str(tic)])<3]
 prf=TESS_PRF(meta['camera'],meta['ccd'],sector,meta['col'],meta['row'],localdatadir='data/prf/start_s0004')
 phase=(t-best['transit_time']+best['period']/2)%best['period']-best['period']/2
 outside=(quality==0)&(abs(phase)>3*best['duration'])
 scene=np.nanmedian(flux[outside],axis=0)
 targetpos=positions[str(tic)];mags={str(s['ID']):s['Tmag'] for s in stars}
 ratios={k:10**(-.4*(mags[k]-mags[str(tic)])) for k in positions}
 def locate_scene(x,y,shape):
  shift=np.array([x,y])-targetpos
  return sum(ratios[k]*prf.locate(*(v+shift),shape) for k,v in positions.items())
 alignment=fit_shift(scene,np.ones(shape),[targetpos],locate_scene)
 synthetic=10000*locate_scene(*(targetpos+np.array([.12,-.08])),shape)+3
 control=fit_shift(synthetic,np.ones(shape),[targetpos],locate_scene)
 np.testing.assert_allclose(control['shift'],[.12,-.08],atol=1e-5)

 diff,sigma,events,numbers=difference_events(t,flux,err,quality,best)
 es,vs,ns=individual_difference_events(t,flux,err,quality,best);assert numbers==ns;np.testing.assert_allclose(es,events)
 templates={k:prf.locate(*(positions[k]+alignment['shift']),shape) for k in host_ids}
 center=positions[str(tic)]+alignment['shift'];eps=.01
 gradx=(locate_scene(*(center+[eps,0]),shape)-locate_scene(*(center-[eps,0]),shape))/(2*eps)
 grady=(locate_scene(*(center+[0,eps]),shape)-locate_scene(*(center-[0,eps]),shape))/(2*eps)

 def fit_all(im,error):
  hs=[]
  for k,v in templates.items():
   f=fit_templates(im,error,[v,gradx,grady]);baseline=fit_templates(im,error,[gradx,grady]);plain=fit_templates(im,error,[v]);hs.append(dict(tic=k,chi2=f['chi2'],dof=f['dof'],amplitude=float(f['coefficients'][0]),motion_coefficients=f['coefficients'][1:3].tolist(),without_motion_chi2=plain['chi2'],without_motion_amplitude=float(plain['coefficients'][0]),motion_only_chi2=baseline['chi2']))
  return sorted(hs,key=lambda r:r['chi2'])
 hs=fit_all(diff,sigma);per=[dict(event=n,hypotheses=fit_all(e,np.sqrt(v))) for n,e,v in zip(ns,es,vs)];loo=[]
 for omit,n in enumerate(ns):
  keep=np.arange(len(ns))!=omit;weights=np.divide(1,vs[keep],out=np.zeros_like(vs[keep]),where=vs[keep]>0);total=weights.sum(axis=0);im=np.divide((weights*es[keep]).sum(axis=0),total,out=np.zeros(shape),where=total>0);error=np.sqrt(np.divide(1,total,out=np.full(shape,np.inf),where=total>0));loo.append(dict(omitted=n,hypotheses=fit_all(im,error)))
 np.savez_compressed(out/f's{sector}-images.npz',scene=scene,gradx=gradx,grady=grady,scene_model=alignment['model'],difference=diff,error=sigma,event_differences=es,event_variances=vs,**{'template_'+k:v for k,v in templates.items()})
 row=dict(sector=sector,year=year,positions={k:v.tolist() for k,v in positions.items()},alignment=alignment['shift'].tolist(),alignment_boundary=alignment['boundary'],synthetic_registration_recovered=control['shift'].tolist(),scene_flux_policy='Tmag fixed ratios with one common amplitude and plane',scene_fractional_rms=float(np.sqrt(np.mean((scene-alignment['model'])**2))/np.max(scene)),hypotheses=hs,events=per,leave_one_out=loo,n_events=len(es));rows.append(row)
 save_json(out/'fits.json',dict(created_utc=now(),tic=tic,sectors=rows,limits='Conditional PRF comparison; diagonal formal errors; model mismatch and registration uncertainty not propagated. Hypotheses selected posthoc from catalog geometry. Each source fit additionally includes two catalog-scene spatial derivatives as motion nuisances; compare motion-only and source-only fits. Posthoc model sensitivity, not host probabilities.'))
 print(sector,'shift',alignment['shift'],'boundary',alignment['boundary'],'best',hs[:2],'LOO',[(r['omitted'],r['hypotheses'][0]['tic']) for r in loo],flush=True)
