from pathlib import Path
import json,numpy as np
from exoplanet.pipeline import sha,save_json
p=Path(__file__).parent;r=json.loads((p/'results.json').read_text());summaries={}
for path,digest in r['inputs'].items():assert sha(Path(path))==digest
for row in r['objects']:
 z=np.load(p/f"{row['oid']}-timing.npz");assert len(z['hmjd'])==row['n']
 np.testing.assert_allclose(z['combined_heuristic'],z['conditional_spread']+abs(z['btjd_assume_utc']-z['btjd_assume_tdb'])+1/86400)
 m=(z['combined_heuristic']<row['half_duration_days']) & (not row['search_boundary_hit']);assert np.array_equal(m,z['timing_useful']);assert m.sum()==row['n_timing_useful']
 phase=abs(z['phase_assume_utc']);assert ((phase<row['half_duration_days'])&m).sum()==row['n_nominal_in_window_useful']
 s=summaries.setdefault(row['tic'],{'n':0,'timing_useful':0,'nominal_inside':0,'inside_under_full_heuristic':0,'potentially_inside_under_heuristic':0})
 s['n']+=row['n'];s['timing_useful']+=int(m.sum());s['nominal_inside']+=row['n_nominal_in_window_useful'];s['inside_under_full_heuristic']+=int((m&(phase+z['combined_heuristic']<row['half_duration_days'])).sum());s['potentially_inside_under_heuristic']+=int((m&(phase-z['combined_heuristic']<row['half_duration_days'])).sum())
save_json(p/'verification.json',{'summary':summaries,'artifacts':{q.name:sha(q) for q in p.iterdir() if q.is_file() and q.name!='verification.json'},'limits':'Mask and arithmetic verification; physical timing scale still unverified. Inside labels are conditional heuristic coverage, not independent detections.'});print(summaries)
