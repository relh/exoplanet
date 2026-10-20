from pathlib import Path
import json,numpy as np
from astropy.io import fits
from exoplanet.archive import qlp_flux_columns
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;rows=[]
checkpoint={'inventory':[{'path':str(p),**json.loads(p.read_text())} for p in (out/'targets').glob('*.json')]}
for item in checkpoint['inventory']:
 if item['status']!='error':continue
 tic=item['tic'];target=json.loads(Path(item['path']).read_text())['target']
 for sector in target['training_sectors']:
  result=out/'targets'/f'{tic}.json';r=json.loads(result.read_text());assert r['status']=='error';p=Path(f'data/qlp/{tic}-s{sector:04d}.fits')
  if not p.exists():
   rows.append({'tic':tic,'sector':sector,'status':'cache_absent_after_earlier_failure','error':r['error'],'result_sha256':sha(result)});continue
  with fits.open(p) as h:
   d=h[1].data;fc,ec,_=qlp_flux_columns(d.names);q=d['QUALITY']==0;t=np.asarray(d['TIME']);f=np.asarray(d[fc]);e=np.asarray(d[ec]);usable=q&np.isfinite(t)&np.isfinite(f)&(f>0)
   rows.append({'tic':tic,'sector':sector,'error':r['error'],'result_sha256':sha(result),'raw_sha256':sha(p),'flux_column':fc,'error_column':ec,'n_rows':len(d),'quality_zero':int(q.sum()),'finite_selected_flux':int(np.isfinite(f).sum()),'finite_selected_errors':int(np.isfinite(e).sum()),'usable_positive_flux_q0':int(usable.sum())})
save_json(out/'errors.json',{'script_sha256':sha(Path(__file__)),'rows':rows,'limits':'Audit of currently recorded failed inputs. No replacement by reserved data, no nondetection inference.'});print(rows)
