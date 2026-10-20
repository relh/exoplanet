"""Follow Sector 16 near-epoch tier pilot screen passes and explicitly labeled detrending diagnostics."""
from pathlib import Path
from functools import partial
import json,time,traceback
from exoplanet.pipeline import save_json,sha,now
from exoplanet.qlp_followup import follow_qlp
from exoplanet.qlp_campaign import load_qlp
from exoplanet.plots import plot_discovery
from exoplanet.secondary import scan_secondary
out=Path(__file__).parent;campaign=Path('results/qlp-near-epoch-sector16-pilot-20261011')
assert not (out/'plan.json').exists()
save_json(out/'plan.json',{'utc':now(),'campaign_run_path':str(campaign/'plan.json'),'campaign_run_sha256_at_start':sha(campaign/'plan.json'),'source_sha256':{p.name:sha(p) for p in Path('src/exoplanet').glob('*.py')},'policy':'Every peak passing all flags except unmeasured crowding, plus diagnostic-only checks of peaks with only crowding and alternative-detrending flags. Original flags retained; diagnostic checks do not promote peaks. Native QLP training refinement then the most distant available nearby reserved QLP sector (no long-term replication), existing frozen-prediction thresholds. Cache presence explicitly recorded; no automatically claimed independent/blind validation. Native plots and off-phase diagnostic require review. No source attribution, planet promotion or novelty claim.'})
seen=set();records=[]
def eligible():
 items=[]
 for p in (campaign/'targets').glob('*.json'):
  try:d=json.loads(p.read_text())
  except json.JSONDecodeError:continue
  for i,peak in enumerate(d.get('screened_peaks',[])):
   if set(peak['flags'])<={'crowding_or_missing_crowding','alternative_detrending_prefers_other_period'} and (d['tic'],i) not in seen:items.append((p,d,i))
 return items
while True:
 for p,d,i in eligible():
  key=(d['tic'],i);seen.add(key);dest=out/f'{key[0]}-peak{key[1]}'
  rec={'tic':key[0],'peak_index':i,'discovery_path':str(p),'discovery_sha256':sha(p),'started_utc':now(),'original_flags':d['screened_peaks'][i]['flags'],'diagnostic_only':'alternative_detrending_prefers_other_period' in d['screened_peaks'][i]['flags']}
  try:
   checks=follow_qlp(p,dest,peak_index=i,max_sectors=1)
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
