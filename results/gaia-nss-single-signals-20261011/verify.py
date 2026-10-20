from pathlib import Path
import json,csv,numpy as np
from exoplanet.pipeline import sha,save_json
p=Path(__file__).parent;read=lambda q:json.loads(q.read_text());plan=read(p/'plan.json');results=read(p/'results.json')
assert sha(p/'query.py')==plan['script_sha256']
for path,digest in plan['inputs'].items():assert sha(Path(path))==digest
assert {r['table'] for r in results}=={q['table'] for q in plan['queries']}
for r in results:
 assert r['status']=='downloaded';f=Path(r['path']);assert sha(f)==r['sha256'];reader=csv.DictReader(f.open());rows=list(reader);assert reader.fieldnames==r['columns'];assert rows==r['rows'];assert len(rows)==r['n_rows']==0
ids={'196681132':'3611756510240137088','241928959':'6865254022910168320','422626648':'6254811248843788416'};context=[];inputs={}
for tic,gid in ids.items():
 gp=Path(f'results/gaia-{tic}-scene-20261011/gaia_source.json');npth=Path(f'results/neighbors-{tic}-20261011/neighbors.json');inputs[str(gp)]=sha(gp);inputs[str(npth)]=sha(npth);g=next(r for r in read(gp) if r['source_id']==gid);s=next(r for r in read(npth) if str(r['ID'])==tic);plx=float(g['parallax']);err=float(g['parallax_error'])
 context.append({'tic':int(tic),'gaia_dr3':gid,'non_single_star':g['non_single_star'],'ruwe':float(g['ruwe']),'parallax_mas':plx,'parallax_error_mas':err,'naive_inverse_parallax_pc':1000/plx,'formal_linearized_distance_error_pc':1000*err/plx**2,'tic_distance_pc':s.get('d'),'tic_parallax_mas':s.get('plx'),'tic_radius_solar':s.get('rad'),'tic_radius_error_solar':s.get('e_rad'),'tic_parameter_flag':s.get('SPFlag'),'gaia_teff_gspphot':g.get('teff_gspphot'),'gaia_distance_gspphot':g.get('distance_gspphot')})
save_json(p/'stellar-context.json',{'inputs':inputs,'targets':context,'limits':'Naive inverse parallax, not a posterior distance; no zero-point or excess-noise correction. TIC and Gaia refer to different catalog estimators/epochs. No replacement stellar radius derived; elevated RUWE limits interpretation. Empty astrophysical fields are unavailable, not zero.'})
save_json(p/'verification.json',{'unique_dr3_sources':len(plan['unique_ids']),'successful_tables':len(results),'nss_rows':sum(r['n_rows'] for r in results),'artifacts':{q.name:sha(q) for q in p.iterdir() if q.is_file() and q.name!='verification.json'},'limits':'Successful empty queries and metadata arithmetic, not evidence of singleness or binary exclusion.'});print(context)
