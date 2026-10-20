from pathlib import Path
import json,numpy as np
from astropy.io import fits
from PRF import TESS_PRF
from exoplanet.prf_fit import fit_templates
from exoplanet.pipeline import sha,save_json,now
p=Path(__file__).parent;parent=Path('results/prf-5540688-20261011');r=json.loads((parent/'fits.json').read_text());models=json.loads((parent/'models.json').read_text());npth=Path('results/neighbors-5540688-20261011/neighbors.json');stars=json.loads(npth.read_text());mags={str(s['ID']):s['Tmag'] for s in stars};fp=Path('results/source-check-5540688-20261011/frozen.json');best=json.loads(fp.read_text())['best'];target='5540688';neighbor='5540683';ratio=10**(-.4*(mags[neighbor]-mags[target]));rows=[]
assert [x['sector'] for x in models['sectors']]==[8,9]
for s in [35,36,62]:assert not Path(f'data/lightcurves/s{s:04d}-5540688.fits').exists()
assert not (p/'plan.json').exists();save_json(p/'plan.json',dict(created_utc=now(),script_sha256=sha(Path(__file__)),inputs={str(x):sha(x) for x in [parent/'fits.json',parent/'models.json',npth,fp]},aperture_radii_pixels=[1,1.5],policy='Exploratory physical-depth diagnostic. Unchanged parent clock/registration; no extra observations. Direct apertures assume stable additive contamination. Compare catalog-ratio scene with neighbor normalization freed; no calibrated host probability.',catalog_neighbor=next(x for x in stars if str(x['ID'])==neighbor)))
for meta,s in zip(models['sectors'],r['sectors']):
 sec=s['sector'];raw=Path(meta['pixel_path']);assert sha(raw)==meta['pixel_sha256']
 for m in meta['models']:assert sha(Path(m['path']))==m['source']['sha256']
 z=np.load(parent/f's{sec}-images.npz');shape=z['scene'].shape;prf=TESS_PRF(meta['camera'],meta['ccd'],sec,meta['col'],meta['row'],localdatadir='data/prf/start_s0004');pos={k:np.array(v)+s['alignment'] for k,v in s['positions'].items()};templates={k:prf.locate(*v,shape) for k,v in pos.items()};scene=sum(10**(-.4*(mags[k]-mags[target]))*v for k,v in templates.items());other=scene-ratio*templates[neighbor]
 base=fit_templates(z['scene'],np.ones(shape),[scene]);free=fit_templates(z['scene'],np.ones(shape),[other,templates[neighbor]]);diff=fit_templates(z['difference'],z['error'],[templates[neighbor]])
 np.testing.assert_allclose(base['model'],z['scene_model'],rtol=1e-8,atol=1e-7)
 cases=[]
 for name,f,coef in [('fixed_catalog_ratios',base,float(base['coefficients'][0]*ratio)),('neighbor_normalization_free',free,float(free['coefficients'][1]))]:
  cases.append(dict(model=name,neighbor_flux_coefficient=coef,difference_coefficient=float(diff['coefficients'][0]),fractional_dip=float(diff['coefficients'][0]/coef),scene_residual_rms=float(np.sqrt(np.mean((z['scene']-f['model'])**2))),scene_fractional_rms=float(np.sqrt(np.mean((z['scene']-f['model'])**2))/np.max(z['scene'])),coefficients=f['coefficients'].tolist(),dof=f['dof'],chi2=f['chi2']))
 with fits.open(raw) as h:
  a=h[1].data;t=np.asarray(a['TIME'],float);valid=np.isfinite(t);t=t[valid];flux=np.asarray(a['FLUX'][valid],float);err=np.asarray(a['FLUX_ERR'][valid],float);q=a['QUALITY'][valid]
 phase=(t-best['transit_time']+best['period']/2)%best['period']-best['period']/2;ev=np.rint((t-best['transit_time'])/best['period']).astype(int);yy,xx=np.indices(shape);aps=[]
 for rad in [1,1.5]:
  ap=np.hypot(xx-pos[neighbor][0],yy-pos[neighbor][1])<=rad;series=np.sum(flux[:,ap],axis=1);variance=np.sum(err[:,ap]**2,axis=1);events=[]
  for rec in s['events']:
   n=rec['event'];inside=(q==0)&(ev==n)&(abs(phase)<best['duration']/2);outside=(q==0)&(ev==n)&(abs(phase)>best['duration'])&(abs(phase)<3*best['duration']);assert inside.sum()>=2 and outside.sum()>=5;assert np.isfinite(series[inside|outside]).all();a0=float(np.mean(series[outside]));a1=float(np.mean(series[inside]));v0=float(variance[outside].sum()/outside.sum()**2);v1=float(variance[inside].sum()/inside.sum()**2);dep=(a0-a1)/a0;error=np.sqrt(v1/a0**2+a1**2*v0/a0**4);events.append(dict(event=n,outside_mean=a0,inside_mean=a1,outside_variance=v0,inside_variance=v1,n_inside=int(inside.sum()),n_outside=int(outside.sum()),depth=dep,error=float(error)))
  depths=np.array([x['depth'] for x in events]);weights=np.array([x['error']**-2 for x in events]);aps.append(dict(radius_pixels=rad,pixels=np.argwhere(ap).tolist(),events=events,weighted_depth=float(np.average(depths,weights=weights)),formal_error=float(weights.sum()**-.5),min_depth=float(depths.min()),max_depth=float(depths.max()),modeled_neighbor_flux_fraction=float((base['coefficients'][0]*ratio*templates[neighbor][ap].sum())/np.mean([x['outside_mean'] for x in events]))))
 np.savez_compressed(p/f's{sec}-models.npz',scene=z['scene'],scene_template=scene,other_template=other,neighbor_template=templates[neighbor],difference=z['difference'],error=z['error'])
 rows.append(dict(sector=sec,raw_path=str(raw),raw_sha256=sha(raw),parent_images_sha256=sha(parent/f's{sec}-images.npz'),neighbor_position=pos[neighbor].tolist(),models=cases,apertures=aps));save_json(p/'results.json',dict(created_utc=now(),neighbor=neighbor,period=best['period'],catalog_flux_ratio=ratio,sectors=rows))
 print(sec,'models',[(x['model'],x['fractional_dip']) for x in cases],'apertures',[(x['radius_pixels'],x['weighted_depth'],x['formal_error']) for x in aps],flush=True)
