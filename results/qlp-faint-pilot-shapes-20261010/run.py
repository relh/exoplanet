"""Training-only visual review of first three high-SNR flagged pilot targets."""
from pathlib import Path
from functools import partial
import json
from exoplanet.pipeline import save_json,sha,now
from exoplanet.qlp_campaign import load_qlp
from exoplanet.plots import plot_discovery
out=Path(__file__).parent
items=[]
for tic in [38698751,424389265,310128088]:
 p=Path(f'results/qlp-faint-pilot-20261010/targets/{tic}.json')
 r=json.loads(p.read_text())
 plot_discovery(p,out/f'{tic}.png',loader=partial(load_qlp,bin_minutes=0))
 items.append({'tic':tic,'discovery_path':str(p),'sha256':sha(p),'best':r['best'],'flags':r['screened_peaks'][0]['flags'],'training_sectors':r['target']['training_sectors']})
save_json(out/'review-inputs.json',{'utc':now(),'items':items,'policy':'Post-hoc training-only inspection of strong flagged signals. No new detection gate or independent validation. No heldout files opened.'})
