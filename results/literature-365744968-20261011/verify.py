from pathlib import Path
import json,re,subprocess
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent
raw=Path('data/literature/bell-2017-32ori.pdf')
source=json.loads((out/'source.json').read_text());assert sha(raw)==source['sha256']
np=Path('results/neighbors-365744968-20261011/neighbors.json')
star=next(r for r in json.loads(np.read_text()) if r['ID']==365744968)
assert star['TWOMASS']=='05264886+0928055'
txt=subprocess.check_output(['pdftotext','-layout',str(raw),'-'],text=True)
rows=[line.split() for line in txt.splitlines() if '05264886+0928055' in line]
assert len(rows)==1
r=rows[0];assert r[0]=='28' and r[-5:]==['M4','−3.9','<70','Y,?,?','Y'],r
assert '24 ± 4 Myr' in txt
save_json(out/'verification.json',{'script_sha256':sha(Path(__file__)),'raw_sha256':sha(raw),'tic_neighbors_sha256':sha(np),'tic':365744968,'twomass':star['TWOMASS'],'THOR':28,'table':3,'spectral_type':r[-5],'Halpha_EW_A':-3.9,'final_membership':'Y','reported_group_age_Myr':24,'reported_group_age_statistical_error_Myr':4,'limits':'Exact catalog alternate-name match. Group membership and Halpha emission do not establish the origin or period of the TESS signal. No planet or eclipsing-binary classification inferred.'})
print('Verified exact 2MASS identity and Table 3 classification.')
