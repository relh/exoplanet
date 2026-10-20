from pathlib import Path
import json
from exoplanet.pipeline import save_json,sha,now
p=Path(__file__).parent;source=Path('results/weak-seed-ranks512-689-20261011');assert json.loads((source/'run.json').read_text())['status']=='complete';flags=[];positions={}
for f in (source/'targets').glob('*.json'):
 r=json.loads(f.read_text())
 if r.get('local_review_flag'):flags.append(r['tic']);s=r['selection']['target']['star'];positions[r['tic']]=(s['ra'],s['dec'])
template=Path('results/weak-seed-review-20261011/analyze.py');s=template.read_text().replace('[160163644,394877426,306680120]',repr(sorted(flags))).replace('weak-seed-pilot-20261011','weak-seed-ranks512-689-20261011');(p/'analyze.py').write_text(s)
q=Path('results/review-138558387-20261011/query.py');s=q.read_text().replace('positions={138558387:(174.380047638458,64.4291055901539)}','positions='+repr(positions));(p/'query.py').write_text(s)
s=Path('results/weak-seed-ranks32-64-review-20261011/verify.py').read_text().replace('diagnostic_windows_reproduced=6','diagnostic_windows_reproduced='+str(2*len(flags))).replace('catalog_response_hashes_checked=3','catalog_response_hashes_checked='+str(len(flags)));(p/'verify.py').write_text(s)
save_json(p/'selection.json',dict(created_utc=now(),source_run_sha256=sha(source/'run.json'),flagged_tics=sorted(flags),diagnostic_template_sha256=sha(template),query_template_sha256=sha(q),policy='Review every terminal local flag without further selection. Existing diagnostics and60arcsecond VSX cones. No exact identity from position alone.'))
print('flags',sorted(flags))
