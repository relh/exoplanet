"""Verify the data failure and the separately frozen two-sector search."""
from pathlib import Path
import json
import numpy as np
from astropy.io import fits
from exoplanet.pipeline import save_json,sha,now
from exoplanet.archive import qlp_flux_columns
from exoplanet.integrity import verify_hdus
out=Path(__file__).parent
read=lambda p:json.loads(p.read_text())
plan=read(out/'plan.json');assert sha(Path(plan['original_path']))==plan['original_sha256']
checks=read(out/'sector-checks.json');selection=read(out/'selection.json')
assert selection['usable_sectors']==[44, 46]
assert sha(out/'sector-checks.json')==selection['sector_checks_sha256']
for row in checks:
    raw=Path(f"data/qlp/63168863-s{row['sector']:04d}.fits")
    assert sha(raw)==row['raw_sha256']==row['download_provenance']['sha256']
raw=Path('data/qlp/63168863-s0045.fits')
with fits.open(raw) as h:
    integrity=verify_hdus(raw,h)
    assert h[0].header['TICID']==63168863 and h[0].header['SECTOR']==45
    d=h[1].data;fc,ec,_=qlp_flux_columns(d.names)
    finite_flux=int(np.isfinite(d[fc]).sum())
    assert finite_flux==0
result=read(out/'targets/63168863.json')
assert result['status']=='screened' and result['target']==selection['target']
assert result['started_utc']>=selection['utc']
assert result['target']['heldout_sectors']==plan['target']['heldout_sectors']
assert all(not Path(f'data/qlp/63168863-s{s:04d}.fits').exists() for s in result['target']['heldout_sectors'])
save_json(out/'verification.json',{'utc':now(),'script_sha256':sha(Path(__file__)),
    'original_sha256':plan['original_sha256'],'result_sha256':sha(out/'targets/63168863.json'),
    'selection_sha256':sha(out/'selection.json'),'sector45_raw_sha256':sha(raw),'integrity':integrity,
    'sector45_flux_column':fc,'sector45_n_rows':len(d),'sector45_finite_flux':finite_flux,
    'recovered_sectors':[44, 46],'disposition':result['disposition'],
    'limits':'No finite selected flux in Sector45; original three-sector failure retained. Two-sector alternate search adds usable coverage, not another star or a full three-sector nondetection.'})
print('Sector45 has no finite selected flux; two-sector recovery verified')
