"""Identity-checked Gaia RV context; no orbital fit or mass inference."""
from pathlib import Path
import json,csv
from exoplanet.pipeline import sha,save_json,fetch,now
out=Path(__file__).parent;g=Path('results/gaia-429034844-scene-20261011');nb=Path('results/neighbors-429034844-20261011/neighbors.json')
read=lambda p:json.loads(p.read_text())
star=next(r for r in read(nb) if int(r['ID'])==429034844)
raw=Path('data/catalogs/gaia-429034844-scene-gaia_source-20261011.csv')
assert sha(raw)==read(g/'gaia_source-source.json')['sha256']
mappings=[r for r in read(g/'dr2_neighbourhood.json') if r['dr2_source_id']==str(star['GAIA'])]
assert len(mappings)==1
sid=mappings[0]['dr3_source_id'];rows=list(csv.DictReader(raw.open()));r=next(r for r in rows if r['source_id']==sid)
assert r==next(r for r in read(g/'gaia_source.json') if r['source_id']==sid)
fields=['source_id','ra','dec','ruwe','duplicated_source','non_single_star','radial_velocity','radial_velocity_error','rv_method_used','rv_nb_transits','rv_nb_deblended_transits','rv_visibility_periods_used','rv_expected_sig_to_noise','rv_renormalised_gof','rv_chisq_pvalue','rv_time_duration','rv_amplitude_robust','rv_template_teff','grvs_mag','has_epoch_rv','has_rvs','has_epoch_photometry']
checks={'pvalue_lt_0_01':float(r['rv_chisq_pvalue'])<.01,'gof_gt_4':float(r['rv_renormalised_gof'])>4,'transits_ge_10':int(r['rv_nb_transits'])>=10,'template_3900_to_8000':3900<=float(r['rv_template_teff'])<=8000}
url='https://gea.esac.esa.int/archive/documentation/GDR3/Gaia_archive/chap_datamodel/sec_dm_main_source_catalogue/ssec_dm_gaia_source.html'
doc=fetch(url,Path('data/literature/gaia-dr3-source-rv-429034844.html'));save_json(out/'documentation-source.json',doc)
result={'utc':now(),'tic':429034844,'tic_gaia_dr2':str(star['GAIA']),'mapping':mappings,'fields':{k:r[k] for k in fields},'rv_variability_cuts':checks,'passes_all':all(checks.values()),'inputs':{str(p):sha(p) for p in [nb,raw,g/'gaia_source.json',g/'gaia_source-source.json',g/'dr2_neighbourhood.json']},'script_sha256':sha(Path(__file__)),'documentation_url':url,'limits':'Catalog RV variability context, not an orbit, calibrated binary probability, companion mass, or proof of the source of TESS dips. Most RV transits were deblended. No epoch RV or period alignment available. Reported p=0 is finite-precision catalog output, not exact zero probability.'}
save_json(out/'results.json',result);print(result['fields']);print(checks)
