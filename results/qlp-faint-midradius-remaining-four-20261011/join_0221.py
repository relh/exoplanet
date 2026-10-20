"""Join immutable original/recovery snapshots without counting stars twice."""
from pathlib import Path
from collections import Counter
import json
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent
read=lambda p:json.loads(p.read_text())
ap=out/'checkpoint-0221.json'
bp=Path('results/qlp-faint-midradius-baseline-recovery-20261011/checkpoint-0043.json')
a=read(ap);b=read(bp)
errors={r['tic'] for r in a['inventory'] if r['status']=='error'}
assert errors=={r['tic'] for r in b['inventory']}
recovered={}
for r in b['inventory']:
    for p,h in r['artifacts'].items():assert sha(Path(p))==h
    if r['status']=='screened':
        p=next(Path(p) for p in r['artifacts'] if '/targets/' in p)
    else:
        assert r['tic']==309703302 and r['status']=='deferred_other_error'
        p=Path('results/qlp-faint-recovery-309703302-20261011/targets/309703302.json')
        v=read(p.parent.parent/'verification.json');assert v['result_sha256']==sha(p)
    result=read(p);assert result['status']=='screened'
    recovered[r['tic']]={'path':str(p),'sha256':sha(p),'disposition':result['disposition']}
rows=[]
for r in a['inventory']:
    assert sha(Path(r['path']))==r['sha256']
    usable=recovered[r['tic']] if r['tic'] in recovered else {k:r[k] for k in ['path','sha256','disposition']}
    rows.append({'tic':r['tic'],'original_path':r['path'],'original_sha256':r['sha256'],'usable':usable})
assert len(rows)==len({r['tic'] for r in rows})==221
counts=dict(Counter(r['usable']['disposition'] for r in rows))
save_json(out/'joined-0221.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'original_snapshot_sha256':sha(ap),'recovery_snapshot_sha256':sha(bp),'n_distinct_usable':221,'original_failures_retained':43,'counts':counts,'rows':rows,'limits':'These exact snapshot stars only. Alternate windows do not repair the original attempts or add stars. Flagged includes admitted diagnostic follow-ups, not confirmed planets. Whole campaign remains live.'})
print('221 distinct usable windows:',counts)
