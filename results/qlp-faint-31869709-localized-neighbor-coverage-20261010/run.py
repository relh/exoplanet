"""Archive availability check for two catalog neighbors; no source attribution."""
from pathlib import Path
from exoplanet.archive import mast_query
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent
ids=[31869705,31869706]
req={'service':'Mast.Caom.Filtered','params':{'columns':'obs_id,target_name,provenance_name,sequence_number,dataURL','filters':[{'paramName':'target_name','values':[str(x) for x in ids]},{'paramName':'provenance_name','values':['QLP','TESS-SPOC','SPOC']}]},'format':'json','pagesize':50000,'page':1}
assert not (out/'plan.json').exists()
save_json(out/'plan.json',{'utc':now(),'request':req,'script_sha256':sha(Path(__file__)),'neighbor_cone_sha256':sha(Path('results/neighbors-31869709-20261010/neighbors.json')),'policy':'Exact catalog target-name availability query for two sources nearest the Sector29/30 difference-image moments. Missing products are not negative photometric evidence. Does not search aliases or coordinate-only observations.'})
try:
 rows,meta=mast_query(req,Path('data/catalogs/31869709-localized-neighbor-coverage-20261010.json'));save_json(out/'observations.json',rows);save_json(out/'source.json',meta)
 print('observations',len(rows),flush=True)
 save_json(out/'results.json',{'finished_utc':now(),'status':'complete','n_observations':len(rows),'counts_by_target':{str(tic):sum(str(r['target_name'])==str(tic) for r in rows) for tic in ids}})
except Exception as exc:
 save_json(out/'error.json',{'utc':now(),'error':repr(exc)});raise
