"""Check completed recovery attempts without treating a live stream as terminal."""
from pathlib import Path
from collections import Counter
import json
from exoplanet.pipeline import sha,save_json,now

out=Path(__file__).parent
read=lambda p:json.loads(p.read_text())
plan=read(out/'plan.json')
assert sha(out/'watch.py')==plan['script_sha256']
for name,h in plan['source_sha256'].items():assert sha(Path('src/exoplanet')/name)==h
inventory=[]
for p in sorted(out.glob('*/result.json')):
    try:r=read(p)
    except json.JSONDecodeError:continue
    assert r['finished_utc']
    original=Path(r['original_path']);a=read(original)
    assert sha(original)==r['original_sha256'] and a['status']=='error'
    artifacts={str(p):sha(p),str(p.parent/'plan.json'):sha(p.parent/'plan.json')}
    if r['status']=='screened':
        selpath=p.parent/'selection.json';sel=read(selpath)
        resultpath=Path(r['result_path']);b=read(resultpath)
        assert sha(resultpath)==r['result_sha256']
        assert b['target']==sel['chosen'] and b['target']['heldout_sectors']==a['target']['heldout_sectors']
        assert a['finished_utc']<=sel['utc']<=b['started_utc']
        assert sel['options'][-1]['training_sectors']==b['target']['training_sectors']
        assert sel['options'][-1]['clean_baseline_days']<=120
        assert all(o.get('clean_baseline_days',float('inf'))>120 for o in sel['options'][:-1])
        assert not sel['reserved_cached_before_recovery']
        assert b['target']['training_sectors']==a['target']['training_sectors'][-len(b['target']['training_sectors']):]
        for raw in sel['raw']:assert sha(Path(raw['path']))==raw['sha256']
        for ev in b['data']:assert sha(Path(f"data/qlp/{r['tic']}-s{ev['sector']:04d}.fits"))==ev['source']['sha256']
        artifacts.update({str(selpath):sha(selpath),str(resultpath):sha(resultpath)})
        if not r['followups']:
            assert all(not Path(f"data/qlp/{r['tic']}-s{s:04d}.fits").exists() for s in b['target']['heldout_sectors'])
        for follow in r['followups']:
            fd=Path(follow['directory'])
            for name in ['frozen.json','heldout.json','discovery.png','secondary.json']:
                assert (fd/name).exists();artifacts[str(fd/name)]=sha(fd/name)
    inventory.append({'tic':r['tic'],'status':r['status'],'disposition':r.get('disposition'),'n_followups':len(r.get('followups',[])),'artifacts':artifacts})
dest=out/f'checkpoint-{len(inventory):04d}.json';assert not dest.exists()
counts=dict(Counter(r['disposition'] or r['status'] for r in inventory))
save_json(dest,{'utc':now(),'plan_sha256':sha(out/'plan.json'),'script_sha256':sha(Path(__file__)),
    'n_completed':len(inventory),'counts':counts,'inventory':inventory,
    'limits':'Completed-file snapshot, not terminal stream evidence. Original failed attempts remain failures. Recovery adds windows, not stars. Plots and follow-up artifacts require separate scientific review.'})
print(dest,counts)
