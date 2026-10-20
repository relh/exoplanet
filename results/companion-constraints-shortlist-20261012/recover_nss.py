from pathlib import Path
import json,requests
from exoplanet.pipeline import save_json,sha,now
O=Path(__file__).parent;R=Path('data/companion-constraints-shortlist-20261012')
# Reuse only the query function definition; never rerun the initial queries/plan.
s=(O/'query.py').read_text();import csv
exec(s[s.index('def query('):s.index("ids=','.join")])
save_json(O/'recovery-plan.json',dict(utc=now(),script_sha256=sha(Path(__file__)),original_error_sha256=sha(O/'nss-schema.json'),reason='Official TAP_SCHEMA.tables produced HTTP500 missing FROM-clause SQL server error. One alternate metadata route TAP_SCHEMA.columns, then at most four exact-source NSSqueries. Do not overwrite/retryfailedresponse.'))
schema=query('nss-columns',"select table_name,column_name,unit,description from TAP_SCHEMA.columns where table_name like 'gaiadr3.nss_%' and column_name in ('source_id','period','nss_solution_type')")
mapped=','.join(sorted({r['dr3_source_id'] for r in json.loads((O/'mapping.json').read_text())['rows']}));present={x['table_name'] for x in schema.get('rows',[])}
for tab in ['nss_two_body_orbit','nss_acceleration_astro','nss_non_linear_spectro','nss_vim_fl']:
 if 'gaiadr3.'+tab in present:query(tab,f'select * from gaiadr3.{tab} where source_id in ({mapped})')
 else:save_json(O/f'{tab}.json',dict(status='schema_missing_or_error',table=tab))
url='https://gea.esac.esa.int/archive/documentation/GDR3/Gaia_archive/chap_datamodel/sec_dm_main_source_catalogue/ssec_dm_gaia_source.html';rec=dict(url=url,started_utc=now())
try:
 r=requests.get(url,timeout=90);p=R/'gaia-source-doc.html';p.write_bytes(r.content);rec.update(path=str(p),sha256=sha(p),http_status=r.status_code);r.raise_for_status();rec['status']='success'
except Exception as e:rec.update(status='error',error=repr(e))
save_json(O/'documentation.json',rec)
