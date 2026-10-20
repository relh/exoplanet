from pathlib import Path
from urllib.parse import urlencode
from exoplanet.pipeline import fetch,save_json,sha,now
out=Path(__file__).parent
url='https://irsa.ipac.caltech.edu/cgi-bin/ZTF/nph_light_curves?'+urlencode({'POS':'CIRCLE 26.8688666186276 65.8432925492533 0.0008333333333333334','FORMAT':'csv'})
save_json(out/'neighbor-retry-request.json',{'url':url,'created_utc':now(),'script_sha256':sha(Path(__file__)),'reason':'Original neighbor query timed out; target query subsequently succeeded. Preserve original failure.'})
try:save_json(out/'neighbor-retry-source.json',fetch(url,Path('data/targeting/ztf-399450592-neighbor-retry.csv')))
except Exception as exc:save_json(out/'neighbor-retry-error.json',{'error':repr(exc),'utc':now(),'url':url})
