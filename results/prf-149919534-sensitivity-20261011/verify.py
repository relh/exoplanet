from pathlib import Path
import itertools,json,numpy as np
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());p=read(out/'plan.json');r=read(out/'results.json');s=read(out/'summary.json');pm=read(out/'plot-manifest.json')
assert p['script_sha256']==sha(out/'run.py') and p['module_sha256']==sha(Path('src/exoplanet/prf_fit.py'))
for n,h in p['inputs'].items():assert sha(Path(n))==h
assert s['results_sha256']==pm['results_sha256']==sha(out/'results.json')
assert pm['script_sha256']==sha(out/'plot.py') and pm['plot_sha256']==sha(out/'controls.png')
rows=r['rows'];assert len(rows)==18 and {(x['dx'],x['dy'],x['width']) for x in rows}==set(itertools.product(*[p['grid'][k] for k in ['dx','dy','width']]))
assert len(r['attempts'])==36;good=[c for c in r['attempts'] if c['status']=='measured'];keys={c['window_id'] for c in good};assert len(good)==13 and len(keys)==8
assert len(r['reference_reproduction_errors'])==10 and max(r['reference_reproduction_errors'])<1e-8
for row in rows:
 assert len(row['controls'])==8 and {c['window_id'] for c in row['controls']}==keys
 assert {e['event'] for e in row['events']}=={1,2}
 for e in row['events']:
  assert {i['source'] for i in e['injections']}=={'149919534','149919536'}
 for fit in row['events']+row['controls']:
  assert fit['dof']==110 and np.isfinite(fit['chi2']) and all(np.isfinite(v) for v in fit['amplitudes'].values())
for report in s['events']:
 for src,a in report['sources'].items():
  es=[next(e['amplitudes'][src] for e in x['events'] if e['event']==report['event']) for x in rows];cs=[[c['amplitudes'][src] for c in x['controls']] for x in rows];flat=sum(cs,[])
  assert a['event_range']==[min(es),max(es)] and a['control_range']==[min(flat),max(flat)]
  assert a['above_same_model_control_max']==sum(e>max(c) for e,c in zip(es,cs))
  assert a['above_same_model_absolute_control']==sum(e>max(abs(v) for v in c) for e,c in zip(es,cs))
for source,report in s['injections'].items():
 inj=[i for row in rows for e in row['events'] for i in e['injections'] if i['source']==source]
 assert len(inj)==36
 for src,bounds in report.items():assert bounds==[min(i['amplitudes'][src] for i in inj),max(i['amplitudes'][src] for i in inj)]
save_json(out/'verification.json',{'script_sha256':sha(Path(__file__)),'results_sha256':sha(out/'results.json'),'summary_sha256':sha(out/'summary.json'),'status':'18 models,36 event fits,144 distinct-window/model controls,72 cross-model injections and10 reference reproductions checked. Not astrophysical validation.'})
print('Verified complete grid, injection accounting, reference reproduction and provenance.')
