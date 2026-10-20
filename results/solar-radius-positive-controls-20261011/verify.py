from pathlib import Path
import json,csv,collections
from exoplanet.pipeline import sha,save_json,read_curve
p=Path(__file__).parent;out=Path('results/solar-radius-positive-controls-run-20261011');plan=json.loads((p/'plan.json').read_text());run=json.loads((out/'run.json').read_text());selected=json.loads((p/'selected.json').read_text());meta=json.loads((p/'catalog-source.json').read_text());raw=Path('data/catalogs/solar-radius-positive-controls-20261011.csv')
assert sha(raw)==meta['sha256'];assert list(csv.DictReader(raw.open()))==json.loads((p/'catalog.json').read_text())
for name,digest in plan['inputs'].items():assert sha(Path(name))==digest
assert sha(p/'selected.json')==plan['selected_sha256']==run['selection_sha256'];assert plan['created_utc']<run['started_utc'];assert run['status']=='complete' and run['n_selected']==5 and run['n_errors']==0
for name,digest in run['source_sha256'].items():assert sha(out/'source'/name)==digest
rows={int(q.stem):json.loads(q.read_text()) for q in (out/'targets').glob('*.json')};assert set(rows)=={s['tic'] for s in selected};n=0
for s in selected:
 r=rows[s['tic']];assert r['target']==s
 for d in r['data']:
  path=Path(f"data/lightcurves/s{d['sector']:04d}-{s['tic']}.fits");assert sha(path)==d['source']['sha256'];_,_,_,star=read_curve(path);assert star['ticid']==s['tic'] and star['sector']==d['sector'];assert plan['created_utc']<d['source']['retrieved_utc'];n+=1
 for sector in s['heldout_sectors']:assert not Path(f"data/lightcurves/s{sector:04d}-{s['tic']}.fits").exists()
eval=json.loads((p/'evaluation.json').read_text());controls=json.loads((p/'selected-controls.json').read_text());passing=matches=0
for c,e in zip(controls,eval['rows']):
 r=rows[c['tic']];period=float(c['catalog_planet']['pl_orbper']);assert e['tic']==c['tic'];assert sha(out/'targets'/f"{c['tic']}.json")==e['target_file_sha256'];hit=any(abs(x['period']-period)<.01*period for x in r['peaks']);full=any(abs(x['best']['period']-period)<.01*period and len(x['flags'])==0 for x in r['screened_peaks']);assert full==e['selected_planet_pass'];assert hit==bool(e['selected_planet_period_matches']);passing+=full;matches+=hit
assert (passing,matches)==(eval['n_full_passes'],eval['n_period_matches'])==(2,4)
save_json(p/'verification.json',dict(status='passed',raw_products_checked=n,source_snapshot_hashes_checked=True,catalog_csv_json_reconciled=True,selection_precedes_download=True,reserved_cache_absent=True,selected_planet_period_matches=matches,selected_planet_full_passes=passing,limits='Audit and outcome arithmetic, not a repeated full photometric search or population completeness estimate.'))
print(n,matches,passing)
