from pathlib import Path
import json,csv
from exoplanet.pipeline import sha,save_json,now
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());rows=[];inputs={}
fields=['source_id','ra','dec','ruwe','duplicated_source','non_single_star','radial_velocity','radial_velocity_error','rv_method_used','rv_nb_transits','rv_nb_deblended_transits','rv_visibility_periods_used','rv_renormalised_gof','rv_chisq_pvalue','rv_time_duration','rv_amplitude_robust','rv_template_teff','has_epoch_rv']
for tic in [422626648,241928959,196681132]:
 g=Path(f'results/gaia-{tic}-scene-20261011');nb=Path(f'results/neighbors-{tic}-20261011/neighbors.json');raw=Path(f'data/catalogs/gaia-{tic}-scene-gaia_source-20261011.csv');assert sha(raw)==read(g/'gaia_source-source.json')['sha256'];catalog=list(csv.DictReader(raw.open()));assert catalog==read(g/'gaia_source.json');mapping=read(g/'dr2_neighbourhood.json');stars=read(g/'plan.json')['targets']
 for p in [nb,raw,g/'gaia_source.json',g/'dr2_neighbourhood.json',g/'plan.json']:inputs[str(p)]=sha(p)
 for star in stars:
  dr2=str(star.get('GAIA'));maps=[m for m in mapping if m['dr2_source_id']==dr2]
  for m in maps:
   r=next(r for r in catalog if r['source_id']==m['dr3_source_id']);needed=['rv_chisq_pvalue','rv_renormalised_gof','rv_nb_transits','rv_template_teff'];missing=[k for k in needed if r[k]==''];checks=None
   if not missing:checks={'pvalue_lt_0_01':float(r['rv_chisq_pvalue'])<.01,'gof_gt_4':float(r['rv_renormalised_gof'])>4,'transits_ge_10':int(r['rv_nb_transits'])>=10,'template_3900_to_8000':3900<=float(r['rv_template_teff'])<=8000}
   rows.append({'scene_tic':tic,'tic':int(star['ID']),'is_target':int(star['ID'])==tic,'dr2':dr2,'mapping':m,'n_mappings_for_tic':len(maps),'fields':{k:r[k] for k in fields},'missing_cut_fields':missing,'cuts':checks,'passes_three_documented_variability_cuts':None if checks is None else all(checks[k] for k in ['pvalue_lt_0_01','gof_gt_4','transits_ge_10']),'passes_all':None if checks is None else all(checks.values())})
doc=Path('data/literature/gaia-dr3-source-rv-429034844.html');meta=Path('results/rv-context-429034844-20261011/documentation-source.json');assert sha(doc)==read(meta)['sha256'];inputs[str(doc)]=sha(doc);inputs[str(meta)]=sha(meta)
save_json(out/'results.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'inputs':inputs,'rows':rows,'documentation_url':read(meta)['url'],'limits':'Reuses retrieved Gaia DR3 evidence with identity mappings. Missing diagnostics are unavailable, never negative. The three variability cuts are documented;3900–8000K is the prior investigation’s additional conservative filter, not a fourth cut on this documentation page. RV diagnostics are not an orbit, mass, host attribution or planet/binary validation. No new measurements.'})
for r in rows:
 if r['is_target'] or r['passes_all']:print(r['scene_tic'],r['tic'],r['fields'],r['passes_all'])
print('rows',len(rows),'complete diagnostics',sum(r['cuts'] is not None for r in rows))
