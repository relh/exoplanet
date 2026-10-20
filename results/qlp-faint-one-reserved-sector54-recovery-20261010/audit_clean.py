"""Inspect failure-frame sample counts without changing loader or quality gates."""
from pathlib import Path
import json
from exoplanet.pipeline import save_json,sha,now
from exoplanet.qlp_campaign import load_qlp
for tic in [244056649,404172362]:
 out=Path(__file__).parent/str(tic);plan=json.loads((out/'plan.json').read_text())
 try:
  load_qlp(plan['target'],Path('data'))
  raise AssertionError('Expected original insufficient-cadence failure')
 except ValueError as exc:
  assert str(exc)=='Fewer than 200 clean cadences'
  tb=exc.__traceback__;frames=[]
  while tb:
   frame=tb.tb_frame
   if frame.f_code.co_name=='flatten':
    frames.append({'file':frame.f_code.co_filename,'line':tb.tb_lineno,'n_clean':len(frame.f_locals['t'])})
   tb=tb.tb_next
  assert len(frames)==1 and frames[0]['n_clean']<200
  save_json(out/'clean-cadence-audit.json',{'utc':now(),'tic':tic,'script_sha256':sha(Path(__file__)),'plan_sha256':sha(out/'plan.json'),'loader_sha256':sha(Path('src/exoplanet/qlp_campaign.py')),'flatten_sha256':sha(Path('src/exoplanet/search.py')),'error':str(exc),'frames':frames,'policy':'Read exception frame count from exact original loader; no algorithm, threshold, array, or reserved sector changed.'})
  print(tic,frames)
