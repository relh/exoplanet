from pathlib import Path
import json
from exoplanet.pipeline import save_json,sha,now
O=Path(__file__).parent;p=json.loads((O.parent/'plan.json').read_text());rows=[]
for sector in [36,37]:
 for product in ['SPOC','QLP']:
  f=Path(f'data/lightcurves/s{sector:04d}-80387959.fits') if product=='SPOC' else Path(f'data/qlp/80387959-s{sector:04d}.fits');rows.append(dict(sector=sector,product=product,path=str(f),sha256=sha(f),provenance=json.loads(Path(str(f)+'.json').read_text()),flux='PDCSAP_FLUX' if product=='SPOC' else 'KSPSAP_FLUX',error='PDCSAP_FLUX_ERR' if product=='SPOC' else 'KSPSAP_FLUX_ERR'))
save_json(O/'plan.json',dict(utc=now(),parent_plan_sha256=sha(O.parent/'plan.json'),parent_results_sha256=sha(O.parent/'results.json'),best=p['best'],inputs=rows,policy='Separatelyfrozen comparison of same-sectorSPOC/QLP36/37 cachedphotons; no newdata. Matchunique nearesttimestamps within1e-4day8.64sec; qualityzero finitepositiveflux/errorsinboth; median-normalizeeachonmatchedsamples. Identicaleventeligibility/localbaseline andoriginalclock asparent. Nativecadenceschecked; exposureintegratedbox usingeachproductsmediancadence (commonmidpointtime). Fitprimary+eventbaselines only; no phase/period/depth/shapeoptimization. Alsofitnormalizedpairedfluxdifference withequalweights andresidualcovariance; sharedphotons meansnotindependentobservations, uncertaintyconditionalnotcalibrated. Omitindividualevents. Reportsign/magnitude ofproductoffsetandwhether itcanaccountforsomecross-epochdifference; nottotalastrophysicalexclusion. Noextra product/sector matrix.'))
