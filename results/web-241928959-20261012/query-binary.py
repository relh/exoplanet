exec(open('results/web-241928959-20261012/query.py').read().split('jobs=')[0])
tap='https://tapvizier.cds.unistra.fr/TAPVizieR/tap/sync';sim='https://simbad.cds.unistra.fr/simbad/sim-tap/sync'
qs=[('binary-exact', 'https://tapvizier.cds.unistra.fr/TAPVizieR/tap/sync', 'SELECT TOP 100 * FROM "J/MNRAS/506/2269/catalog" WHERE Source1=6865254022910168320 OR Source2=6865254022910168320'), ('wds-cone-fixed', 'https://tapvizier.cds.unistra.fr/TAPVizieR/tap/sync', 'SELECT TOP 100 * FROM "B/wds/wds" WHERE 1=CONTAINS(POINT(\'ICRS\',RAJ2000,DEJ2000),CIRCLE(\'ICRS\',297.987022155552,-21.5031691342776,0.0166666667))')]
rows=[]
for name,url,query in qs:
 try:
  r=requests.get(url,params={'REQUEST':'doQuery','LANG':'ADQL','FORMAT':'csv','QUERY':query},timeout=90);p=D/(name+'.response');p.write_bytes(r.content);rows.append(dict(name=name,url=r.url,status=r.status_code,path=str(p),sha256=hashlib.sha256(r.content).hexdigest(),query=query));print(name,r.status_code,r.text[:1800],flush=True)
 except Exception as e:rows.append(dict(name=name,error=str(e)))
 (O/'queries-binary.json').write_text(json.dumps(rows,indent=2))
