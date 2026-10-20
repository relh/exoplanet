from pathlib import Path
import json,lsdb,dask,hashlib,datetime,traceback,importlib.metadata
p=Path(__file__).parent;root=Path('data/resolved-followup-402-20261013');url='s3://ipac-irsa-ztf/ztf/enhanced/dr24/lc/hats'; cols=['objectid','objra','objdec','filterid','nepochs']
rec=dict(started_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),url=url,columns=cols,cone=[295.156702074408,15.63630907684673,5],note='Metadata projection explicitly excludes lightcurve; no epoch flux or timestamps requested.',packages={n:importlib.metadata.version(n) for n in ['lsdb','s3fs','dask','pandas']})
(p/'cloud-metadata-plan.json').write_text(json.dumps(rec,indent=2)+'\n')
try:
 c=lsdb.open_catalog(url,columns=cols,storage_options={'anon':True}).cone_search(*rec['cone'])
 with dask.config.set(scheduler='single-threaded'):r=c.compute()
 raw=root/'cloud-metadata.json';raw.write_text(r.to_json(orient='records',double_precision=15)+'\n');rec.update(status='success',path=str(raw),sha256=hashlib.sha256(raw.read_bytes()).hexdigest(),rows=json.loads(raw.read_text()))
except Exception as e:rec.update(status='error',error=repr(e),traceback=traceback.format_exc())
(p/'cloud-metadata.json').write_text(json.dumps(rec,indent=2)+'\n');print(json.dumps(rec,indent=2))
