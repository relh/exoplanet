"""Read the ten frozen ZTF IDs from IRSA's public DR24 cloud collection."""
from pathlib import Path
import json,importlib.metadata,traceback
import lsdb
import dask
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent;prior=Path('results/ztf-catalog-route-20261011/catalog-results.json');rows=json.loads(prior.read_text())
ids=[int(x['oid']) for r in rows for x in r['rows']]
url='s3://ipac-irsa-ztf/ztf/enhanced/dr24/lc/hats'
plan={'created':now(),'catalog_url':url,'objectids':ids,'catalog_sha256':sha(prior),'script_sha256':sha(Path(__file__)),'versions':{n:importlib.metadata.version(n) for n in ['lsdb','s3fs','pyarrow','hats']},'policy':'Frozen ID selection, no photometric selection or retiming. Export full nested records before quality filtering. Single-threaded compute bounds concurrent partition memory.'}
assert not (out/'plan.json').exists();save_json(out/'plan.json',plan)
try:
 catalog=lsdb.open_catalog(url,columns=['objectid','objra','objdec','filterid','nepochs','lightcurve'],storage_options={'anon':True})
 selected=catalog.id_search(values={'objectid':ids})
 save_json(out/'selection.json',{'npartitions':selected.npartitions,'pixels':str(selected.get_healpix_pixels()),'created':now()})
 print('selected',selected.npartitions,flush=True)
 with dask.config.set(scheduler='single-threaded'):
  data=selected.compute()
 result=[]
 for _,r in data.iterrows():
  oid=int(r['objectid']);assert oid in ids
  p=Path(f'data/ztf/cloud-dr24-{oid}.json');p.parent.mkdir(parents=True,exist_ok=True)
  # pandas JSON preserves column names and nested photometry without hand coercion.
  lightcurve=json.loads(r['lightcurve'].to_json(orient='records',double_precision=15))
  record={'objectid':oid,'objra':float(r['objra']),'objdec':float(r['objdec']),'filterid':int(r['filterid']),'nepochs':int(r['nepochs']),'lightcurve':lightcurve}
  save_json(p,record);result.append({'objectid':oid,'path':str(p),'sha256':sha(p),'n_rows':len(lightcurve),'nepochs':record['nepochs'],'columns':list(r['lightcurve'].columns)})
 save_json(out/'results.json',{'status':'downloaded','objects':result,'missing_ids':sorted(set(ids)-{r['objectid'] for r in result}),'finished':now(),'limits':'Files are JSON exports (pandas double_precision=15) of selected cloud records, not original Parquet bytes; source catalog, ID selection and versions recorded. No interpretation yet.'});print(result,flush=True)
except Exception as e:
 save_json(out/'results.json',{'status':'error','error':repr(e),'traceback':traceback.format_exc(),'finished':now()});raise
