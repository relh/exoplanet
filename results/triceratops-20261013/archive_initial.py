from pathlib import Path
import time,json,shutil
R=Path('results/triceratops-20261013');D=R/'original-catalog';D.mkdir(exist_ok=True)
while not (R/'80387959-N100000-seed29-noise1-none.json').exists():time.sleep(2)
paths=[]
for glob in ['*-N10000-*','80387959-N100000-seed13-*','80387959-N100000-seed29-*','*-smoke.log']:
 for p in list(R.glob(glob)):
  if p.is_file():shutil.move(str(p),str(D/p.name));paths.append(str(D/p.name))
(R/'superseded-runs.json').write_text(json.dumps({'files':paths,'reason':'Catalog duplicate correction;803fractioneffectnegligible but rerunconsistently.402physicallydoublecountedsource. Archived outputsdiagnostic only.'},indent=2))
