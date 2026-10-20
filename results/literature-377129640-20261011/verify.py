from pathlib import Path
import json,subprocess
from astropy.coordinates import SkyCoord
from astropy import units as u
from exoplanet.pipeline import sha,save_json
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());meta=read(out/'source.json');pdf=Path(meta['path']);assert sha(pdf)==meta['source']['sha256']
text=subprocess.check_output(['pdftotext','-layout',str(pdf),'-'],text=True)
for term in ['377129640','3850549957388322816','0.821301','March 9th, 2026','J095623.83+064801.9']:assert term in text,term
path=Path('results/qlp-faint-midradius-remaining-one-20261011/targets/377129640.json');star=read(path)['target']['star'];gp=Path('results/gaia-377129640-scene-20261011');plan=read(gp/'plan.json');target=next(x for x in plan['targets'] if int(x['ID'])==377129640);assert str(target['GAIA'])=='3850549957388322816';mapping=[x for x in read(gp/'dr2_neighbourhood.json') if x['dr2_source_id']==str(target['GAIA'])];assert len(mapping)==1 and mapping[0]['dr3_source_id']=='3850549957388322816'
pos=SkyCoord('09h56m23.83s +06d48m01.9s');tic=SkyCoord(star['ra']*u.deg,star['dec']*u.deg);sep=pos.separation(tic).arcsec;assert sep<2
alias=Path('results/alias-377129640-20261011/plan.json');period=read(alias)['short_period'];reported=.821301
save_json(out/'verification.json',{'script_sha256':sha(Path(__file__)),'source_sha256':sha(out/'source.json'),'inputs':{str(p):sha(p) for p in [path,gp/'plan.json',gp/'dr2_neighbourhood.json',alias]},'tic':377129640,'gaia_dr3':'3850549957388322816','dfbs':'J095623.83+064801.9','name_coordinate_offset_arcsec':sep,'reported_period_days':reported,'our_posthoc_alias_period_days':period,'period_difference_days':reported-period,'relative_period_difference':(reported-period)/period,'status':'Exact TIC and Gaia identity verified; coordinate-name proximity checked. Prior report establishes non-novel signal, not independent physical validation. Periods are close but not identical; no timing or uncertainty agreement claimed.'})
print('Identity verified; positional difference',sep,'arcsec; period difference',reported-period,'days')
