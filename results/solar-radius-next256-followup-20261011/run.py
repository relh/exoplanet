from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from exoplanet.followup import follow_target
from exoplanet.pipeline import sha,save_json,now
p=Path(__file__).parent;tics=[396160833,34576133]
for tic,s in [(396160833,79),(34576133,85)]:assert not Path(f'data/lightcurves/s{s:04d}-{tic}.fits').exists()
save_json(p/'plan.json',dict(created_utc=now(),tics=tics,source_sha256=sha(Path('src/exoplanet/followup.py')),policy='Peak0 only; original discovery sectors, no expansion. Existing refinement writes frozen timing before opening reserved product. No posthoc retiming of reserved data.'))
def run(tic):
 checks=follow_target(Path(f'results/solar-radius-next256-20261011/targets/{tic}.json'),p/str(tic),peak_index=0,max_sectors=1)
 return dict(tic=tic,checks=checks)
with ThreadPoolExecutor(max_workers=2) as pool:rs=list(pool.map(run,tics))
save_json(p/'results.json',rs);print([(r['tic'],[(q.get('conclusion'),q.get('error')) for q in r['checks']]) for r in rs])
