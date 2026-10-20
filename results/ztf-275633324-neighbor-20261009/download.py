from pathlib import Path
from urllib.parse import urlencode
from exoplanet.pipeline import fetch,save_json,sha,now
out=Path(__file__).parent
url='https://irsa.ipac.caltech.edu/cgi-bin/ZTF/nph_light_curves?'+urlencode({'POS':'CIRCLE 294.063739711912 57.2755619782996 0.0008333333333333334','FORMAT':'csv'})
save_json(out/'request.json',{'url':url,'created_utc':now(),'script_sha256':sha(Path(__file__)),'target':'TIC 275633326, suspected contaminant of TIC 275633324'})
try:save_json(out/'source.json',fetch(url,Path('data/targeting/ztf-275633326.csv')))
except Exception as exc:save_json(out/'error.json',{'error':repr(exc),'utc':now(),'url':url})
