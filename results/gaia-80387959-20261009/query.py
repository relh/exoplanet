from pathlib import Path
from exoplanet.pipeline import fetch,save_json
out=Path(__file__).parent
ids='5362389543781401216,5362389543781400192,5362389543781400960,5362389543778670592'
for table in ['vari_classifier_result','vari_eclipsing_binary','gaia_source']:
 q=f'select * from gaiadr3.{table} where source_id in ({ids})'
 try:
  p=Path(f'data/targeting/gaia-80387959-{table}.csv');meta=fetch('https://gea.esac.esa.int/tap-server/tap/sync',p,{'REQUEST':'doQuery','LANG':'ADQL','FORMAT':'csv','QUERY':q});save_json(out/f'{table}-source.json',meta);(out/f'{table}.csv').write_bytes(p.read_bytes())
 except Exception as exc:save_json(out/f'{table}-error.json',{'query':q,'error':repr(exc)})
