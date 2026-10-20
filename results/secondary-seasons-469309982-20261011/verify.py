from pathlib import Path
import json,numpy as np
from exoplanet.pipeline import sha,save_json
from exoplanet.campaign import load_training
p=Path(__file__).parent;plan=json.loads((p/'plan.json').read_text());b=plan['clock'];rows=json.loads((p/'results.json').read_text())['rows'];assert len(rows)==12
assert sha(p/'run.py')==plan['script_sha256'];assert sha(Path('results/source-check-469309982-20261011/frozen.json'))==plan['frozen_sha256']
for path,h in plan['raw_hashes'].items():assert sha(Path(path))==h
for r in rows:
 t,y,e,_=load_training(dict(tic=469309982,training_sectors=r['sectors']),Path('data'),window=r['window']);epoch=b['transit_time']+(b['period']/2 if r['component']=='half_phase' else 0);phase=(t-epoch+b['period']/2)%b['period']-b['period']/2;inside=abs(phase)<b['duration']/2;outside=(abs(phase)>b['duration'])&(abs(phase)<min(3*b['duration'],b['period']/2));wi=1/e[inside]**2;wo=1/e[outside]**2;d=np.dot(wo,y[outside])/wo.sum()-np.dot(wi,y[inside])/wi.sum();error=np.sqrt(1/wi.sum()+1/wo.sum());m=r['measurement']['total'];np.testing.assert_allclose([d,error,d/error],[m['depth'],m['error'],m['snr']],rtol=1e-8,atol=1e-10);assert inside.sum()==m['n']
save_json(p/'verification.json',dict(status='passed',independent_weighted_total_measurements=12,raw_hashes_checked=True,limits='Totals independently reconstructed; preprocessing shares implementation. No event-level independent reconstruction or calibrated significance.'))
