from pathlib import Path
import json,numpy as np
from astropy.io import fits
from exoplanet.pipeline import sha,save_json,now
from exoplanet.pixel_vet import individual_difference_events
O=Path(__file__).parent
specs=[(137151335,'20261011','137151335','137151319'),(106583384,'20261012','780959515','106583384')]
def main():
 assert not (O/'plan.json').exists();cases=[];inputs={}
 for tic,date,expected,other in specs:
  root=Path(f'results/prf-{tic}-{date}');fp=root/'fits.json';mp=root/'models.json';cp=Path(f'results/source-check-{tic}-{date}/frozen.json')
  for p in [fp,mp,cp]:inputs[str(p)]=sha(p)
  models=json.loads(mp.read_text());old=json.loads(fp.read_text());clock=json.loads(cp.read_text())['best']
  for s in old['sectors']:
   m=next(v for v in models['sectors'] if v['sector']==s['sector']);path=Path(m['pixel_path']);inputs[str(path)]=sha(path);cases.append(dict(tic=tic,sector=s['sector'],expected=expected,other=other,positions={h:s['positions'][h] for h in [expected,other]},pixel=str(path),clock=clock))
 save_json(O/'plan.json',dict(created_utc=now(),cases=cases,inputs=inputs,script_sha256=sha(Path(__file__)),radii=[1.,1.5],method='Uncorrected raw FLUX. Catalog propagated positions unchanged, no fitted registration. Apertures comprise pixel centers withinradius. Remove sharedpixels; exclusive mean expected minus exclusive mean competitor provides equal-area constant-background rejection. Compare out-minus-in images atunchanged clocks, quality0, >=2inside/5outside, outsideD<phase<3D. Inversevariance combine eventcontrasts; retain everyevent/LOO; no pointingcorrection orPRF fit.',gate='All8 sector/radius cases require nonempty exclusive regions, positive weightedcontrast, formalSNR>=3 and positive everyleaveoneout. Empiricaleventscatter reportedbutnotcalibrated. Failure stops candidatefluxapplication; no relaxation of earlierfailedpointingcontrolgate.',scope='Retrospective knownrealcontrols. Expectedcontaminant isregionnotexactidentity. No templateinjections, independentPRFcalibration, orplanetprobability. Candidate geometricapertureoverlap alone allowed afterfailure, no candidateeventevaluation.'))
 rows=[]
 for c in cases:
  with fits.open(c['pixel']) as h:
   d=h[1].data;t=np.asarray(d['TIME'],float);k=np.isfinite(t);f=np.asarray(d['FLUX'],float)[k];e=np.asarray(d['FLUX_ERR'],float)[k];q=np.asarray(d['QUALITY'])[k];t=t[k]
  dif,var,ev=individual_difference_events(t,f,e,q,c['clock']);yy,xx=np.indices(f.shape[1:]);median=np.nanmedian(f[q==0],axis=0)
  for rad in [1.,1.5]:
   a,b=[np.hypot(xx-x,yy-y)<=rad for x,y in c['positions'].values()];aonly=a&~b;bonly=b&~a;assert aonly.any() and bonly.any();weights=aonly/aonly.sum()-bonly/bonly.sum();z=np.einsum('ijk,jk->i',dif,weights);v=np.einsum('ijk,jk->i',var,weights**2);w=1/v;mean=float(z@w/w.sum());err=float(1/np.sqrt(w.sum()));loo=[float((z@w-z[j]*w[j])/(w.sum()-w[j])) for j in range(len(z))];passed=bool(mean>0 and mean/err>=3 and min(loo)>0)
   rows.append(dict(tic=c['tic'],sector=c['sector'],radius=rad,expected=c['expected'],other=c['other'],exclusive_pixels=[int(aonly.sum()),int(bonly.sum())],overlap_pixels=int((a&b).sum()),event_numbers=ev,event_contrasts=z.tolist(),event_variances=v.tolist(),contrast=mean,error=err,snr=mean/err,empirical_event_scatter_error=float(z.std(ddof=1)/len(z)**.5),leave_one_out=loo,passed=passed,aperture_median_flux=[float(median[a].sum()),float(median[b].sum())]))
   np.savez_compressed(O/f"{c['tic']}-s{c['sector']}-r{rad}.npz",difference=dif,variance=var,expected_mask=a,other_mask=b,weights=weights)
 save_json(O/'results.json',dict(finished_utc=now(),plan_sha256=sha(O/'plan.json'),rows=rows,all_passed=all(r['passed'] for r in rows),candidate_flux_applied=False));print([(r['tic'],r['sector'],r['radius'],round(r['snr'],2),r['passed']) for r in rows])
if __name__=='__main__':main()
