from pathlib import Path
import json,csv,io
from exoplanet.pipeline import sha,save_json,now
O=Path(__file__).parent;x=json.loads((O/'metadata.json').read_text());g=x['rows'][0];p=Path(g['source']['path']);assert sha(p)==g['source']['sha256'];rows=list(csv.DictReader(io.StringIO(p.read_text())));assert rows==g['rows'];assert rows[0]['source_id']=='6865254022910168320' and rows[0]['has_epoch_photometry']=='false' and rows[0]['phot_variable_flag']=='NOT_AVAILABLE';assert all(r['status']=='error' for r in x['rows'][1:])
paths=[Path('results/qlp-faint-midradius-single-remaining-20261011/targets/241928959.json'),Path('results/ffi-coverage-single-signals-20261011/results.json'),Path('results/ffi-coverage-single-signals-20261011/verification.json'),Path('results/ztf-original-clocks-two-20261011/ASSESSMENT.md'),Path('results/asassn-remaining-signals-20261011/ASSESSMENT.md')]
assert json.loads(paths[0].read_text())['target']['sectors']==[92]
ffi=next(r for r in json.loads(paths[1].read_text())['rows'] if r['tic']==241928959);assert ffi['status']=='complete' and ffi['sectors']==[92] and not ffi['additional_sectors']
save_json(O/'verification.json',dict(created_utc=now(),status='passed',script_sha256=sha(Path(__file__)),metadata_sha256=sha(O/'metadata.json'),local_evidence_sha256={str(p):sha(p) for p in paths},scope='Exact Gaia metadata response/identity/availability flag; retained ASAS-SN errors; QLP/TESScut coverage records and linked prior-evidence hashes. No flux, timing reanalysis, or all-survey coverage claim.'))
print('passed')
