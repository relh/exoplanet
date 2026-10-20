from pathlib import Path
import json,traceback,lsdb,dask
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent;plan=json.loads((out/'ztf-plan.json').read_text());ids=[int(x['row']['oid']) for x in plan['selected']];url='s3://ipac-irsa-ztf/ztf/enhanced/dr24/lc/hats'
save_json(out/'ztf-fetch-start.json',dict(started_utc=now(),plan_sha256=sha(out/'ztf-plan.json'),url=url,ids=ids))
try:
 catalog=lsdb.open_catalog(url,columns=['objectid','objra','objdec','filterid','nepochs','lightcurve'],storage_options={'anon':True})
 selected=catalog.id_search(values={'objectid':ids})
 save_json(out/'ztf-cloud-selection.json',{'npartitions':selected.npartitions,'pixels':str(selected.get_healpix_pixels()),'created':now()})
 print('selected',selected.npartitions,flush=True)
 with dask.config.set(scheduler='single-threaded'):
  data=selected.compute()
 result=[]
 for _,r in data.iterrows():
  oid=int(r['objectid']);assert oid in ids
  p=Path(f'data/resolved-followup-402-20261013/ztf-{oid}.json');p.parent.mkdir(parents=True,exist_ok=True)
  # pandas JSON preserves column names and nested photometry without hand coercion.
  lightcurve=json.loads(r['lightcurve'].to_json(orient='records',double_precision=15))
  record={'objectid':oid,'objra':float(r['objra']),'objdec':float(r['objdec']),'filterid':int(r['filterid']),'nepochs':int(r['nepochs']),'lightcurve':lightcurve}
  save_json(p,record);result.append({'objectid':oid,'path':str(p),'sha256':sha(p),'n_rows':len(lightcurve),'nepochs':record['nepochs'],'columns':list(r['lightcurve'].columns)})
 save_json(out/'ztf-cloud-results.json',{'status':'downloaded','objects':result,'missing_ids':sorted(set(ids)-{r['objectid'] for r in result}),'finished':now(),'limits':'Files are JSON exports (pandas double_precision=15) of selected cloud records, not original Parquet bytes; source catalog, ID selection and versions recorded. No interpretation yet.'});print(result,flush=True)
except Exception as e:
 save_json(out/'ztf-cloud-results.json',{'status':'error','error':repr(e),'traceback':traceback.format_exc(),'finished':now()});raise
