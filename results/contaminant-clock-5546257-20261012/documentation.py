from pathlib import Path
import urllib.request,json,hashlib,datetime
p=Path(__file__).parent;(p/'data').mkdir(exist_ok=True);(p/'.gitignore').write_text('data/\n');rows=[]
for name,url in [('esa','https://gea.esac.esa.int/archive/documentation/GDR3/Gaia_archive/chap_datamodel/sec_dm_variability_tables/ssec_dm_vari_eclipsing_binary.html'),('aip','https://gaia.aip.de/metadata/gaiadr3/vari_eclipsing_binary/')]:
 row=dict(url=url,retrieved_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
 try:
  data=urllib.request.urlopen(url,timeout=15).read();q=p/'data'/f'{name}.html';q.write_bytes(data);row.update(path=str(q),sha256=hashlib.sha256(data).hexdigest(),bytes=len(data),status='ok')
 except Exception as exc:row.update(status='error',error=repr(exc))
 rows.append(row)
(p/'documentation.json').write_text(json.dumps(rows,indent=2)+'\n');print(rows)
