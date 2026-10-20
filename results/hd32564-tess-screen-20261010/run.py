"""First-sector transit screen of an identified external RV lead."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json
from exoplanet.pipeline import save_json,sha,now
from exoplanet.campaign import process_target,load_training
from exoplanet.qlp_campaign import load_qlp
out=Path(__file__).parent;identity=Path('results/hd32564-tess-identity-20261010');star=json.loads((identity/'identity.json').read_text())['star'];tic=int(star['ID']);obs=json.loads((identity/'observations.json').read_text());products={str(r['sequence_number']):r for r in obs if r['provenance_name']=='QLP'}
target={'tic':tic,'star':star,'training_sectors':[5],'heldout_sectors':[32,98],'qlp_products':products,'estimate_missing_errors':True}
assert not (out/'plan.json').exists()
save_json(out/'plan.json',{'utc':now(),'target':target,'identity_sha256':sha(identity/'identity.json'),'observations_sha256':sha(identity/'observations.json'),'source_hashes':{p.name:sha(p) for p in Path('src/exoplanet').glob('*.py')},'cache_present_before':{f'{kind}-{s}':path.exists() for s in [5,32,98] for kind,path in [('qlp',Path(f'data/qlp/{tic}-s{s:04d}.fits')),('spoc',Path(f'data/lightcurves/s{s:04d}-{tic}.fits'))]},'policy':'External RV lead HD32564=TIC213078996 verified through SIMBAD TIC/HIP/Gaia IDs. Earliest Sector5 discovery;32/98reserved. Same original blind0.5..20day box screen and gates, in QLP and TESS-SPOC FFI reductions of same images. Not two independent observations. No sensitivity to all orientations or long-period planets; not a novelty claim.'})
def work(item):
 name,loader=item;dest=out/name;(dest/'targets').mkdir(parents=True)
 r=process_target(target,Path('data'),dest,loader,120)
 return {k:r.get(k) for k in ['tic','status','error','disposition','best']}|{'reduction':name,'path':str(dest/'targets'/f'{tic}.json')}
with ThreadPoolExecutor(max_workers=2) as ex:rows=list(ex.map(work,[('qlp',load_qlp),('spoc',load_training)]))
save_json(out/'results.json',rows);print(rows,flush=True)
