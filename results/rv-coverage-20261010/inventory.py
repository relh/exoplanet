import csv,io,json,zipfile
from collections import defaultdict
from pathlib import Path
import numpy as np
from bs4 import BeautifulSoup
from astropy.coordinates import SkyCoord
import astropy.units as u
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent;archive=Path('data/rv/HARPS_RVBank_ver02.csv.zip')
metadata={};s=BeautifulSoup(Path('data/rv/rvbank-index.html').read_text(),'html.parser')
for a in s.find_all('a'):
 href=str(a.get('href',''))
 if not(href.startswith('./Ver_02/') and href.endswith('_HARPS_RVBank_ver02.csv')):continue
 cells=a.find_parent('tr').find_all(['th','td'],recursive=False)
 if len(cells)!=12:continue
 f=[c.get_text(' ',strip=True) for c in cells]
 try:metadata[f[0]]=dict(teff=float(f[4]),vmag=float(f[6]),distance_pc=float(f[8]))
 except ValueError:continue
summary=defaultdict(lambda:dict(times=[],errors=[],ra=None,dec=None,rows=0));count=0
with zipfile.ZipFile(archive) as z:
 with z.open('HARPS_RVBank_ver02.csv') as stream:
  for r in csv.DictReader(io.TextIOWrapper(stream)):
   count+=1;v=summary[r['target']];v['rows']+=1
   try:
    t,y,e,flag=[float(r[k]) for k in ['BJD','RV_mlc_nzp','e_RV_mlc_nzp','f_RV']]
    if flag!=0 or not np.all(np.isfinite([t,y,e])) or not(0<e<100) or abs(y)>1e6:continue
    v['times'].append(t);v['errors'].append(e);v['ra']=float(r['ra']);v['dec']=float(r['dec'])
   except ValueError:continue
known=list(csv.DictReader(open('data/rv/known-planets-20261010.csv')))
kcoord=SkyCoord([float(r['ra']) for r in known]*u.deg,[float(r['dec']) for r in known]*u.deg)
candidates=[];coverage=[]
for name,v in sorted(summary.items()):
 if not v['times']:continue
 t=np.array(v['times']);nights=np.unique(np.floor(t+.5));m=metadata.get(name,{})
 row=dict(name=name,raw_rows=v['rows'],usable_rows=len(t),nights=len(nights),span=float(np.ptp(t)),median_error=float(np.median(v['errors'])),ra=v['ra'],dec=v['dec'],**m)
 coverage.append(row)
 if len(nights)<80 or np.ptp(t)<500 or row['median_error']>3:continue
 if not(4000<=m.get('teff',0)<=6500 and m.get('vmag',99)<10.5 and m.get('distance_pc',999)<100):continue
 coord=SkyCoord(v['ra']*u.deg,v['dec']*u.deg);separation=coord.separation(kcoord).arcsec
 if separation.min()<60 or name=='HD32564':continue
 row={**row,'train_last_night':float(nights[int(.75*len(nights))-1]),'status':'not_yet_searched','closest_confirmed_arcsec':float(separation.min())}
 candidates.append(row)
with (out/'coverage.csv').open('w') as f:
 writer=csv.DictWriter(f,fieldnames=['name','raw_rows','usable_rows','nights','span','median_error','ra','dec','teff','vmag','distance_pc']);writer.writeheader();writer.writerows(coverage)
save_json(out/'selection.json',dict(created_utc=now(),archive_sha256=sha(archive),catalog_sha256=sha(Path('data/rv/known-planets-20261010.csv')),script_sha256=sha(Path(__file__)),total_rows=count,total_targets=len(summary),selection='>=80 quality-filtered nights, >=500day span, median formal error<=3m/s; 4000–6500K,V<10.5,d<100pc; no confirmed planet within60arcsec. Exclude external HD32564. Last25% nights reserved before any RV screen.',targets=candidates))
# Export selected series and known controls from the exact same archive.
names={r['name'] for r in candidates}|{'HD40307','HD69830'};records=defaultdict(list)
with zipfile.ZipFile(archive) as z:
 with z.open('HARPS_RVBank_ver02.csv') as stream:
  reader=csv.DictReader(io.TextIOWrapper(stream));fields=reader.fieldnames
  for r in reader:
   if r['target'] in names:records[r['target']].append(r)
exports=[]
for name,rows in records.items():
 p=Path('data/rv/coverage-selected')/(name+'.csv');p.parent.mkdir(exist_ok=True)
 with p.open('w') as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
 exports.append(dict(name=name,path=str(p),sha256=sha(p),n_rows=len(rows)))
save_json(out/'exports.json',exports)
print('archive rows',count,'targets',len(summary),'selected',len(candidates));print([(r['name'],r['nights']) for r in candidates])
