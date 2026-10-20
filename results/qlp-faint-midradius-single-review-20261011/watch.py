from pathlib import Path
from functools import partial
import json,time,traceback
from exoplanet.pipeline import save_json,sha,now
from exoplanet.qlp_campaign import load_qlp
from exoplanet.followup import refine_training,fixed_measure
from exoplanet.plots import plot_discovery
from exoplanet.secondary import scan_secondary
out=Path(__file__).parent;campaign=Path('results/qlp-faint-midradius-single-remaining-20261011');assert not (out/'plan.json').exists()
save_json(out/'plan.json',{'utc':now(),'campaign_sha256':sha(campaign/'plan.json'),'script_sha256':sha(Path(__file__)),'source_hashes':{p.name:sha(p) for p in Path('src/exoplanet').glob('*.py')},'policy':'Original/detrending and coverage diagnostic eligibility unchanged. Native training refinement and plots only. No reserved sectors or validation claims. Every eligible fit needs visual/catalog/source review; original flags retained.'})
seen=set();records=[]
def eligible():
 items=[]
 for p in (campaign/'targets').glob('*.json'):
  d=json.loads(p.read_text())
  for i,v in enumerate(d.get('screened_peaks',[])):
   flags=set(v['flags']);base={'crowding_or_missing_crowding','alternative_detrending_prefers_other_period'};extra={'secondary_unmeasurable','fewer_than_3_supported_events'}
   category='original_or_detrending' if flags<=base else 'coverage_diagnostic' if flags<=base|extra and flags&extra and v['diagnostics']['supported_events']>=2 else None
   if category and (d['tic'],i) not in seen:items.append((p,d,i,category))
 return items
while True:
 for p,d,i,category in eligible():
  key=(d['tic'],i);seen.add(key);dest=out/f'{key[0]}-peak{i}';dest.mkdir();v=d['screened_peaks'][i]
  record={'tic':key[0],'peak_index':i,'category':category,'discovery_path':str(p),'discovery_sha256':sha(p),'started_utc':now(),'original_flags':v['flags']}
  try:
   t,y,e,data=load_qlp(d['target'],Path('data'),bin_minutes=0);best,ranges=refine_training(t,y,e,v['best'],seed_baseline=d['clean_baseline_days'])
   save_json(dest/'frozen.json',{'tic':key[0],'collection':'QLP','discovery_sha256':sha(p),'peak_index':i,'seed':v['best'],'best':best,'timing_ranges':ranges,'training_sectors':d['target']['training_sectors'],'training_data':data,'heldout_sectors':[],'training_measurement':fixed_measure(t,y,e,best['period'],best['transit_time'],best['duration']),'policy':'Training refinement only; no independent validation.'})
   plot_discovery(p,dest/'discovery.png',peak_index=i,loader=partial(load_qlp,bin_minutes=0))
   save_json(dest/'secondary.json',{'data':data,'diagnostic':scan_secondary(t,y,e,v['best']),'policy':'Exploratory training-only diagnostic, selected SNR uncalibrated.'})
   record.update(status='complete',visual_review_pending=True,source_checks_pending=True)
  except Exception as exc:record.update(status='error',error=repr(exc),traceback=traceback.format_exc())
  records.append(record);save_json(out/'progress.json',records);print(record,flush=True)
 done=(campaign/'results.json').exists()
 if done and not eligible():break
 time.sleep(15)
save_json(out/'terminal.json',{'utc':now(),'status':'complete','records':records})
