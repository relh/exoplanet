"""Independent HTML-parser check of CHEOPS result tables; no network or flux."""
from pathlib import Path
from html.parser import HTMLParser
import json, hashlib
R=Path(__file__).resolve().parents[2]
class Table(HTMLParser):
 def __init__(self):super().__init__();self.active=False;self.rows=[];self.row=None
 def handle_starttag(self,tag,attrs):
  if tag=='table' and dict(attrs).get('id')=='results':self.active=True
  if self.active and tag=='tr':self.row=[]
 def handle_data(self,data):
  if self.active and self.row is not None and data.strip():self.row.append(data.strip())
 def handle_endtag(self,tag):
  if self.active and tag=='tr':self.rows.append(self.row);self.row=None
  if tag=='table':self.active=False
manifest=json.loads((R/'results/cheops-metadata-20261013/provenance.json').read_text())
for m in manifest:assert hashlib.sha256((R/m['path']).read_bytes()).hexdigest()==m['sha256']
counts={}
for name in ['80387959','402358350','control']:
 p=Table();p.feed((R/f'data/cheops-metadata-20261013/{name}-result.html').read_text())
 if name=='control':
  rows=[row for row in p.rows if 'WASP-189' in row];assert len(rows)==8
 else:
  assert any('No data available in table' in row for row in p.rows)
  assert not any(any(item.startswith('CH_PR') for item in row) for row in p.rows)
  rows=[]
 counts[name]=len(rows)
out={'status':'pass','raw_hashes':len(manifest),'independently_parsed_table_counts':counts,'scope':'Standard-library HTMLParser, table id=results only; no archive completeness or planet validation.'}
(R/'results/remaining-evidence-audit-20261013/cheops-review.json').write_text(json.dumps(out,indent=2)+'\n');print(out)
