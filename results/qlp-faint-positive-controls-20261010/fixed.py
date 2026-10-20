"""Known-ephemeris probes separate sensitivity from blind recovery."""
from pathlib import Path
import json
from exoplanet.qlp_campaign import load_qlp
from exoplanet.followup import fixed_measure
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent;items=json.loads((out/'search-plan.json').read_text())['items'];default=json.loads((out/'truth.json').read_text());allrows=json.loads((out/'truth-all.json').read_text());truth={}
for d in default:
 if not d['pl_trandur']:d=next(r for r in allrows if r['pl_name']==d['pl_name'] and r['pl_trandur'] and r['pl_tranmid'])
 truth[int(d['tic_id'].replace('TIC','').strip())]=d
save_json(out/'fixed-plan.json',{'utc':now(),'truth':truth,'script_sha256':sha(Path(__file__)),'policy':'Complete default literature solution, else complete archived ExoFOP solution. Never mix epoch/period/duration across solutions. Published period/epoch/duration fixed, no fitting. Compare native and discovery10minute binning. Known-planet positive controls, not discoveries.'})
results=[]
for item in items:
 target=item['target'];r=truth[target['tic']];p=float(r['pl_orbper']);epoch=float(r['pl_tranmid'])-2457000;dur=float(r['pl_trandur'])/24
 for binning in [0,10]:
  try:
   t,y,e,data=load_qlp(target,Path('data'),bin_minutes=binning);measurement=fixed_measure(t,y,e,p,epoch,dur)
   results.append({'tic':target['tic'],'label':item['label'],'bin_minutes':binning,'status':'measured','data':data,'measurement':measurement});print(target['tic'],item['label'],binning,measurement['total'],flush=True)
  except Exception as exc:results.append({'tic':target['tic'],'label':item['label'],'bin_minutes':binning,'status':'error','error':repr(exc)})
 save_json(out/'fixed-results.json',results)
