from pathlib import Path
import json,csv
from exoplanet.pipeline import sha,save_json,now
O=Path(__file__).parent;p=json.loads((O/'plan.json').read_text());mapping=json.loads((O/'mapping.json').read_text())['rows'];sources={r['source_id']:r for r in json.loads((O/'source.json').read_text())['rows']};rows=[]
prior_paths=['results/gaia-80387959-20261009/gaia_source.csv','results/gaia-402358350-scene-20261011/gaia_source.json','results/gaia-241928959-scene-20261011/gaia_source.json','results/gaia-5546257-scene-20261011/gaia_source.json']
for t in p['targets']:
 matches=[r for r in mapping if r['dr2_source_id']==t['dr2']];assert len(matches)==1;r=sources[matches[0]['dr3_source_id']];n=int(r['rv_nb_transits']);pv=None if not r['rv_chisq_pvalue'] else float(r['rv_chisq_pvalue']);gof=None if not r['rv_renormalised_gof'] else float(r['rv_renormalised_gof']);gate=None if pv is None or gof is None else pv<.01 and gof>4 and n>=10;flags=int(r['non_single_star']);prior=[]
 for path in prior_paths:
  pp=Path(path);rr=list(csv.DictReader(pp.open())) if pp.suffix=='.csv' else json.loads(pp.read_text());match=[x for x in rr if x['source_id']==r['source_id']]
  if match:prior.append(dict(path=path,sha256=sha(pp),matching_fields=[k for k in r if k in match[0] and r[k]==match[0][k]],changed_fields=[k for k in r if k in match[0] and r[k]!=match[0][k]]))
 rows.append(dict(tic=t['tic'],dr2=t['dr2'],dr3=r['source_id'],mapping=matches[0],values=r,nss_bits=dict(astrometric=bool(flags&1),spectroscopic=bool(flags&2),eclipsing=bool(flags&4)),official_rv_variability_selection=gate,rv_diagnostic_coverage='unavailable' if gate is None else 'below_recommended_transit_count' if n<10 else 'available',deblended_fraction=int(r['rv_nb_deblended_transits'])/n,prior_snapshots=prior))
save_json(O/'summary.json',dict(created_utc=now(),script_sha256=sha(Path(__file__)),rows=rows,interpretation='False RV selection means these metadata do not flag variability under that rule, never constancy or binary exclusion. None means statistics unavailable. Earlier snapshots with matching fields are reinterpreted evidence, not new Gaia measurements.'))
