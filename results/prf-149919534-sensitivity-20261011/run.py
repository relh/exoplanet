"""Fixed PRF perturbations with matched controls; no best-model selection."""
from pathlib import Path
import itertools,json,hashlib
import numpy as np
from scipy.ndimage import gaussian_filter
from astropy.io import fits
from PRF import TESS_PRF
from exoplanet.prf_fit import fit_templates
from exoplanet.pixel_vet import individual_difference_events
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;base=Path('results/prf-149919534-astrometry-20261011');read=lambda p:json.loads(p.read_text())
mp=Path('results/prf-149919534-20261011/models.json');fp=Path('results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/149919534-peak0/frozen.json')
r=read(base/'fits.json');m=read(mp)['sectors'][0];b=read(fp)['best'];z=np.load(base/'images.npz');scene=z['scene'];shape=scene.shape;ids=r['scene_ids'];pos=np.array(r['input_positions']);registration=np.array(r['alignment']);schedule=read(base/'broader-controls.json')['rows']
assert not (out/'plan.json').exists()
save_json(out/'plan.json',{'script_sha256':sha(Path(__file__)),'module_sha256':sha(Path('src/exoplanet/prf_fit.py')),'inputs':{str(p):sha(p) for p in [base/'fits.json',base/'images.npz',base/'broader-controls.json',mp,fp,Path(m['pixel_path'])]},'grid':{'dx':[-.1,0.,.1],'dy':[-.1,0.,.1],'width':[0.,.4]},'policy':'All18 offset/broadening variants retained, fixed six-source membership and Gaia-propagated positions. Refit nonnegative median scene plus plane; signed event and control source amplitudes plus scene derivatives and plane. No renormalization of truncated PRFs. Same archived36 control attempts; deduplicate exact exposure masks. Original target/neighbor536 template flux5 injections test cross-model leakage. Settings are not posterior samples; no false-alarm calibration.'})
with fits.open(m['pixel_path']) as h:
 d=h[1].data;t=np.asarray(d['TIME'],float);ok=np.isfinite(t);t=t[ok];flux=np.asarray(d['FLUX'][ok],float);err=np.asarray(d['FLUX_ERR'][ok],float);q=d['QUALITY'][ok]
maps,variances,numbers=individual_difference_events(t,flux,err,q,b);phase=(t-b['transit_time']+b['period']/2)%b['period']-b['period']/2;valid=(q==0)&(abs(phase)>b['duration']);windows={};attempts=[]
for old in schedule:
 center=b['transit_time']+(old['event']+old['fraction'])*b['period'];dt=abs(t-center);inside=valid&(dt<b['duration']/2);outside=valid&(dt>b['duration'])&(dt<3*b['duration']);ni,no=int(inside.sum()),int(outside.sum());assert (ni,no)==(old['inside'],old['outside']);row={k:old[k] for k in ['event','fraction','status','inside','outside']}
 if ni>=2 and no>=5:
  assert old['status']=='measured';key=hashlib.sha256(inside.tobytes()+outside.tobytes()).hexdigest();row['window_id']=key
  if key not in windows:
   im=np.nanmean(flux[outside],axis=0)-np.nanmean(flux[inside],axis=0);se=np.sqrt(np.nansum(err[outside]**2,axis=0)/no**2+np.nansum(err[inside]**2,axis=0)/ni**2);windows[key]=(im,se,old)
 else:assert old['status']=='insufficient_coverage'
 attempts.append(row)
assert len(windows)==8
prf=TESS_PRF(m['camera'],m['ccd'],75,m['col'],m['row'],localdatadir='data/prf/start_s0004');rows=[];reproduction=[]
for dx,dy,width in itertools.product([-.1,0.,.1],[-.1,0.,.1],[0.,.4]):
 templates=[]
 for p in pos:
  tpl=prf.locate(*(p+registration+[dx,dy]),shape)
  if width:tpl=gaussian_filter(tpl,width,mode='constant',cval=0.)
  templates.append(tpl)
 sf=fit_templates(scene,np.ones(shape),templates,nonnegative=True);gy,gx=np.gradient(sf['model'])
 def fit(im,se):
  f=fit_templates(im,se,templates+[gx,gy]);return {'amplitudes':dict(zip(ids,map(float,f['coefficients']))),'chi2':f['chi2'],'dof':f['dof']}
 row={'dx':dx,'dy':dy,'width':width,'scene_fractional_rms':float(np.sqrt(np.mean((scene-sf['model'])**2))/scene.max()),'events':[],'controls':[]}
 for n,im,v in zip(numbers,maps,variances):
  f=fit(im,np.sqrt(v));inj=[dict(source=src,**fit(5*z['template_'+src],np.sqrt(v))) for src in ['149919534','149919536']];row['events'].append(dict(event=n,injections=inj,**f))
  if dx==dy==width==0:
   ref=next(x for x in r['rows'] if x['event']==n)['fits'][1];delta=max(abs(f['amplitudes'][s]-ref['amplitudes'][s]) for s in ids);assert delta<1e-8;reproduction.append(delta)
 for key,(im,se,old) in windows.items():
  f=fit(im,se);row['controls'].append(dict(window_id=key,**f))
  if dx==dy==width==0:
   delta=max(abs(f['amplitudes'][s]-old['amplitudes'][s]) for s in ids);assert delta<1e-8;reproduction.append(delta)
 rows.append(row)
save_json(out/'results.json',{'rows':rows,'attempts':attempts,'reference_reproduction_errors':reproduction,'limits':'Conditional flux coefficients. Eight unique control windows, no independent-sample/FAP claim; settings and deterministic injections omit realistic noise/PRF evolution.'})
summary={'results_sha256':sha(out/'results.json'),'scene_rms_range':[min(x['scene_fractional_rms'] for x in rows),max(x['scene_fractional_rms'] for x in rows)],'events':[]}
for n in numbers:
 row={'event':n,'sources':{}}
 for src in ['149919534','149919536']:
  es=[next(e['amplitudes'][src] for e in x['events'] if e['event']==n) for x in rows];cs=[[c['amplitudes'][src] for c in x['controls']] for x in rows];flat=sum(cs,[])
  row['sources'][src]={'event_range':[min(es),max(es)],'control_range':[min(flat),max(flat)],'above_same_model_control_max':sum(e>max(c) for e,c in zip(es,cs)),'above_same_model_absolute_control':sum(e>max(abs(v) for v in c) for e,c in zip(es,cs))}
 summary['events'].append(row)
summary['injections']={}
for source in ['149919534','149919536']:
 inj=[i for x in rows for e in x['events'] for i in e['injections'] if i['source']==source];summary['injections'][source]={s:[min(i['amplitudes'][s] for i in inj),max(i['amplitudes'][s] for i in inj)] for s in ['149919534','149919536']}
save_json(out/'summary.json',summary);print(json.dumps(summary,indent=2))
