from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import subprocess,json
from exoplanet.pipeline import sha,save_json,now
out=Path(__file__).parent;plan=json.loads((out/'plan.json').read_text())
assert not (out/'terminal.json').exists()
def run(tic):
 p=Path(f'results/qlp-faint-recovery-{tic}-20261011');script=p/'run.py'
 r=subprocess.run(['uv','run','python',str(script)],capture_output=True,text=True)
 (p/'stdout.txt').write_text(r.stdout);(p/'stderr.txt').write_text(r.stderr)
 row={'tic':tic,'script_sha256':sha(script),'exit_code':r.returncode,'utc':now()};save_json(p/'status.json',row)
 print(tic,r.returncode,r.stdout.strip().replace('\n','; '),flush=True);return row
with ThreadPoolExecutor(max_workers=4) as pool:rows=list(pool.map(run,plan['targets']))
save_json(out/'terminal.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'plan_sha256':sha(out/'plan.json'),'rows':rows})
