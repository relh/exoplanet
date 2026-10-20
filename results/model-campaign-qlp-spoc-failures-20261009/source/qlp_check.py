"""Reproduce initial cross-extraction checks of three inspected campaign leads."""
import json
from pathlib import Path
import numpy as np
from astropy.io import fits
from .followup import fixed_measure
from .search import flatten
from .pipeline import save_json
from .integrity import verify_hdus


def main():
    output=Path('results/inspection-small-stars-20261009')
    products=json.loads((output/'qlp-products.json').read_text())
    products += json.loads((output/'qlp-467361658-products.json').read_text())
    rows=[]
    for product in products:
        p=Path(product['local_path'])
        with fits.open(p) as h:
            d=h[1].data
            t,f,e=(np.array(d[k],dtype=float) for k in ['TIME','KSPSAP_FLUX','KSPSAP_FLUX_ERR'])
            good=(d['QUALITY']==0)&np.isfinite(t)&np.isfinite(f)&np.isfinite(e)&(f>0)&(e>0)
            tic=int(product['observation']['target_name']);sector=int(product['observation']['sequence_number'])
            item={'tic':tic,'sector':sector,'source':product['source'],
                'integrity':verify_hdus(p,h),'time_reference':h[1].header.get('BJDREFI',h[0].header.get('BJDREFI')),
                'note':'QLP and TESS-SPOC use the same images. Missing HDU checksums are recorded; HTTPS download SHA-256 provenance is retained.'}
            if item['time_reference']!=2457000:raise ValueError('Unexpected time reference')
            if tic in [311931991,178278439]:
                center=1809.2554553184896 if tic==311931991 else 2576.5637702019512
                inside=abs(t-center)<(.06 if tic==311931991 else .09)
                outside=(abs(t-center)>.2)&(abs(t-center)<.6)
                item.update(event_btjd=center,n_event_all=int(inside.sum()),
                    n_event_quality_zero=int((inside&good).sum()),
                    event_quality_flags=np.unique(d['QUALITY'][inside]).tolist())
                item['aperture_depths']={}
                for column in ['SAP_FLUX','KSPSAP_FLUX','KSPSAP_FLUX_SML','KSPSAP_FLUX_LAG']:
                    a=np.array(d[column],dtype=float)
                    item['aperture_depths'][column]=float(1-np.nanmedian(a[inside&good])/np.nanmedian(a[outside&good]))
            else:
                frozen=json.loads(Path(f'results/followup-{tic}-20261009/frozen.json').read_text())['best']
                tt,yy,ee=flatten(t[good],f[good],e[good])
                item['measurement']=fixed_measure(tt,yy,ee,frozen['period'],frozen['transit_time'],frozen['duration'])
            rows.append(item)
    save_json(output/'qlp-checks.json',rows)
    for row in rows:print(row['tic'],row['sector'],row.get('aperture_depths',row.get('measurement',{}).get('total')))

if __name__=='__main__':
    main()
