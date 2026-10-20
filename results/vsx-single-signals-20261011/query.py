from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import requests,json,csv,io
from exoplanet.pipeline import sha,save_json,now
out=Path(__file__).parent;gids={196681132:'3611756510240137088',241928959:'6865254022910168320',422626648:'6254811248843788416'};plans=[]
for tic,gid in gids.items():
 p=Path(f'results/gaia-{tic}-scene-20261011/gaia_source.json');g=next(x for x in json.loads(p.read_text()) if x['source_id']==gid);ra,dec=float(g['ra']),float(g['dec']);query=f'''SELECT TOP 100 * FROM "B/vsx/vsx" WHERE 1=CONTAINS(POINT('ICRS',"RAJ2000","DEJ2000"),CIRCLE('ICRS',{ra},{dec},{60/3600}))'''
 plans.append({'tic':tic,'gaia_dr3':gid,'position':[ra,dec],'gaia_path':str(p),'gaia_sha256':sha(p),'query':query})
save_json(out/'plan.json',{'created':now(),'script_sha256':sha(Path(__file__)),'catalog':'B/vsx/vsx','radius_arcsec':60,'targets':plans,'limits':'Cone includes possible neighbors; positional/period match must be inspected. Nonmatch is not novelty or binary exclusion.'})
def query(row):
 params={'REQUEST':'doQuery','LANG':'ADQL','FORMAT':'csv','QUERY':row['query']};url=requests.Request('GET','https://tapvizier.cds.unistra.fr/TAPVizieR/tap/sync',params=params).prepare().url;p=Path(f'data/targeting/vsx-{row["tic"]}-20261011.csv')
 try:
  r=requests.get(url,timeout=45);r.raise_for_status();p.write_bytes(r.content);reader=csv.DictReader(io.StringIO(r.text));rows=list(reader);assert {'Name','Period','RAJ2000','DEJ2000'}<=set(reader.fieldnames or []),r.text[:500]
  return {'tic':row['tic'],'status':'downloaded','url':url,'path':str(p),'sha256':sha(p),'columns':reader.fieldnames,'rows':rows,'n_rows':len(rows),'possibly_truncated':len(rows)==100}
 except Exception as e:return {'tic':row['tic'],'status':'error','url':url,'error':repr(e)}
with ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(query,plans))
save_json(out/'results.json',results);print(results)
