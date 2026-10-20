"""Diagnostic-only checks of coverage-limited Sector 35 pilot signals."""
from pathlib import Path
from functools import partial
import json,time,traceback
from exoplanet.pipeline import save_json,sha,now
from exoplanet.qlp_followup import follow_qlp
from exoplanet.qlp_campaign import load_qlp
from exoplanet.plots import plot_discovery
from exoplanet.secondary import scan_secondary
out=Path(__file__).parent
source=Path('results/two-reserved-tier-audit-20261011/followups.json')
gaps=json.loads(source.read_text())['modern_gate_unaccounted']
assert len(gaps)==6 and not (out/'plan.json').exists()
save_json(out/'plan.json',{'utc':now(),'source_sha256':sha(source),'targets':gaps,'script_sha256':sha(Path(__file__)),'policy':'Retrospective application of later coverage-diagnostic gates to six early peaks. Same follow_qlp refinement and first2 reserved sectors; record prior cache access, retain original flags. No blind-discovery, confirmation, host or novelty claim.'})
items=[];seen=set();records=[]
for g in gaps:
 p=Path(g['path']);d=json.loads(p.read_text());i=g['peak_index']
 assert d['tic']==g['tic'] and d['screened_peaks'][i]['flags']==g['flags']
 items.append((p,d,i))
for p,d,i in items:
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
save_json(out/'terminal.json',{'utc':now(),'status':'complete','records':records})
