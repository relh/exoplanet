exec(open('results/web-241928959-20261012/query.py').read().split('jobs=')[0])
tap='https://tapvizier.cds.unistra.fr/TAPVizieR/tap/sync';sim='https://simbad.cds.unistra.fr/simbad/sim-tap/sync'
qs=[('simbad-ref-join',sim,'SELECT r.bibcode FROM has_ref h JOIN ref r ON h.oidbibref=r.oidbib WHERE h.oidref=30823552'),('binary-tables',tap,"SELECT table_name,description FROM TAP_SCHEMA.tables WHERE table_name LIKE '%506/2269%'"),('wds-cone',tap,'SELECT TOP 100 * FROM "B/wds/wds" WHERE 1=CONTAINS(POINT(\'ICRS\',RAdeg,DEdeg),CIRCLE(\'ICRS\',297.987022155552,-21.5031691342776,0.0166666667))')]
rows=[]
for name,url,query in qs:
 try:
  r=requests.get(url,params={'REQUEST':'doQuery','LANG':'ADQL','FORMAT':'csv','QUERY':query},timeout=90);p=D/(name+'.response');p.write_bytes(r.content);rows.append(dict(name=name,url=r.url,status=r.status_code,path=str(p),sha256=hashlib.sha256(r.content).hexdigest(),query=query));print(name,r.status_code,r.text[:1800],flush=True)
 except Exception as e:rows.append(dict(name=name,error=str(e)))
 (O/'queries-more.json').write_text(json.dumps(rows,indent=2))
