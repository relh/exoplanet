from pathlib import Path
import csv,json
from exoplanet.pipeline import fetch,save_json,sha,now
p=Path(__file__).parent
query='select tic_id,pl_name,pl_orbper,pl_rade,pl_trandep,st_rad,sy_dist,tran_flag from pscomppars where tran_flag=1 and pl_orbper between 0.5 and 20 and pl_rade between 0.5 and 3 and tic_id is not null'
save_json(p/'catalog-request.json',dict(created_utc=now(),query=query,script_sha256=sha(Path(__file__))))
raw=Path('data/catalogs/solar-radius-positive-controls-20261011.csv');meta=fetch('https://exoplanetarchive.ipac.caltech.edu/TAP/sync',raw,{'query':query,'format':'csv'});save_json(p/'catalog-source.json',meta);rs=list(csv.DictReader(raw.open()));assert rs and 'pl_rade' in rs[0];save_json(p/'catalog.json',rs);print(len(rs))
