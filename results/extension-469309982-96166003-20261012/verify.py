from pathlib import Path
import json,csv,hashlib,math
O=Path(__file__).parent
records=[r for name in ['queries.json','follow.json','tables.json'] for r in json.loads((O/name).read_text())]
parsed={}
for r in records:
 assert r['status']==200;p=Path(r['path']);assert hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256']
 if p.suffix=='.csv' or r['name']=='cluster-tables':parsed[r['name']]=list(csv.DictReader(p.open()))
for tic,date,g,dr1,hd in [(469309982,'20261011','5259582389096040960','5259582384786570368','HD 300413'),(96166003,'20261012','161856980718462208','161856976421129472','HD 282445')]:
 p=Path(f'data/catalogs/neighbors-{tic}-{date}.json');x=json.loads(p.read_text());x=x['data'] if isinstance(x,dict) else x;row=next(v for v in x if int(v['ID'])==tic);assert str(row['GAIA'])==g
 aliases={v['id'] for v in parsed[f'{tic}-aliases']};assert {f'TIC {tic}',f'Gaia DR3 {g}',f'Gaia DR1 {dr1}',f'2MASS J{row["TWOMASS"]}',hd} <=aliases
 ident=parsed[f'{tic}-identity'][0];assert ident['main_id']==hd;assert abs(float(ident['ra'])-row['ra'])<.00001;assert abs(float(ident['dec'])-row['dec'])<.00001
row=parsed['469-cluster'][0];assert row['Source']=='5259582384786570368';assert row['TYC2'].strip()=='8606-1845-1';assert row['Cluster']=='Platais_8' and float(row['Pfinal'])==0
row=parsed['961-simulated'][0];assert row['TICID']=='96166003' and float(row['Perp'])==15.592607
row=parsed['961-lowextinction'][0];assert row['Source']=='161856976421129472' and row['2MASS']=='04502136+3342255';assert float(row['E(B-V)max'])==.0103
text=Path('data/extension-469309982-96166003-20261012/yield-readme.response').read_text();assert 'planet in our simulation' in text
out=dict(verified=True,response_hashes=len(records),counts={k:len(v) for k,v in parsed.items()},scope='Independent CSV parsing; exact Gaia release aliases, TIC, Tycho and 2MASS identities; matched-table assertions and simulation scope. No physical validation.');(O/'verification.json').write_text(json.dumps(out,indent=2));print(json.dumps(out))
