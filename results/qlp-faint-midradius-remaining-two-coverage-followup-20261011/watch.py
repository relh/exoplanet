"""Diagnostic-only checks of coverage-limited four-sector faint midradius pilot pilot signals."""
from pathlib import Path
from functools import partial
import json,time,traceback
from exoplanet.pipeline import save_json,sha,now
from exoplanet.qlp_followup import follow_qlp
from exoplanet.qlp_campaign import load_qlp
from exoplanet.plots import plot_discovery
from exoplanet.secondary import scan_secondary
out=Path(__file__).parent;campaign=Path('results/qlp-faint-midradius-remaining-two-20261011')
assert not (out/'plan.json').exists()
save_json(out/'plan.json',{'utc':now(),'campaign_run_path':str(campaign/'plan.json'),'campaign_run_sha256_at_start':sha(campaign/'plan.json'),'source_sha256':{p.name:sha(p) for p in Path('src/exoplanet').glob('*.py')},'historical_policy_control_audit_sha256':sha(Path('results/qlp-faint-sector98-long-injections-20261010/audit.json')),'policy':'Coverage diagnostic policy: require >=2 supported training events and at least one of fewer_than_3_supported_events or secondary_unmeasurable, with remaining flags restricted to crowding or alternate detrending. No inconsistent-event, variability, inverted-signal or noise failures admitted. All checks diagnostic-only. Original discovery flags and primary follow-up thresholds retained. Earlier unchanged policy follows every peak passing all flags except unmeasured crowding, plus diagnostic-only checks of peaks with only crowding and alternative-detrending flags. Original flags retained; diagnostic checks do not promote peaks. Native QLP training refinement then the first two distant reserved QLP sectors in frozen order, existing frozen-prediction thresholds. Cache presence explicitly recorded; no automatically claimed independent/blind validation. Native plots and off-phase diagnostic require review. No source attribution, planet promotion or novelty claim.'})
seen=set();records=[]
def eligible():
 items=[]
 for p in (campaign/'targets').glob('*.json'):
  try:d=json.loads(p.read_text())
  except json.JSONDecodeError:continue
  for i,peak in enumerate(d.get('screened_peaks',[])):
   flags=set(peak['flags'])
   if flags<={'crowding_or_missing_crowding','alternative_detrending_prefers_other_period','secondary_unmeasurable','fewer_than_3_supported_events'} and flags&{'secondary_unmeasurable','fewer_than_3_supported_events'} and peak['diagnostics']['supported_events']>=2 and (d['tic'],i) not in seen:items.append((p,d,i))
 return items
while True:
 for p,d,i in eligible():
  key=(d['tic'],i);seen.add(key);dest=out/f'{key[0]}-peak{key[1]}'
  rec={'tic':key[0],'peak_index':i,'discovery_path':str(p),'discovery_sha256':sha(p),'started_utc':now(),'original_flags':d['screened_peaks'][i]['flags'],'diagnostic_only':True}
  try:
   checks=follow_qlp(p,dest,peak_index=i,max_sectors=2)
   rec['heldout']=[{'sector':x['sector'],'status':x['status'],'conclusion':x.get('conclusion',x.get('error'))} for x in checks]
   plot_discovery(p,dest/'discovery.png',peak_index=i,loader=partial(load_qlp,bin_minutes=0))
   t,y,e,evidence=load_qlp(d['target'],Path('data'))
   sec=scan_secondary(t,y,e,d['screened_peaks'][i]['best'])
   save_json(dest/'secondary.json',{'data':evidence,'diagnostic':sec,'policy':'Exploratory training-only off-phase scan; selected SNR not calibrated'})
   rec['status']='complete'
  except Exception as exc:rec.update(status='error',error=repr(exc),traceback=traceback.format_exc())
  rec['finished_utc']=now();records.append(rec);save_json(out/'progress.json',records);print(rec,flush=True)
 try:done=(campaign/'results.json').exists() and len(json.loads((campaign/'results.json').read_text()))==len(json.loads((campaign/'plan.json').read_text())['targets'])
 except json.JSONDecodeError:done=False
 # Re-scan once the discovery run is terminal to avoid missing final-written files.
 if done and not eligible():break
 time.sleep(15)
save_json(out/'terminal.json',{'utc':now(),'status':'complete','records':records})
