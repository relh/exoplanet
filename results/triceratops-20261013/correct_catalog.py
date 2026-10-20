from pathlib import Path
import pandas as pd,numpy as np,json,hashlib,datetime,shutil
from triceratops.triceratops import target
R=Path('results/triceratops-20261013');D=R/'original-catalog';D.mkdir(exist_ok=True)
records=[]
for tic in [80387959,402358350]:
 df=pd.read_csv(R/f'{tic}-stars.csv',dtype={'ID':str,'GAIA':str,'duplicate_id':str});dups=[]
 for i,row in df.iterrows():
  if row.get('disposition')!='DUPLICATE':continue
  alternatives=df[(df.ra==row.ra)&(df.dec==row.dec)&(df.Tmag==row.Tmag)&(df.GAIA==row.GAIA)&(df.ID!=row.ID)]
  if len(alternatives):dups.append(dict(remove=str(row.ID),keep=str(alternatives.iloc[0].ID),row_index=int(i),reason='Exact RA/Dec/Tmag/GaiaID match and explicit TIC DUPLICATE flag'))
 records.append(dict(tic=tic,duplicates=dups,original_stars_sha256=hashlib.sha256((R/f'{tic}-stars.csv').read_bytes()).hexdigest()))
(R/'catalog-correction-plan.json').write_text(json.dumps(dict(created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),records=records,interpretation='Remove only catalog duplicates with exact identity evidence; preserve all originalinputs and rawcatalog runs. Correctedrows represent same physicalstar once. Existing40210000smokeinvalid as adopted probability because duplicated flux/scenarios.'),indent=2))
for r in records:
 if not r['duplicates']:continue
 tic=r['tic'];df=pd.read_csv(R/f'{tic}-stars.csv',dtype={'ID':str,'GAIA':str,'duplicate_id':str});z=np.load(R/f'{tic}-input.npz');m=json.loads((R/f'{tic}-input.json').read_text());keep=~df.ID.isin([x['remove'] for x in r['duplicates']]);a=target.__new__(target);a.stars=df[keep].reset_index(drop=True);a.pix_coords=[z['pix_coords'][keep.values]];a.calc_depths(m['depth'],[z['aperture']],dilution_corrected=False)
 for suffix in ['stars.csv','input.npz','input.json']:shutil.copy2(R/f'{tic}-{suffix}',D/f'{tic}-{suffix}')
 a.stars.to_csv(R/f'{tic}-stars.csv',index=False);np.savez_compressed(R/f'{tic}-input.npz',**{k:(a.pix_coords[0] if k=='pix_coords' else z[k]) for k in z.files});m['modeled_target_fraction']=float(a.stars.fluxratio.iloc[0]);m['catalog_correction']=r['duplicates'];(R/f'{tic}-input.json').write_text(json.dumps(m,indent=2));print(tic,r['duplicates'],flush=True)
