from pathlib import Path
from astropy.io.votable import parse
from exoplanet.pipeline import fetch,save_json,sha,now
out=Path(__file__).parent;p=Path('data/catalogs/nsc-dr2-exposure-schema.xml');params={'REQUEST':'doQuery','LANG':'ADQL','FORMAT':'votable','QUERY':"SELECT column_name,description,unit FROM TAP_SCHEMA.columns WHERE table_name='nsc_dr2.exposure'"}
save_json(out/'exposure-schema-request.json',{'utc':now(),'params':params,'script_sha256':sha(Path(__file__))})
m=fetch('https://datalab.noirlab.edu/tap/sync',p,params);save_json(out/'exposure-schema-source.json',m)
v=parse(p);t=v.get_first_table().to_table();rows=[{k:str(r[k]) for k in t.colnames} for r in t];save_json(out/'exposure-schema.json',rows);print(rows)
