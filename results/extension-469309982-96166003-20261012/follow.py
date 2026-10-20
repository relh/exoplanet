exec(open('results/extension-469309982-96166003-20261012/query.py').read().split('rows=[]')[0])
rows=[]
jobs=[('cluster-readme','https://cdsarc.cds.unistra.fr/viz-bin/ReadMe/J/A+A/615/A49',{'format':'html','tex':'true'}),('yield-readme','https://cdsarc.cds.unistra.fr/viz-bin/ReadMe/J/ApJS/239/2',{'format':'html','tex':'true'}),('cluster-tables','https://tapvizier.cds.unistra.fr/TAPVizieR/tap/sync',{'REQUEST':'doQuery','LANG':'ADQL','FORMAT':'csv','QUERY':"SELECT table_name,description FROM TAP_SCHEMA.tables WHERE table_name LIKE '%615/A49%'"})]
for name,url,params in jobs:
 r=requests.get(url,params=params,timeout=90);p=D/(name+'.response');p.write_bytes(r.content);rows.append(dict(name=name,url=r.url,path=str(p),status=r.status_code,sha256=hashlib.sha256(r.content).hexdigest()));print(name,r.status_code,r.text[-3000:] if name=='cluster-tables' else len(r.content),flush=True);(O/'follow.json').write_text(json.dumps(rows,indent=2))
