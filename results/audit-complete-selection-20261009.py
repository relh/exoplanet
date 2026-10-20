"""Verify the full selected population against immutable original/recovery records."""
import json
from pathlib import Path
from exoplanet.pipeline import sha,save_json,now
selection=Path('results/selection-small-stars-20261009/eligible.json');selected=json.loads(selection.read_text());expected={r['tic'] for r in selected};assert len(expected)==len(selected)==11851
old=Path('results/checkpoint-7000-20261009.json');prior=json.loads(old.read_text());runs=[Path(r['path']) for r in prior['runs']]
for entry in prior['runs']:assert sha(Path(entry['path'])/'run.json')==entry['run_sha256']
runs += [Path(f'results/campaign-small-stars-batch{b}-20261009') for b in ['9','9-resume','10','10-resume','11','12','13']]
manifest=[];attempted=set();spoc=set();qlp=set();priorities=[];records={}
for root in runs:
 run=json.loads((root/'run.json').read_text());interrupted=(root/'interruption.json').exists()
 if interrupted:
  # Original terminated manifests intentionally retain historical running status.
  interruption=json.loads((root/'interruption.json').read_text())
 else:assert run['status']=='complete',f'Not complete: {root}'
 paths=sorted((root/'targets').glob('*.json'));n_errors=0
 for p in paths:
  row=json.loads(p.read_text());tic=row['tic'];attempted.add(tic);records[str(p)]=sha(p)
  if row['status']!='screened':n_errors+=1;continue
  isqlp=any(d['star'].get('collection')=='QLP' for d in row['data']);(qlp if isqlp else spoc).add(tic)
  for i,peak in enumerate(row['screened_peaks']):
   if not peak['flags']:priorities.append({'tic':tic,'peak_index':i,'source':str(p),'period':peak['best']['period'],'note':'Automated pass only, not a planet candidate'})
 manifest.append({'path':str(root),'run_sha256':sha(root/'run.json'),'interruption_sha256':sha(root/'interruption.json') if interrupted else None,'n_records':len(paths),'n_original_errors':n_errors})
assert attempted==expected,{'missing':sorted(expected-attempted),'extra':sorted(attempted-expected)}
assert spoc|qlp==expected,{'no_usable_search':sorted(expected-(spoc|qlp))}
for b in [9,10]:
 a={int(p.stem) for p in Path(f'results/campaign-small-stars-batch{b}-20261009/targets').glob('*.json')};r={int(p.stem) for p in Path(f'results/campaign-small-stars-batch{b}-resume-20261009/targets').glob('*.json')}
 assert not a&r and len(a|r)==1000
out=Path('results/checkpoint-11851-20261009.json');assert not out.exists(),'Do not overwrite checkpoint'
save_json(out,{'created_utc':now(),'script_sha256':sha(Path(__file__)),'selection_sha256':sha(selection),'prior_checkpoint_sha256':sha(old),'n_unique_selected':len(expected),'n_unique_with_usable_search':len(spoc|qlp),'n_with_spoc_search':len(spoc),'n_only_qlp':len(qlp-spoc),'runs':manifest,'record_sha256':records,'automated_passes':priorities,'limitations':'All selected stars searched in assigned discovery sectors, not every sector/period or an exhaustive survey. Original failures and terminations retained; recovery runs supply missing usable searches. Known-catalog filtering and heuristic screen passes do not establish novelty or planethood. Source localization, independent recovery and manual reviews are separate evidence.'})
print('VERIFIED',len(expected),'stars;',len(spoc),'SPOC;',len(qlp-spoc),'QLP-only')
