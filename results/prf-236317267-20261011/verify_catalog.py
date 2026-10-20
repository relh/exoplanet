from pathlib import Path
import json,csv
from exoplanet.pipeline import sha,save_json,now
O=Path(__file__).parent;np=Path('results/neighbors-236317267-20261011');stars=json.loads((np/'neighbors.json').read_text());star=next(x for x in stars if int(x['ID'])==236317263);assert str(star['GAIA'])=='1316214619309621248'
x=json.loads((O/'neighbor-identity.json').read_text());assert x['status']=='complete' and sha(Path(x['path']))==x['sha256'];assert list(csv.DictReader(Path(x['path']).open()))==x['rows']==[{'dr2_source_id':'1316214619309621248','dr3_source_id':'1316214619309621248'}]
v=json.loads((O/'neighbor-vsx.json').read_text())[0];assert v['status']=='success' and sha(Path(v['path']))==v['sha256'];assert list(csv.DictReader(Path(v['path']).open()))==v['rows'];assert v['rows'][0]['Name'].strip()=='Gaia DR3 1316214619309621248';assert v['rows'][0]['Type'].strip()=='VAR'
for sector in [51,78]:assert not Path(f'data/lightcurves/s{sector:04d}-236317267.fits').exists()
save_json(O/'catalog-verification.json',dict(status='passed',created_utc=now(),script_sha256=sha(Path(__file__)),neighbor=236317263,exact_dr2_dr3_vsx_identity=True,additional_reserved_caches_absent=[51,78],limits='KnownVARclassification and differentcatalogperiod do not identify physicalcause of2.197daydimming.'))
print('passed')
