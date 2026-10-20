"""Public SkyMapper DR4 detection cone around unresolved TESS target."""
from pathlib import Path
from exoplanet.pipeline import fetch,save_json,sha,now
out=Path(__file__).parent
params={'RA':165.31041473672,'DEC':-48.6136321332977,'SR':25/3600,'VERB':3,'CATALOG':'dr4.photometry','RESPONSEFORMAT':'VOTABLE'}
save_json(out/'request.json',{'utc':now(),'params':params,'script_sha256':sha(Path(__file__)),'documentation':'https://skymapper.anu.edu.au/how-to-access/','policy':'Public per-image detection cone encompassing target and close host alternatives. No phase optimization or data-quality interpretation before schema review. Empty/error query is not nondetection.'})
p=Path('data/catalogs/skymapper-80387959-dr4-photometry.xml')
try:
 m=fetch('https://skymapper.anu.edu.au/sm-cone/public/query',p,params);save_json(out/'source.json',m)
 from astropy.io.votable import parse
 v=parse(p);statuses=[{'name':i.name,'value':i.value,'content':i.content} for r in v.resources for i in r.infos];save_json(out/'query-status.json',statuses)
 if any(i['value'] in ['ERROR','OVERFLOW'] for i in statuses):raise ValueError(statuses)
 t=v.get_first_table().to_table();save_json(out/'schema.json',{'n_rows':len(t),'columns':[{'name':c,'dtype':str(t[c].dtype),'unit':str(t[c].unit),'description':t[c].description} for c in t.colnames]});print(len(t),t.colnames,flush=True)
except Exception as exc:save_json(out/'error.json',{'utc':now(),'error':repr(exc)});print(repr(exc),flush=True)
