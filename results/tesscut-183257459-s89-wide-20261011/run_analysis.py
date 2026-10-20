from pathlib import Path
import subprocess
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent
for name in ['analyze','background']:
 script=out/f'{name}.py';r=subprocess.run(['uv','run','python',str(script)],capture_output=True,text=True)
 (out/f'{name}-stdout.txt').write_text(r.stdout);(out/f'{name}-stderr.txt').write_text(r.stderr)
 save_json(out/f'{name}-status.json',{'utc':now(),'script_sha256':sha(script),'exit_code':r.returncode})
 print(name,r.returncode,r.stdout or r.stderr,flush=True)
 if r.returncode:break
