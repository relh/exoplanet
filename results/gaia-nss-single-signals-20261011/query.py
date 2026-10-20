from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json,csv,io,requests
from exoplanet.pipeline import sha,save_json,now
out=Path(__file__).parent;inputs={};scenes={};ids=set()
for tic in [196681132,241928959,422626648]:
 p=Path(f'results/gaia-{tic}-scene-20261011/gaia_source.json');inputs[str(p)]=sha(p);rows=json.loads(p.read_text());scenes[str(tic)]=[r['source_id'] for r in rows];ids.update(scenes[str(tic)])
tables=['nss_two_body_orbit','nss_acceleration_astro','nss_non_linear_spectro','nss_vim_fl'];plans=[{'table':table,'query':f"SELECT * FROM gaiadr3.{table} WHERE source_id IN ({','.join(sorted(ids))})"} for table in tables]
assert not (out/'plan.json').exists();save_json(out/'plan.json',{'created':now(),'inputs':inputs,'script_sha256':sha(Path(__file__)),'scenes':scenes,'unique_ids':sorted(ids),'queries':plans,'policy':'All existing DR3 scene identities for three unresolved signals. No outcome-based ID selection. No entry does not exclude a binary.'})
def query(plan):
 name=plan['table'];path=Path(f'data/targeting/gaia-nss-single-{name}.csv');params={'REQUEST':'doQuery','LANG':'ADQL','FORMAT':'csv','MAXREC':'100000','QUERY':plan['query']};url=requests.Request('GET','https://gea.esac.esa.int/tap-server/tap/sync',params=params).prepare().url
 try:
  r=requests.get(url,timeout=45);r.raise_for_status();path.write_bytes(r.content);reader=csv.DictReader(io.StringIO(r.text));rows=list(reader);assert 'source_id' in (reader.fieldnames or []),r.text[:500];assert all(x['source_id'] in ids for x in rows)
  return {'table':name,'status':'downloaded','url':url,'path':str(path),'sha256':sha(path),'columns':reader.fieldnames,'rows':rows,'n_rows':len(rows)}
 except Exception as e:return {'table':name,'status':'error','url':url,'error':repr(e)}
with ThreadPoolExecutor(max_workers=4) as pool:results=list(pool.map(query,plans))
save_json(out/'results.json',results);print('unique sources',len(ids));print([{k:r[k] for k in ['table','status','n_rows'] if k in r} for r in results])
