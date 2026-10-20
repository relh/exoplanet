from pathlib import Path
import subprocess
from exoplanet.pipeline import save_json,sha,now
p=Path(__file__).parent
r=subprocess.run(["uv","run","python",str(p/"analyze.py")],capture_output=True,text=True)
(p/"stdout.txt").write_text(r.stdout);(p/"stderr.txt").write_text(r.stderr)
save_json(p/"status.json",{"utc":now(),"exit_code":r.returncode,"script_sha256":sha(p/"analyze.py")})
print(r.stdout or r.stderr)
