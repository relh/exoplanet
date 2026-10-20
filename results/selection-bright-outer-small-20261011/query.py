"""Metadata-only extension to bright small stars at 120–200 pc."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
import traceback
from exoplanet.archive import mast_query
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent
assert not (out/'run.json').exists()
plan={'utc':now(),'script_sha256':sha(Path(__file__)),'bounds':[[120,160],[160,200]],'radius_solar':[.15,.6],'Tmag':[6,12],'policy':'Extend distance beyond previous <=120pc pool while prioritizing brighter stars rather than noisier faint tails. Metadata only; require distant reserved QLP sectors before opening photometry. Radius/brightness is a sensitivity proxy, not measured quietness. No claim of unsearched status or completeness.'}
save_json(out/'run.json',plan)
def query(bounds):
 lo,hi=bounds
 req={'service':'Mast.Catalogs.Filtered.Tic.Rows','params':{'columns':'ID,ra,dec,Tmag,rad,Teff,d,contratio,disposition,duplicate_id','filters':[{'paramName':'rad','values':[{'min':.15,'max':.6}]},{'paramName':'Tmag','values':[{'min':6,'max':12}]},{'paramName':'d','values':[{'min':lo,'max':hi}]}]},'format':'json','pagesize':100000,'page':1}
 save_json(out/f'request-{lo}-{hi}.json',req)
 try:
  rows,meta=mast_query(req,Path(f'data/targeting/bright-outer-small-{lo}-{hi}-20261011.json'))
  return {'bounds':bounds,'status':'complete','n_rows':len(rows),'source':meta},rows
 except Exception as exc:return {'bounds':bounds,'status':'error','error':repr(exc),'traceback':traceback.format_exc()},[]
records=[];stars={}
with ThreadPoolExecutor(max_workers=2) as pool:
 for future in as_completed([pool.submit(query,b) for b in plan['bounds']]):
  rec,rows=future.result();records.append(rec);print(rec['bounds'],rec['status'],rec.get('n_rows'),flush=True)
  for r in rows:
   tic=int(r['ID'])
   if tic in stars:assert stars[tic]==r
   stars[tic]=r
  save_json(out/'progress.json',records)
save_json(out/'sources.json',records)
assert all(r['status']=='complete' for r in records),'Incomplete metadata query'
save_json(out/'catalog-rows.json',[stars[k] for k in sorted(stars)])
save_json(out/'terminal.json',{'utc':now(),'status':'complete','n_rows':len(stars),'catalog_sha256':sha(out/'catalog-rows.json')})
