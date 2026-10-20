from pathlib import Path
import subprocess
from exoplanet.pipeline import save_json,sha
out=Path(__file__).parent
for parity in [0,1]:
 args=['uv','run','python','-m','exoplanet.pixel_vet','--tic','429034844','--sector','70','--frozen',str(out/f'frozen-{parity}.json'),'--neighbors','results/neighbors-429034844-20261011/neighbors.json','--output',str(out/f'parity-{parity}')]
 r=subprocess.run(args,capture_output=True,text=True)
 (out/f'stdout-{parity}.txt').write_text(r.stdout);(out/f'stderr-{parity}.txt').write_text(r.stderr)
 save_json(out/f'status-{parity}.json',{'args':args,'exit_code':r.returncode,'script_sha256':sha(Path(__file__))});print(r.stdout or r.stderr);assert r.returncode==0
