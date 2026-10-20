from pathlib import Path
import subprocess
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent
args=['uv','run','python','-m','exoplanet.pixel_vet','--tic','74189224','--sector','103','--frozen','results/qlp-faint-midradius-remaining-two-coverage-followup-20261011/74189224-peak0/frozen.json','--neighbors','results/neighbors-74189224-20261011/neighbors.json','--output',str(out/'analysis')]
assert not (out/'plan.json').exists()
save_json(out/'plan.json',{'utc':now(),'args':args,'script_sha256':sha(Path(__file__)),'policy':'Same-sector SPOC processed target pixel diagnostic at frozen QLP fit. Same photons, different processing; not an independent epoch or automatic host proof.'})
r=subprocess.run(args,capture_output=True,text=True);(out/'stdout.txt').write_text(r.stdout);(out/'stderr.txt').write_text(r.stderr);save_json(out/'status.json',{'utc':now(),'exit_code':r.returncode});print(r.stdout or r.stderr)
