"""Fixed-ephemeris QLP measurements on discovery sectors, with aperture checks."""
import argparse,json
from pathlib import Path
import numpy as np
from astropy.io import fits
from .archive import qlp_observations,qlp_flux_columns
from .pipeline import fetch,sha,save_json,now
from .integrity import verify_hdus
from .search import flatten
from .followup import fixed_measure


def compare(discovery,output,root=Path('data'),peak_index=0,observations=None):
    row=json.loads(discovery.read_text());target=row['target'];best=row['screened_peaks'][peak_index]['best']
    output.mkdir(parents=True,exist_ok=False)
    if observations is None:
        observations,evidence=qlp_observations([row['tic']],root/'qlp-observations'/f'{row["tic"]}.json')
    else:
        path=Path(observations);payload=json.loads(path.read_text())
        if isinstance(payload,dict):payload=payload['data']
        observations=[o for o in payload if int(o['target_name'])==row['tic']]
        evidence={'source_path':str(path),'sha256':sha(path)}
    matches=[o for o in observations if o['sequence_number'] in target['training_sectors']]
    save_json(output/'run.json',{'created_utc':now(),'discovery_sha256':sha(discovery),'observation_query':evidence,
        'seed':best,'matched_training_sectors':[o['sequence_number'] for o in matches],
        'note':'Only discovery sectors opened; independent extraction of same images, not independent observations'})
    results=[]
    for obs in matches:
        sector=obs['sequence_number'];entry={'sector':sector,'status':'error'}
        try:
            path=root/'qlp'/f'{row["tic"]}-s{sector:04d}.fits'
            entry['source']=fetch('https://mast.stsci.edu/api/v0.1/Download/file/?uri='+obs['dataURL'],path)
            with fits.open(path) as hdus:
                entry['integrity']=verify_hdus(path,hdus)
                h=hdus[1].header;entry['time_reference']=h.get('BJDREFI',hdus[0].header.get('BJDREFI'))
                if entry['time_reference']!=2457000:raise ValueError('Unexpected QLP time reference')
                data=hdus[1].data;flux_col,error_col,apertures=qlp_flux_columns(data.names)
                t=np.array(data['TIME'],dtype=float);dy=np.array(data[error_col],dtype=float)
                entry['flux_column']=flux_col
                entry['apertures']={}
                for col in apertures:
                    f=np.array(data[col],dtype=float)
                    keep=(data['QUALITY']==0)&np.isfinite(t)&np.isfinite(f)&np.isfinite(dy)&(f>0)&(dy>0)
                    tt,yy,ee=flatten(t[keep],f[keep],dy[keep])
                    entry['apertures'][col]=fixed_measure(tt,yy,ee,best['period'],best['transit_time'],best['duration'])
                entry['status']='measured'
        except Exception as exc:entry['error']=f'{type(exc).__name__}: {exc}'
        results.append(entry);save_json(output/'measurements.json',results)
    print(row['tic'],[(r['sector'],r.get('apertures',{}).get(r.get('flux_column'),{}).get('total',r.get('error'))) for r in results],flush=True)
    return results


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--discovery',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True);p.add_argument('--observations',type=Path)
    p.add_argument('--peak-index',type=int,default=0)
    a=p.parse_args();compare(a.discovery,a.output,peak_index=a.peak_index,observations=a.observations)

if __name__=='__main__':main()
