"""Summarize terminal recovery controls and retain actual search bounds."""
from pathlib import Path
import json
from astropy.timeseries import BoxLeastSquares
from exoplanet.campaign import DURATIONS
from exoplanet.pipeline import save_json, sha, now

out=Path(__file__).parent
summary=[]
for name in ['injections','long-injections']:
    folder=Path(f'results/qlp-faint-midradius-next32-recovery-{name}-20261011')
    audit=folder/'audit.json'
    a=json.loads(audit.read_text())
    assert a['terminal'] and a['n_completed']==12 and a['n_errors']==0
    bounds=[]
    for r in a['rows']:
        p=Path(r['path']);z=json.loads(p.read_text());b=z['clean_baseline_days']
        assert sha(p)==r['source_sha256']
        grid=BoxLeastSquares([0,b],[1,1]).autoperiod(DURATIONS,minimum_period=.5,maximum_period=min(20,b/2.5),frequency_factor=2)
        bounds.append({'tic':r['tic'],'period':r['period'],'radius_earth':r['radius_earth'],'baseline_days':b,'nominal_max_period':min(20,b/2.5),'grid_min':float(min(grid)),'grid_max':float(max(grid)),'in_grid':float(min(grid))<=r['period']<=float(max(grid)),'result_sha256':sha(p)})
    save_json(folder/'bounds.json',{'utc':now(),'audit_sha256':sha(audit),'rows':bounds})
    timed=lambda r:any(m['within_half_injected_duration_at_three_times'] for m in r['matches'])
    passes=[r for r in a['rows'] if r['noncrowding_screen_pass'] and timed(r)]
    eq=list(folder.glob('*-baseline-equivalence.json'))
    assert len(eq)==3
    for p in eq:
        d=json.loads(p.read_text());assert d['exact_arrays_equal'] and d['windows']==[1.5,2.5]
    item={'family':name,'audit_sha256':sha(audit),'n_completed':12,'n_in_grid':sum(r['in_grid'] for r in bounds),'n_period':a['n_top3_period_recovered'],'n_phase':sum(timed(r) for r in a['rows']),'n_screen_pass':a['n_noncrowding_pass'],'n_screen_and_phase_pass':len(passes),'passing_trials':[{'tic':r['tic'],'period':r['period'],'radius_earth':r['radius_earth']} for r in passes],'baseline_hashes':{str(p):sha(p) for p in eq}}
    summary.append(item);print(item)
save_json(out/'control_summary.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'families':summary,'limits':'Three frozen targets, one phase/duration per family. Existing variability retained. No completeness or calibrated discovery confidence.'})
