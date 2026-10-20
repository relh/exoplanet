exec(open('results/web-241928959-20261012/query.py').read().split('jobs=')[0])
tap='https://tapvizier.cds.unistra.fr/TAPVizieR/tap/sync';sim='https://simbad.cds.unistra.fr/simbad/sim-tap/sync'
qs=[('binary-schema',tap,"SELECT column_name FROM TAP_SCHEMA.columns WHERE table_name LIKE '%506/2269/catalog%'"),('wds-schema',tap,"SELECT column_name FROM TAP_SCHEMA.columns WHERE table_name LIKE '%B/wds/wds%'"),('spyglass-older',tap,'SELECT TOP 10 * FROM "J/ApJ/954/134/table4" WHERE Gaia=6865254022910168320')]
rows=[]
for name,url,query in qs:
 try:
  r=requests.get(url,params={'REQUEST':'doQuery','LANG':'ADQL','FORMAT':'csv','QUERY':query},timeout=90);p=D/(name+'.response');p.write_bytes(r.content);rows.append(dict(name=name,url=r.url,status=r.status_code,path=str(p),sha256=hashlib.sha256(r.content).hexdigest(),query=query));print(name,r.status_code,r.text[:1800],flush=True)
 except Exception as e:rows.append(dict(name=name,error=str(e)))
 (O/'queries-final.json').write_text(json.dumps(rows,indent=2))
