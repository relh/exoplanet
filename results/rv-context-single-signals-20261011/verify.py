from pathlib import Path
import json,csv
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());d=read(out/'results.json');assert d['script_sha256']==sha(out/'run.py')
for p,h in d['inputs'].items():assert sha(Path(p))==h
for r in d['rows']:
 tic=r['scene_tic'];g=Path(f'results/gaia-{tic}-scene-20261011');maps=read(g/'dr2_neighbourhood.json');assert r['mapping'] in maps and r['mapping']['dr2_source_id']==r['dr2'];source=next(x for x in read(g/'gaia_source.json') if x['source_id']==r['mapping']['dr3_source_id']);assert all(source[k]==v for k,v in r['fields'].items())
 star=next(x for x in read(g/'plan.json')['targets'] if int(x['ID'])==r['tic']);assert str(star['GAIA'])==r['dr2']
 if r['cuts'] is None:assert r['missing_cut_fields'] and r['passes_all'] is None and r['passes_three_documented_variability_cuts'] is None
 else:
  f=r['fields'];assert r['passes_three_documented_variability_cuts']==(float(f['rv_chisq_pvalue'])<.01 and float(f['rv_renormalised_gof'])>4 and int(f['rv_nb_transits'])>=10)
  assert r['passes_all']==(r['passes_three_documented_variability_cuts'] and 3900<=float(f['rv_template_teff'])<=8000)
targets=[r for r in d['rows'] if r['is_target']];assert len(targets)==3 and all(r['n_mappings_for_tic']==1 for r in targets)
r=next(r for r in targets if r['tic']==422626648);assert r['fields']['source_id']=='6254811248843788416' and r['passes_three_documented_variability_cuts'] and not r['passes_all'];assert float(r['fields']['rv_amplitude_robust'])==29.727648
save_json(out/'verification.json',{'script_sha256':sha(Path(__file__)),'results_sha256':sha(out/'results.json'),'n_rows':len(d['rows']),'status':'All input hashes and71 TIC/DR2/DR3 field mappings checked. Three target mappings unique. Three documented RV cuts separated from prior additional temperature filter; unavailable diagnostics remain null.'})
print('71mapped rows verified')
