"""Compare the independently selected peak with the neighboring known planet."""
from pathlib import Path
import csv, json
from exoplanet.pipeline import fetch, save_json, sha, now
out=Path(__file__).parent
path=Path('data/catalogs/tic46432937-ps-20261010.csv')
query="select pl_name,hostname,tic_id,pl_orbper,pl_orbpererr1,pl_tranmid,pl_tranmiderr1,pl_trandur,pl_refname from ps where hostname='TIC 46432937'"
params={'query':query,'format':'csv'}
save_json(out/'request.json',{'utc':now(),'query':query,'script_sha256':sha(Path(__file__))})
source=fetch('https://exoplanetarchive.ipac.caltech.edu/TAP/sync',path,params)
rows=list(csv.DictReader(path.open()));assert rows and all(r['tic_id']=='TIC 46432937' for r in rows)
fp=Path('results/qlp-faint-sector98-followup-20261010/46432934-peak0/frozen.json')
b=json.loads(fp.read_text())['best'];comparisons=[]
for r in rows:
    if not r['pl_orbper'] or not r['pl_tranmid']:continue
    p=float(r['pl_orbper']);epoch=float(r['pl_tranmid'])-2457000
    cycle=round((b['transit_time']-epoch)/p)
    comparisons.append({'row':r,'cycle_to_selected_epoch':cycle,
        'period_difference_days':b['period']-p,
        'selected_epoch_minus_published_prediction_days':b['transit_time']-(epoch+cycle*p)})
save_json(out/'results.json',{'utc':now(),'source':source,'frozen_sha256':sha(fp),
    'comparisons':comparisons,'limits':'Post-selection identification against a known neighboring planet. No period refit or new transit validation. Differences are numerical comparisons, not confidence intervals; catalog solutions may share observations.'})
print(comparisons)
