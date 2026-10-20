from pathlib import Path
import json,hashlib,datetime,requests,sys
import numpy as np
R=Path('results/triceratops-20261013');D=Path('data/triceratops-20261013')
for tic in (list(map(int,sys.argv[1:])) or [80387959,402358350]):
 import pandas as pd
 a=pd.read_csv(R/f'{tic}-stars-original.csv').iloc[0]
 q=f"SELECT phot_g_mean_mag, phot_bp_mean_mag, phot_rp_mean_mag, parallax, parallax_over_error FROM gaiadr3.gaia_source WHERE 1 = CONTAINS(POINT('ICRS', ra, dec), CIRCLE('ICRS', {a.ra}, {a.dec}, {np.sqrt(.1/np.pi)})) AND phot_g_mean_mag < 21.0"
 url='https://gea.esac.esa.int/tap-server/tap/sync';resp=requests.post(url,data={'REQUEST':'doQuery','LANG':'ADQL','FORMAT':'csv','QUERY':q},timeout=180);p=D/f'{tic}-gaia-raw.csv';p.write_bytes(resp.content);out=dict(url=url,adql=q,status=resp.status_code,path=str(p),sha256=hashlib.sha256(resp.content).hexdigest(),retrieved_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),note='Independent repeat of package query; transformed population actually used is separately hashed.');(R/f'{tic}-gaia-raw-provenance.json').write_text(json.dumps(out,indent=2));print(tic,resp.status_code,len(resp.content),flush=True)
