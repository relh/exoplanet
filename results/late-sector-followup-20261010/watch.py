"""Apply unchanged follow-up to every future unflagged discovery-screen pass."""
import json,time,traceback
from pathlib import Path
from exoplanet.pipeline import now,save_json,sha
from exoplanet.followup import follow_target
from exoplanet.compare_qlp import compare
from exoplanet.plots import plot_discovery
out=Path(__file__).parent
batches=[Path(f'results/campaign-late-sectors-batch{i}-20261010') for i in (1,2)]
plan={'utc':now(),'rule':'Every followup_priority target from the 1322-target late-sector campaign; first unflagged screened peak, native training refinement, first two reserved sectors, QLP training extraction and native plot. All automatically produced results require review.','already_started':[420359321,395477762],'source_sha256':{p.name:sha(p) for p in Path('src/exoplanet').glob('*.py')}}
save_json(out/'plan.json',plan)
seen=set(plan['already_started']);records=[]
while True:
 for batch in batches:
  for p in sorted((batch/'targets').glob('*.json')):
   try:d=json.loads(p.read_text())
   except json.JSONDecodeError:continue
   if d['tic'] in seen or d.get('disposition')!='followup_priority':continue
   tic=d['tic'];seen.add(tic);i=next(i for i,x in enumerate(d['screened_peaks']) if not x['flags'])
   rec={'tic':tic,'discovery':str(p),'sha256':sha(p),'peak_index':i,'started_utc':now()}
   dest=out/str(tic)
   try:
    r=follow_target(p,dest,peak_index=i,max_sectors=2)
    rec['heldout']=[{'sector':x['sector'],'conclusion':x.get('conclusion',x.get('error'))} for x in r]
    plot_discovery(p,dest/'discovery.png',peak_index=i)
    q=compare(p,dest/'qlp-training',peak_index=i)
    rec['qlp_sectors']=[x['sector'] for x in q]
    rec['status']='complete'
   except Exception as e:rec.update(status='error',error=repr(e),traceback=traceback.format_exc())
   rec['finished_utc']=now();records.append(rec);save_json(out/'progress.json',records)
   print(rec,flush=True)
 try:finished=all(json.loads((b/'run.json').read_text())['status']=='complete' for b in batches)
 except json.JSONDecodeError:finished=False
 if finished:break
 time.sleep(15)
save_json(out/'terminal.json',{'utc':now(),'status':'complete','records':records,'already_started':plan['already_started']})
