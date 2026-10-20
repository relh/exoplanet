exec(open('results/extension-469309982-96166003-20261012/query.py').read().split('rows=[]')[0])
rows=[]
jobs=[('469-cluster','SELECT * FROM "J/A+A/615/A49/members" WHERE Source=5259582384786570368'),('961-simulated','SELECT * FROM "J/ApJS/239/2/table2" WHERE TICID=96166003'),('961-lowextinction','SELECT * FROM "J/A+A/609/A116/lowetgas" WHERE Source=161856976421129472')]
for name,query in jobs:
 r=requests.get('https://tapvizier.cds.unistra.fr/TAPVizieR/tap/sync',params={'REQUEST':'doQuery','LANG':'ADQL','FORMAT':'csv','QUERY':query},timeout=90);p=D/(name+'.csv');p.write_bytes(r.content);rows.append(dict(name=name,url=r.url,path=str(p),status=r.status_code,sha256=hashlib.sha256(r.content).hexdigest()));print(name,r.status_code,r.text[:3000],flush=True);(O/'tables.json').write_text(json.dumps(rows,indent=2))
