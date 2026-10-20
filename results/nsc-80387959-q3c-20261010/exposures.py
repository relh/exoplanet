from pathlib import Path
from astropy.io.votable import parse
from exoplanet.pipeline import fetch,save_json,sha,now
out=Path(__file__).parent;t=parse('data/catalogs/nsc-80387959-q3c-measurements.xml').get_first_table().to_table();ids=sorted(set(map(str,t['exposure'])))
query='SELECT * FROM nsc_dr2.exposure WHERE exposure IN ('+','.join("'"+x.replace("'","''")+"'" for x in ids)+')'
params={'REQUEST':'doQuery','LANG':'ADQL','FORMAT':'votable','QUERY':query,'MAXREC':10000};p=Path('data/catalogs/nsc-80387959-q3c-exposures.xml');save_json(out/'exposures-request.json',{'utc':now(),'params':params,'script_sha256':sha(Path(__file__))})
m=fetch('https://datalab.noirlab.edu/tap/sync',p,params);save_json(out/'exposures-source.json',m);v=parse(p);status=[{'name':i.name,'value':i.value,'content':i.content} for r in v.resources for i in r.infos];save_json(out/'exposures-status.json',status);assert not any(i['value'] in ['ERROR','OVERFLOW'] for i in status)
t=v.get_first_table().to_table();assert set(map(str,t['exposure']))==set(ids);print('Matched exposures',len(t),flush=True)
