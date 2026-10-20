from pathlib import Path
import json,re,subprocess
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;meta=json.loads((out/'oddo2025-source.json').read_text());p=Path(meta['path']);assert sha(p)==meta['source']['sha256']
text=subprocess.check_output(['pdftotext','-layout',str(p),'-'],text=True)
assert 'HIGH RUWE SYSTEMS' in text and '(days)' in text
m=re.search(r'^58464534\s+(2\.800456)\s+(0\.0612)\s+(1\.5415)\s*$',text,re.M);assert m
fp=Path('results/qlp-faint-midradius-remaining-one-followup-20261011/58464534-peak0/frozen.json');f=json.loads(fp.read_text());period=float(m[1]);twice=2*f['best']['period']
save_json(out/'verification.json',{'script_sha256':sha(Path(__file__)),'pdf_sha256':sha(p),'frozen_sha256':sha(fp),'tic':58464534,'table':4,'catalog_period_days':period,'our_twice_period_days':twice,'difference_days':period-twice,'limits':'Exact TIC row in Oddo et al. arXiv2508.13941v2 Table4, a subset of their eclipsing-binary catalog. Near doubled-period match, not exact epoch confirmation. Gan2023 download failed403 and is not used as verified primary evidence.'})
print('Verified literature row; doubled-period difference',period-twice)
