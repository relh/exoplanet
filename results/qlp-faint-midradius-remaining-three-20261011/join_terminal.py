from pathlib import Path
from collections import Counter
import json
from exoplanet.pipeline import sha,save_json,now
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());a=read(out/'checkpoint-1493.json');summaries={r['tic']:r for r in read(out/'results.json')};assert len(summaries)==1493
recovered={}
for tic in [62900968,358566081,116255113,63168863,19065157,323712477]:
 p=Path(f'results/qlp-faint-recovery-{tic}-20261011');q=p/'targets'/f'{tic}.json';assert read(p/'verification.json')['result_sha256']==sha(q);recovered[tic]=q
for r in read(Path('results/qlp-faint-network-retry-three-20261011/verification.json'))['rows']:
 p=Path(r['path']);assert sha(p)==r['sha256'];recovered[r['tic']]=p
errors={r['tic'] for r in a['inventory'] if r['status']=='error'};assert set(recovered)|{271946735}==errors
rows=[]
for r in a['inventory']:
 p=Path(r['path']);d=read(p);assert sha(p)==r['sha256'] and {k:d.get(k) for k in summaries[r['tic']]}==summaries[r['tic']]
 q=recovered.get(r['tic'],p if r['status']!='error' else None)
 rows.append({'tic':r['tic'],'original_path':str(p),'original_sha256':sha(p),'usable_path':str(q) if q else None,'usable_sha256':sha(q) if q else None,'disposition':read(q)['disposition'] if q else 'insufficient_training_coverage'})
expected={(r['tic'],r['screened_peak_index']) for r in a['review']};seen=set();terminal_hashes={}
for tier in ['three-followup','three-coverage-followup']:
 p=Path(f'results/qlp-faint-midradius-remaining-{tier}-20261011/terminal.json');b=read(p);assert b['status']=='complete'
 for r in b['records']:assert r['status']=='complete';seen.add((r['tic'],r['peak_index']))
 terminal_hashes[str(p)]=sha(p)
assert seen==expected
p=Path('results/qlp-faint-midradius-three-baseline-recovery-20261011/terminal.json');b=read(p);assert b['status']=='complete' and {r['tic'] for r in b['records']}==errors;terminal_hashes[str(p)]=sha(p)
counts=dict(Counter(r['disposition'] for r in rows));assert len(rows)==len({r['tic'] for r in rows})==1493
save_json(out/'joined-terminal.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'original_counts':a['counts'],'counts':counts,'n_distinct_stars':len(rows),'n_distinct_usable':sum(r['usable_path'] is not None for r in rows),'rows':rows,'terminal_hashes':terminal_hashes,'observed_exit_codes':{'26063':0,'61664':0,'97813':0,'48901':0},'limits':'Original11failures retained; six reduced-window recoveries and four unchanged network retries counted once. One target lacks usable coverage. Batch completion is not survey completeness or planet validation; follow-up scientific review remains ongoing.'})
print(counts)
