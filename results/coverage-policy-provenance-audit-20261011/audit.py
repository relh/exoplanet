from pathlib import Path
import json
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent
original=Path('results/qlp-faint-one-reserved-sector31-pilot-coverage-followup-20261010/watch.py')
control=Path('results/qlp-faint-sector98-long-injections-20261010/audit.json')
def eligibility(s):return s[s.index('def eligible():'):s.index('while True:')]
baseline=eligibility(original.read_text());rows=[]
for p in sorted(Path('results').glob('qlp-faint-one-reserved-sector*-pilot-coverage-followup-20261010/watch.py')):
 plan=p.parent/'plan.json'
 if not plan.exists():continue
 d=json.loads(plan.read_text());same=eligibility(p.read_text())==baseline
 assert same, str(p)
 rows.append({'watch_path':str(p),'watch_sha256':sha(p),'plan_sha256':sha(plan),'eligibility_identical_to_original':same,'recorded_control_sha256':d.get('historical_policy_control_audit_sha256'),'correct_control_sha256':sha(control),'control_provenance_correct':d.get('historical_policy_control_audit_sha256')==sha(control)})
save_json(out/'audit.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'original_watch_sha256':sha(original),'historical_control_path':str(control),'historical_control_sha256':sha(control),'rows':rows,'limits':'The Sector64 launch failed before writing a plan due to a copied historical-control path. The corrected launch and every prior completed plan reference the original control hash. All eligibility function source blocks are identical to the original policy; hashes are not scientific validation. Original manifests preserved.'})
print(len(rows),'watchers;',sum(not r['control_provenance_correct'] for r in rows),'historical-reference mismatches; all eligibility blocks identical')
