from pathlib import Path
import json,csv,requests
from exoplanet.pipeline import save_json,sha,now
O=Path(__file__).parent;R=Path('data/companion-constraints-shortlist-20261012');records=[]
for tic in [80387959,402358350,241928959,469309982,96166003,5546257]:
 if tic==80387959:p=Path('data/targeting/neighbors-80387959.json');rows=json.loads(p.read_text())['data']
 else:p=next(Path('results').glob(f'neighbors-{tic}*/neighbors.json'));rows=json.loads(p.read_text())
 s=next(x for x in rows if int(x['ID'])==tic);records.append(dict(tic=tic,prior_path=str(p),prior_sha256=sha(p),tic_record=s,dr2=str(s['GAIA'])))
assert not (O/'plan.json').exists();save_json(O/'plan.json',dict(created_utc=now(),script_sha256=sha(Path(__file__)),targets=records,scope='Six exact target stars only; reuse existing TIC identifiers. Recheck all DR2->DR3 mappings, official schema then selected Gaia DR3 source metadata and four NSS tables. No flux/time-series or field-wide sources. Missing/zero flags do not exclude binaries; no repeated endpoint retries beyond one request each.'))
def query(name,q):
 rec=dict(name=name,query=q,started_utc=now())
 try:
  response=requests.get('https://gea.esac.esa.int/tap-server/tap/sync',params=dict(REQUEST='doQuery',LANG='ADQL',FORMAT='csv',MAXREC=100000,QUERY=q),timeout=90);raw=R/f'{name}.csv';raw.write_bytes(response.content);rec.update(url=response.url,path=str(raw),sha256=sha(raw),http_status=response.status_code);response.raise_for_status();reader=csv.DictReader(raw.open());rows=list(reader);assert reader.fieldnames and len(rows)<100000 and '<' not in reader.fieldnames[0];rec.update(status='success',columns=reader.fieldnames,rows=rows)
 except Exception as exc:rec.update(status='error',error=repr(exc))
 save_json(O/f'{name}.json',rec);print(name,rec['status'],len(rec.get('rows',[])),flush=True);return rec
ids=','.join(x['dr2'] for x in records)
m=query('mapping',f'select * from gaiadr3.dr2_neighbourhood where dr2_source_id in ({ids})');assert m['status']=='success';mapped=','.join(sorted({r['dr3_source_id'] for r in m['rows']}))
fields=['source_id','ra','dec','non_single_star','ruwe','duplicated_source','ipd_frac_multi_peak','ipd_frac_odd_win','astrometric_excess_noise','astrometric_excess_noise_sig','radial_velocity','radial_velocity_error','rv_nb_transits','rv_nb_deblended_transits','rv_visibility_periods_used','rv_method_used','rv_chisq_pvalue','rv_renormalised_gof','rv_amplitude_robust','rv_time_duration','grvs_mag','rv_template_teff']
quoted=','.join("'"+x+"'" for x in fields);schema=query('source-schema',f"select table_name,column_name,unit,description from TAP_SCHEMA.columns where table_name='gaiadr3.gaia_source' and column_name in ({quoted})");assert schema['status']=='success';available={r['column_name'] for r in schema['rows']};save_json(O/'missing-fields.json',dict(missing=sorted(set(fields)-available)));assert 'source_id' in available
query('source',f"select {','.join(x for x in fields if x in available)} from gaiadr3.gaia_source where source_id in ({mapped})")
tables=query('nss-schema',"select table_name,description from TAP_SCHEMA.tables where table_name like 'gaiadr3.nss_%'");assert tables['status']=='success';present={x['table_name'] for x in tables['rows']}
for tab in ['nss_two_body_orbit','nss_acceleration_astro','nss_non_linear_spectro','nss_vim_fl']:
 if 'gaiadr3.'+tab in present:query(tab,f'select * from gaiadr3.{tab} where source_id in ({mapped})')
 else:save_json(O/f'{tab}.json',dict(status='schema_missing',table=tab))
url='https://gea.esac.esa.int/archive/documentation/GDR3/Gaia_archive/chap_datamodel/sec_dm_main_source_catalogue/ssec_dm_gaia_source.html';rec=dict(url=url,started_utc=now())
try:
 r=requests.get(url,timeout=90);p=R/'gaia-source-doc.html';p.write_bytes(r.content);rec.update(path=str(p),sha256=sha(p),http_status=r.status_code);r.raise_for_status();rec['status']='success'
except Exception as e:rec.update(status='error',error=repr(e))
save_json(O/'documentation.json',rec)
