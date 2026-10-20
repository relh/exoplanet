from pathlib import Path
import csv
from exoplanet.pipeline import fetch,save_json,now
O=Path(__file__).parent
q="select table_name,column_name,unit,description from TAP_SCHEMA.columns where table_name='gaiadr3.dr2_neighbourhood' and column_name='angular_distance'"
p=Path('data/catalogs/gaia-402358350-scene-metadata-20261011.csv')
s=fetch('https://gea.esac.esa.int/tap-server/tap/sync',p,{'REQUEST':'doQuery','LANG':'ADQL','FORMAT':'csv','QUERY':q})
save_json(O/'metadata.json',dict(query=q,path=str(p),source=s,rows=list(csv.DictReader(p.open()))))
