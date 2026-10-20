from pathlib import Path
import json
from exoplanet.pipeline import save_json,sha,now
p=Path(__file__).parent;source=Path('results/weak-seed-pilot-20261011/eligible.json');eligible=json.loads(source.read_text());selected=eligible[8:32]
assert len(selected)==24
for row in selected:
 for s in row['added_sectors']+row['target']['heldout_sectors']:assert not Path(f"data/lightcurves/s{s:04d}-{row['tic']}.fits").exists()
save_json(p/'selected.json',selected);save_json(p/'plan.json',dict(created_utc=now(),source=str(source),source_sha256=sha(source),audit_sha256=sha(Path('results/solar-radius-lead-audit-20261011/audit.json')),selection_script_sha256=sha(Path(__file__)),selected_sha256=sha(p/'selected.json'),n_eligible=len(eligible),n_selected=24,policy='Continue original frozen weak-seed ranking, indices8:32 inclusive-exclusive. Same local refinement and review rule as original eight-star pilot, two windows, all early sectors<=55. No new selection based on added-data outcomes, no reserved sectors, no full-gate or calibrated significance claim.'))
