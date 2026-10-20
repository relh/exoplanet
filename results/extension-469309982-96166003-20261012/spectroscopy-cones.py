exec(open('results/extension-469309982-96166003-20261012/query.py').read().split('rows=[]')[0])
from concurrent.futures import ThreadPoolExecutor
from astropy.io.votable import parse
from io import BytesIO
jobs=[(tic,ra,dec,cat) for tic,ra,dec in [(469309982,148.848112423025,-56.6859202446395),(96166003,72.5889755509497,33.7070971379888)] for cat in ['III/283/ravedr6','III/286/catalog','V/156/dr7slrs','J/MNRAS/506/150/galahdr3']]
def query(j):
 tic,ra,dec,cat=j;name=str(tic)+'-'+cat.replace('/','_');r=requests.get('https://vizier.cds.unistra.fr/viz-bin/votable',params={'-source':cat,'-c':f'{ra} {dec}','-c.rs':'10','-out.all':'1','-out.max':'100'},timeout=120);p=D/(name+'.xml');p.write_bytes(r.content);rec=dict(name=name,tic=tic,catalog=cat,ra=ra,dec=dec,radius_arcsec=10,url=r.url,path=str(p),status=r.status_code,sha256=hashlib.sha256(r.content).hexdigest());v=parse(BytesIO(r.content));tables=list(v.iter_tables());rec['tables']=[]
 for k,t in enumerate(tables):
  table=t.to_table();out=O/(name+f'-{k}.csv');table.write(out,format='ascii.csv',overwrite=False);rec['tables'].append(dict(path=str(out),rows=len(table),columns=table.colnames))
 rec['infos']=[dict(name=x.name,value=x.value,content=x.content) for res in v.resources for x in res.infos];print(name,[(x['rows']) for x in rec['tables']],rec['infos'],flush=True);return rec
rows=[]
with ThreadPoolExecutor(max_workers=4) as pool:
 for rec in pool.map(query,jobs):rows.append(rec);(O/'spectroscopy-cones.json').write_text(json.dumps(rows,indent=2))
