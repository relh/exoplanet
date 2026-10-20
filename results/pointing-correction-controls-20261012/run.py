"""Bounded real-control pointing correction; no candidate application."""
from pathlib import Path
import json,numpy as np
from astropy.io import fits
from exoplanet.pipeline import sha,save_json,now
from exoplanet.pixel_vet import difference_events
from exoplanet.prf_fit import fit_templates
O=Path(__file__).parent
SPECS=[(137151335,'20261011'),(106583384,'20261012')]
def main():
 assert not (O/'plan.json').exists();inputs={};cases=[]
 for tic,date in SPECS:
  parent=Path(f'results/prf-{tic}-{date}');clock=Path(f'results/source-check-{tic}-{date}/frozen.json');models=parent/'models.json';b=json.loads(clock.read_text())['best']
  for p in [clock,models,parent/'fits.json']:inputs[str(p)]=sha(p)
  for meta in json.loads(models.read_text())['sectors']:
   path=Path(meta['pixel_path']);zpath=parent/f"s{meta['sector']}-images.npz";inputs[str(path)]=sha(path);inputs[str(zpath)]=sha(zpath);cases.append(dict(tic=tic,sector=meta['sector'],pixel=str(path),templates=str(zpath),fits=str(parent/'fits.json'),clock=b))
 save_json(O/'plan.json',dict(created_utc=now(),cases=cases,inputs=inputs,script_sha256=sha(Path(__file__)),mask='Quality0,finitepointing/pixels; exclude absphase<max(.5day,3durations).',basis='Intercept+2POS_CORR components; standardized outsideevents. Alternating2dayblocks non-event train/test diagnostic then fitallnon-event samples forcorrection; subtract onlypointingterms, preserveintercept.',gates='All four controls must have usablepointing, heldoutRMS improvement, expectedhost winsaftercorrection, expectedhost versusbestalternative chi2gap improves, expectedsource amplitudechanges<=20percent. These thresholds frozen beforeoutputs; descriptivepilot not probability. Stop beforecandidates if anyfail.',limits='Onlyreal Kepler93 and resolvedcontaminantcontrols, unchangedclock/template/registration. No templateinjections. Errorbarsignorecoefficient uncertainty. Samephotons; empiricalscene correctiondoesnot identifyindependentPRFs.'))
 rows=[]
 for case in cases:
  tic=case['tic'];s=case['sector'];b=case['clock'];saved=next(r for r in json.loads(Path(case['fits']).read_text())['sectors'] if r['sector']==s);templates=np.load(case['templates']);hs=saved['hypotheses'];expected=str(tic) if tic==137151335 else saved['hypotheses'][0]['tic'];row=dict(tic=tic,sector=s,expected_host=expected,status='unusable')
  with fits.open(case['pixel']) as h:
   d=h[1].data;t=np.asarray(d['TIME'],float);flux=np.asarray(d['FLUX'],float);err=np.asarray(d['FLUX_ERR'],float);quality=np.asarray(d['QUALITY']);pointing=np.c_[d['POS_CORR1'],d['POS_CORR2']].astype(float)
  good=np.isfinite(t)&np.all(np.isfinite(pointing),axis=1)&np.all(np.isfinite(flux),axis=(1,2))&(quality==0);phase=(t-b['transit_time']+b['period']/2)%b['period']-b['period']/2;outside=good&(abs(phase)>max(.5,3*b['duration']))
  if outside.sum()<100 or np.any(np.std(pointing[outside],axis=0)==0):row['reason']='Missing/constantpointing or insufficientnon-eventdata';rows.append(row);continue
  blocks=np.floor((t-np.nanmin(t))/2);train=outside&(blocks%2==0);test=outside&(blocks%2==1);mu=pointing[train].mean(0);sd=pointing[train].std(0);x=np.c_[np.ones(len(t)),(pointing-mu)/sd];flat=flux.reshape(len(t),-1);coeff=np.linalg.lstsq(x[train],flat[train],rcond=None)[0];ratio=float(np.sqrt(np.mean((flat[test]-x[test]@coeff)**2))/np.sqrt(np.mean((flat[test]-flat[train].mean(0))**2)))
  mu=pointing[outside].mean(0);sd=pointing[outside].std(0);x=np.c_[np.ones(len(t)),(pointing-mu)/sd];coef=np.linalg.lstsq(x[outside],flat[outside],rcond=None)[0];corrected=(flat-x[:,1:]@coef[1:]).reshape(flux.shape)
  # Preserve raw difference cadence eligibility; unavailabletelemetry cannot be silentlyremoved.
  usable=np.isfinite(t);assert np.all(np.isfinite(pointing[usable]));raw,noise,_,events=difference_events(t[usable],flux[usable],err[usable],quality[usable],b);new,newnoise,_,new_events=difference_events(t[usable],corrected[usable],err[usable],quality[usable],b);assert events==new_events;np.testing.assert_allclose(noise,newnoise)
  def fits_for(im):
   out=[]
   for h in hs:
    v=fit_templates(im,noise,[templates['template_'+h['tic']]]);out.append(dict(tic=h['tic'],amplitude=float(v['coefficients'][0]),chi2=v['chi2'],dof=v['dof']))
   return sorted(out,key=lambda h:h['chi2'])
  before=fits_for(raw);after=fits_for(new)
  def gap(hs):return min(h['chi2'] for h in hs if h['tic']!=expected)-next(h['chi2'] for h in hs if h['tic']==expected)
  oldamp=next(h['amplitude'] for h in before if h['tic']==expected);newamp=next(h['amplitude'] for h in after if h['tic']==expected);fraction=abs(newamp-oldamp)/abs(oldamp);passed=bool(ratio<1 and after[0]['tic']==expected and gap(after)>gap(before) and fraction<=.2)
  row.update(status='measured',heldout_rms_ratio=ratio,before=before,after=after,before_gap=gap(before),after_gap=gap(after),amplitude_fraction_change=fraction,passed=passed,n_non_event=int(outside.sum()),events=events);rows.append(row);np.savez_compressed(O/f'{tic}-s{s}.npz',time=t,pointing=pointing,outside=outside,mu=mu,sd=sd,coeff=coef,raw=raw,corrected=new,error=noise)
  save_json(O/'results.json',dict(rows=rows));print(tic,s,ratio,before[0]['tic'],after[0]['tic'],fraction,passed,flush=True)
 save_json(O/'results.json',dict(rows=rows,all_passed=bool(len(rows)==4 and all(r.get('passed',False) for r in rows)),decision='No candidate application unless everypredeclaredrealcontrolgatepasses; even thencoordinatorreviewrequired.'))
if __name__=='__main__':main()
