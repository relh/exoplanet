import json,math,pathlib,hashlib,datetime
R=pathlib.Path(__file__).parent;D=pathlib.Path('data')/R.name
p=json.loads((R/'plan.json').read_text());ts=p['targets']+[{'tic':'control','ra':99.97608333333334,'dec':35.523805555555555}]
keys=['sourceid','ra','dec','hjdstart','hjdstop','wasp_mag','npts','tm_statnpts','tm_median','tm_stddevwrtmed','tm_range595']
summary={}
for t in [ts[0],ts[2]]:
 rows=[]
 for tab in json.loads((D/f"ui-{t['tic']}-tables.json").read_text()):
  for row in tab:
   if len(row)==14 and row[2].strip().startswith('1SWASP'):
    a=dict(zip(keys,[x.strip() for x in row[2:13]]))
    for k in keys[1:]:a[k]=int(a[k]) if k in ['npts','tm_statnpts'] else float(a[k])
    ra1,de1,ra2,de2=map(math.radians,[a['ra'],a['dec'],t['ra'],t['dec']]);h=math.sin((de1-de2)/2)**2+math.cos(de1)*math.cos(de2)*math.sin((ra1-ra2)/2)**2
    a['separation_j2016_arcsec']=math.degrees(2*math.asin(math.sqrt(h)))*3600;a['span_minutes']=(a['hjdstop']-a['hjdstart'])*1440
    rows.append(a)
 summary[str(t['tic'])]={'rows':rows,'row_count':len(rows),'nearest':min(rows,key=lambda r:r['separation_j2016_arcsec'])}
summary['402358350']={'rows':[],'row_count':0,'status':'Official UI HTTP200 with XML explicit No data found in this region, input resolves to exact requested coordinate. TAP403 remains an error.'}
(R/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
records=[]
for f in sorted(D.glob('ui-*')):
 rec={'path':str(f),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'bytes':f.stat().st_size,'captured_file_mtime_utc':datetime.datetime.fromtimestamp(f.stat().st_mtime,datetime.timezone.utc).isoformat()}
 if f.name.endswith('network.json'):
  a=json.loads(f.read_text())['data'];rec.update(url=a['url'],status=a['status'],request_timestamp_ms=a['timestamp'],response_date=a['responseHeaders']['date'])
 records.append(rec)
(R/'browser-manifest.json').write_text(json.dumps({'entry_url':'https://exoplanetarchive.ipac.caltech.edu/cgi-bin/TblSearch/nph-tblSearchInit?app=ExoTbls&config=superwasptimeseries','method':'agent-browser official UI search (120arcsec); capture DOM tables/text and network query response; no time-series open/plot/download','files':records,'capture_notes':'Files ui-402358350-{text,snapshot,tables,url} capture input form, not a result table: UI silently auto-dismissed no-data alert. Authoritative 402 result is ui-402358350-network.json. Three identical UI 402 submits occurred while diagnosing missing popup. Initial table extraction syntax error and invalid tab-switch command changed no data.'},indent=2)+'\n')
print({k:{'count':v['row_count'],'nearest':v.get('nearest')} for k,v in summary.items()})
