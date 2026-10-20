from pathlib import Path
import requests,json,hashlib,datetime
O=Path(__file__).parent;D=Path('data')/O.name
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
url='https://academic.oup.com/mnras/article/373/1/231/1378493'
r=requests.get(url,timeout=60);p=D/'pont2006.html';p.write_bytes(r.content)
lit=dict(url=url,status=r.status_code,path=str(p),sha256=sha(p),retrieved_utc=datetime.datetime.now(datetime.UTC).isoformat())
(O/'literature.json').write_text(json.dumps(lit,indent=2))
plan=dict(created_utc=datetime.datetime.now(datetime.UTC).isoformat(),target=80387959,duration_days=.092736,sectors=[10,36,37,63,90,100],inputs=[dict(path=str(p),sha256=sha(p)) for p in sorted(Path('results/strongest-80387959-shape-20261012').glob('*primary.npz'))],method='Pont2006-inspired time-averaging of joint box+event-baseline residuals. White reference generated and refitted at same timestamps/errors/design. No new clock/duration/flux access. Diagnostic uncertainty sensitivity, not calibrated coverage or FAP.',widths_duration=[.5,1,2],offset_fractions=[0,.5],gap_cadences=1.5,min_bins=8,white_simulations=2000,seed=80387959,beta='max(1, observed RMS of bin means / RMS of same statistic over white residual simulations); take maximum over all declared widths and offsets. Formal white errors retain original residual-scale floor. Global beta rescales conditional depth error.',bins='Equal-count bins N=round(width/cadence), min2; split at event boundary or gap>1.5 median cadence. Offset floor(offset*N) independently per segment; discard incomplete bins. Never bridge gaps. Residuals include in-transit points with fitted box removed.',event_influence='Refit each single-event omission; recompute all betas and inflated errors.',tests='Noiseless zero and +/-1000ppm injection recovery on every design. Deterministic 200-replicate iid and AR1(phi=.85) simulations on representative sector90 with resets per contiguous segment; evaluate beta response and fixed-depth error scatter. All failures retained.')
(O/'plan.json').write_text(json.dumps(plan,indent=2))
print(lit)
