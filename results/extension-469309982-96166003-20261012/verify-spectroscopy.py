from pathlib import Path
import json,hashlib,xml.etree.ElementTree as ET
O=Path(__file__).parent;out=[]
for name in ['spectroscopy-cones.json','spectroscopy-recovery.json']:
 for r in json.loads((O/name).read_text()):
  p=Path(r['path']);assert hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256'];root=ET.fromstring(p.read_bytes());tables=root.findall('.//{*}TABLE');rows=root.findall('.//{*}TR');errors=[v.attrib for v in root.findall('.//{*}INFO') if v.get('value')=='ERROR' or v.get('name')=='Error'];assert not rows
  if 'galahdr3' in r['catalog']:assert len(tables)==0;status='invalid table route, not nonmatch'
  else:assert len(tables)==1 and not errors;status='valid empty table'
  out.append(dict(tic=r['tic'],catalog=r['catalog'],status=status,tables=len(tables),rows=len(rows)))
(O/'spectroscopy-verification.json').write_text(json.dumps(dict(verified=True,queries=out),indent=2));print(out)
