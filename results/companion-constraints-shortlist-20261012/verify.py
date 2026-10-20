from pathlib import Path
import json,csv
from decimal import Decimal
from exoplanet.pipeline import sha,save_json,now
O=Path(__file__).parent;read=lambda p:json.loads(p.read_text());plan=read(O/'plan.json');assert sha(O/'query.py')==plan['script_sha256'];summary=read(O/'summary.json');assert sha(O/'summarize.py')==summary['script_sha256'];checked=[]
for p in O.glob('*.json'):
 r=read(p)
 if isinstance(r,dict) and 'path' in r and 'sha256' in r:
  assert sha(Path(r['path']))==r['sha256'];checked.append(p.name)
  if r.get('status')=='success' and 'rows' in r:assert list(csv.DictReader(Path(r['path']).open()))==r['rows']
for t in plan['targets']:
 p=Path(t['prior_path']);assert sha(p)==t['prior_sha256'];r=read(p);rr=r['data'] if isinstance(r,dict) else r;s=next(x for x in rr if int(x['ID'])==t['tic']);assert s==t['tic_record'] and str(s['GAIA'])==t['dr2']
m=read(O/'mapping.json')['rows'];src={x['source_id']:x for x in read(O/'source.json')['rows']};assert len(m)==len(src)==len(plan['targets'])==6
for r in summary['rows']:
 assert r['values']==src[r['dr3']];assert r['dr2']==r['dr3'];assert r['mapping'] in m;s=r['values'];pv=s['rv_chisq_pvalue'];g=s['rv_renormalised_gof'];gate=None if not pv or not g else Decimal(pv)<Decimal('.01') and Decimal(g)>4 and int(s['rv_nb_transits'])>=10;assert gate==r['official_rv_variability_selection'];assert abs(float(Decimal(s['rv_nb_deblended_transits'])/Decimal(s['rv_nb_transits']))-r['deblended_fraction'])<1e-14
 bits=int(s['non_single_star']);assert [r['nss_bits'][k] for k in ['astrometric','spectroscopic','eclipsing']]==[bool((bits//2**i)%2) for i in range(3)]
 for prior in r['prior_snapshots']:assert sha(Path(prior['path']))==prior['sha256'];assert not prior['changed_fields']
for tab in ['nss_two_body_orbit','nss_acceleration_astro','nss_non_linear_spectro','nss_vim_fl']:
 r=read(O/f'{tab}.json');assert r['status']=='success' and r['rows']==[] and 'source_id' in r['columns']
assert read(O/'nss-schema.json')['status']=='error';assert read(O/'documentation.json')['status']=='success'
save_json(O/'verification.json',dict(status='passed',created_utc=now(),script_sha256=sha(Path(__file__)),raw_records_verified=checked,exact_target_joins=6,empty_nss_tables_checked=4,independent_checks='Decimal RV gate and deblending fraction; integer NSS bit decomposition; exact source/raw/schema joins. No epoch data or physical companion exclusion.'))
print('passed',len(checked))
