"""Final discovery/recovery inventory, distinct from ongoing residual surveys."""
from pathlib import Path
from collections import Counter
import json
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent;root=Path('results/campaign-qlp-full-pool-20261010')
run=json.loads((root/'run.json').read_text());assert run['status']=='complete'
selection=json.loads(Path('results/qlp-full-pool-coverage-20261010/selected.json').read_text());ids={r['tic'] for r in selection};assert len(ids)==len(selection)==5619
rows={};inventory=[]
for p in (root/'targets').glob('*.json'):
 d=json.loads(p.read_text());rows[d['tic']]=d;inventory.append({'tic':d['tic'],'path':str(p),'sha256':sha(p),'kind':'original'})
assert set(rows)==ids
original_errors={tic for tic,d in rows.items() if d['status']=='error'};seen=set();recovered=[]
for name in ['qlp-full-pool-recovery1-20261010','qlp-full-pool-recovery2-20261010']:
 rroot=Path('results')/name;rr=json.loads((rroot/'run.json').read_text());assert rr['status']=='complete'
 for r in json.loads((rroot/'progress.json').read_text()):
  tic=r['tic'];assert tic in original_errors and tic not in seen;seen.add(tic)
  p=Path(r['attempts'][-1]['path']);d=json.loads(p.read_text());inventory.append({'tic':tic,'path':str(p),'sha256':sha(p),'kind':'recovery'})
  if r['resolved']:assert d['status']=='screened';rows[tic]=d;recovered.append(tic)
 # All remaining first-epoch failures were tested at second assigned SPOC epoch.
 second=json.loads((rroot/'spoc-second-results.json').read_text());assert all(x['status']=='error' for x in second)
assert seen==original_errors
review=[];counts=Counter()
resolved={378761120:'neighbor378761130_ZTF',240023401:'neighbor240023393_ZTF',286607959:'neighbor286608026_QLP',25324731:'neighbor25318752_QLP',314649431:'neighbor314649408_ZTF'}
for tic,d in rows.items():
 peaks=[i for i,p in enumerate(d.get('screened_peaks',[])) if set(p['flags'])<={'crowding_or_missing_crowding'}]
 label='review_pass' if peaks else d.get('disposition',d['status']);counts[label]+=1
 for i in peaks:
  dest=Path(f'results/qlp-full-pool-followup-20261010/{tic}-peak{i}');assert (dest/'heldout.json').exists() and (dest/'ASSESSMENT.md').exists()
  review.append({'tic':tic,'peak_index':i,'heldout_path':str(dest/'heldout.json'),'heldout_sha256':sha(dest/'heldout.json'),'assessment_path':str(dest/'ASSESSMENT.md'),'assessment_sha256':sha(dest/'ASSESSMENT.md'),'resolution':resolved.get(tic,'already_published_DTARPS' if tic==296179330 else 'unsupported_or_timing_inconclusive')})
terminal=Path('results/qlp-full-pool-followup-20261010/terminal.json');assert json.loads(terminal.read_text())['status']=='complete'
save_json(out/'audit.json',{'utc':now(),'n_selected':len(ids),'n_original_errors':len(original_errors),'n_recovered':len(recovered),'n_usable':sum(d['status']=='screened' for d in rows.values()),'classification_counts':dict(counts),'unusable_tics':[tic for tic,d in rows.items() if d['status']=='error'],'review':review,'review_resolution_counts':dict(Counter(r['resolution'] for r in review)),'selection_sha256':sha(Path('results/qlp-full-pool-coverage-20261010/selected.json')),'run_sha256':sha(root/'run.json'),'followup_terminal_sha256':sha(terminal),'inventory':inventory,'limits':'Unique-target accounting for this5619 selection only. Recovered single-sector coverage is narrower. Inconclusive timing is not planet exclusion. Residual surveys are separate and introduce additional trials. No completeness, calibrated FAP, novelty or likely-planet claim.'})
print(dict(counts),len(recovered),'recovered',len(review),'review peaks')
