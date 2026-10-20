exec(open('results/extension-469309982-96166003-20261012/query.py').read().split('rows=[]')[0])
rows=[]
queries=[('spectroscopy-tables',"SELECT table_name,description FROM TAP_SCHEMA.tables WHERE table_name LIKE '%V/154/%' OR table_name LIKE '%V/156/%' OR table_name LIKE '%V/164/%' OR table_name LIKE '%III/284/%' OR table_name LIKE '%III/290/%'")]
for name,query in queries:
 r=requests.get('https://tapvizier.cds.unistra.fr/TAPVizieR/tap/sync',params={'REQUEST':'doQuery','LANG':'ADQL','FORMAT':'csv','QUERY':query},timeout=90);p=D/(name+'.csv');p.write_bytes(r.content);rows.append(dict(name=name,url=r.url,path=str(p),status=r.status_code,sha256=hashlib.sha256(r.content).hexdigest()));print(r.status_code,r.text[:9000]);(O/'spectroscopy-discovery.json').write_text(json.dumps(rows,indent=2))
