"""Verify all forty original data failures without relaxing search eligibility."""
from pathlib import Path
import json
import numpy as np
from astropy.io import fits
from exoplanet.pipeline import sha,save_json,now
from exoplanet.archive import qlp_flux_columns
from exoplanet.integrity import verify_hdus
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text())
plan=read(out/'plan.json');terminal=read(out/'terminal.json')
assert terminal['script_sha256']==sha(out/'run.py') and terminal['plan_sha256']==sha(out/'plan.json')
assert all(r['exit_code']==0 for r in terminal['rows'])
assert {r['tic'] for r in terminal['rows']}==set(plan['targets'])
rows=[]
for tic in plan['targets']+plan['already_reviewed']:
 p=Path(f'results/qlp-faint-recovery-{tic}-20261011');a=read(p/'plan.json');checks=read(p/'sector-checks.json');sel=read(p/'selection.json');result=read(p/'result.json')
 assert sha(Path(a['original_path']))==a['original_sha256'] and sha(p/'run.py')==a['script_sha256']
 assert [r['sector'] for r in checks]==a['target']['training_sectors']
 assert sel['sector_checks_sha256']==sha(p/'sector-checks.json')
 assert sel['usable_sectors']==[r['sector'] for r in checks if r['status']=='usable']
 assert len(sel['usable_sectors'])==1 and sel['target'] is None
 assert result['status']=='insufficient_training_coverage' and not (p/'targets').exists()
 assert all(not Path(f'data/qlp/{tic}-s{s:04d}.fits').exists() for s in a['target']['heldout_sectors'])
 raw_rows=[]
 for r in checks:
  raw=Path(f"data/qlp/{tic}-s{r['sector']:04d}.fits");assert sha(raw)==r['raw_sha256']==r['download_provenance']['sha256']
  with fits.open(raw) as h:
   assert h[0].header['TICID']==tic and h[0].header['SECTOR']==r['sector']
   integrity=verify_hdus(raw,h);d=h[1].data;fc,ec,_=qlp_flux_columns(d.names)
   item={'sector':r['sector'],'raw_sha256':sha(raw),'n_rows':len(d),'flux_column':fc,'finite_flux':int(np.isfinite(d[fc]).sum()),'status':r['status'],'n_clean':r.get('n_clean'),'error':r.get('error'),'integrity':integrity}
   if r['status']=='error' and 'Insufficient adjacent samples' in r['error']:assert item['finite_flux']==0
   raw_rows.append(item)
 rows.append({'tic':tic,'original_path':a['original_path'],'original_sha256':a['original_sha256'],'result_path':str(p/'result.json'),'result_sha256':sha(p/'result.json'),'selection_sha256':sha(p/'selection.json'),'checks_sha256':sha(p/'sector-checks.json'),'raw':raw_rows})
assert len(rows)==len({r['tic'] for r in rows})==40
save_json(out/'verification.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'rows':rows,'limits':'Forty original data failures: each has one usable assigned sector; no new period search or reserved-sector access. Twenty-two empirical-error failures have no finite archived selected flux. The other eighteen fail unchanged clean-cadence requirements. These are coverage failures, not transit nondetections.'})
print('Verified 40 insufficient-coverage cases, including raw identity and hashes.')
