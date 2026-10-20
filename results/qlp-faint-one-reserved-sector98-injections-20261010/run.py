"""Deterministic raw-flux injections into first three frozen pilot targets."""
from pathlib import Path
import json
import numpy as np
from astropy.io import fits
from exoplanet.pipeline import save_json,sha,now
from exoplanet.qlp_campaign import load_qlp,bin_curve,empirical_errors
from exoplanet.archive import qlp_flux_columns
from exoplanet.search import flatten
from exoplanet.transit_model import integrated_box
from exoplanet.campaign import process_target
out=Path(__file__).parent;parent=Path('results/qlp-faint-one-reserved-sector98-pilot-20261010')
targets=json.loads((parent/'plan.json').read_text())['targets'][:3]
assert not (out/'plan.json').exists()
save_json(out/'plan.json',{'utc':now(),'targets':targets,'periods':[.83,2.37],'radii_earth':[1.,2.],'duration_days':.04,'phase_fraction':.317,'parent_sha256':sha(parent/'plan.json'),'script_sha256':sha(Path(__file__)),'source_hashes':{p.name:sha(p) for p in Path('src/exoplanet').glob('*.py')},'policy':'Same first3 frozen pilot targets, not selected by measured quietness. Periods adopted from prior Sector104 controls before running this new control set. Audit actual search bounds rather than assuming in-grid sensitivity.12 deterministic exposure-integrated box injections before binning/detrending. Original noise and astrophysical signals retained. One phase/duration only; not completeness or calibrated false-positive rate. No heldout opened. Baseline loader equivalence must pass before any injection.'})
allrows=[]
for target in targets:
 tic=target['tic'];baseline=json.loads((parent/'targets'/f'{tic}.json').read_text())
 reference=load_qlp(target,Path('data'));curves=[]
 for evidence in reference[3]:
  sector=evidence['sector'];path=Path(f'data/qlp/{tic}-s{sector:04d}.fits')
  with fits.open(path) as h:
   d=h[1].data;fc,ec,_=qlp_flux_columns(d.names)
   t,y,dy=(np.array(d[k],dtype=float) for k in ['TIME',fc,ec])
   usable=(d['QUALITY']==0)&np.isfinite(t)&np.isfinite(y)&(y>0)
   if not np.any(usable&np.isfinite(dy)&(dy>0)):
    idx=np.flatnonzero(usable);idx=idx[np.argsort(t[idx])];dy[usable]=empirical_errors(t[idx],y[idx])[0]
   keep=usable&np.isfinite(dy)&(dy>0);t,y,dy=t[keep],y[keep],dy[keep];order=np.argsort(t);t,y,dy=t[order],y[order],dy[order]
   exposure=float(np.median(np.diff(t)))
   curves.append((t,y,dy,evidence,exposure))
 def make_loader(probe=None):
  def loader(_target,_root,window=1.5):
   parts=[];evidence=[]
   for t,y,dy,ev,exp in curves:
    factor=np.ones_like(t) if probe is None else 1-probe['depth']*integrated_box(t,probe['period'],probe['epoch'],probe['duration'],exp)
    tt,yy,ee=bin_curve(t,y*factor,dy*factor)
    parts.append(flatten(tt,yy,ee,window=window));evidence.append(dict(ev,injection=probe,exposure_days=exp))
   arrays=[np.concatenate([p[k] for p in parts]) for k in range(3)];order=np.argsort(arrays[0]);return *(a[order] for a in arrays),evidence
  return loader
 for window in [1.5,2.5]:
  actual=make_loader()(target,Path('data'),window);expected=load_qlp(target,Path('data'),window)
  for a,b in zip(actual[:3],expected[:3]):np.testing.assert_array_equal(a,b)
 save_json(out/f'{tic}-baseline-equivalence.json',{'exact_arrays_equal':True,'windows':[1.5,2.5],'discovery_sha256':sha(parent/'targets'/f'{tic}.json'),'sources':reference[3]})
 for period in [.83,2.37]:
  for radius in [1.,2.]:
   probe={'period':period,'duration':.04,'depth':(radius/(target['star']['rad']*109.076))**2,'epoch':float(min(c[0][0] for c in curves)+.317*period),'radius_earth':radius}
   dest=out/f'{tic}-p{period}-r{radius}';(dest/'targets').mkdir(parents=True)
   r=process_target(dict(target,injection=probe),Path('data'),dest,make_loader(probe),120)
   matches=[p for p in r.get('screened_peaks',[]) if abs(p['best']['period']/period-1)<.005]
   row={'tic':tic,**probe,'status':r['status'],'error':r.get('error'),'baseline_period_match':any(abs(p['period']/period-1)<.005 and p['depth_snr']>=7 for p in baseline.get('peaks',[])),'recovered_top3':any(abs(p['period']/period-1)<.005 for p in r.get('peaks',[])),'noncrowding_screen_pass':any(set(p['flags'])<={'crowding_or_missing_crowding'} for p in matches),'matching_flags':[p['flags'] for p in matches],'path':str(dest/'targets'/f'{tic}.json')}
   allrows.append(row);save_json(out/'progress.json',allrows)
save_json(out/'results.json',allrows)
