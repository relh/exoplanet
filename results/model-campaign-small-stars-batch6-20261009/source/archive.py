"""Cached MAST observation queries with explicit provenance and completeness checks."""
import json
from pathlib import Path
import requests
from .pipeline import sha,save_json,now


def mast_query(request,path):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    meta=path.with_suffix('.provenance.json')
    if path.exists() and meta.exists():
        evidence=json.loads(meta.read_text())
        if evidence['request']!=request or evidence['sha256']!=sha(path):
            raise ValueError('MAST cache/request mismatch')
    else:
        response=requests.post('https://mast.stsci.edu/api/v0/invoke',
            data={'request':json.dumps(request)},timeout=(20,180))
        response.raise_for_status()
        data=response.json()
        if data.get('status')!='COMPLETE':
            raise ValueError(f'MAST query incomplete: {data.get("status")}: {data.get("msg")}')
        path.write_text(response.text)
        evidence={'url':response.url,'request':request,'retrieved_utc':now(),
                  'sha256':sha(path),'bytes':path.stat().st_size}
        save_json(meta,evidence)
    data=json.loads(path.read_text())
    if data.get('status')!='COMPLETE':raise ValueError('Cached MAST query incomplete')
    if len(data['data'])!=data['paging']['rowsFiltered']:
        raise ValueError('MAST query exceeds page size; split into smaller queries')
    return data['data'],evidence


def qlp_observations(tics,path):
    query={'service':'Mast.Caom.Filtered','params':{
        'columns':'obs_id,target_name,provenance_name,sequence_number,dataURL',
        'filters':[{'paramName':'target_name','values':[str(t) for t in sorted(tics)]},
                   {'paramName':'provenance_name','values':['QLP']}]},
        'format':'json','pagesize':50000,'page':1}
    return mast_query(query,path)


def qlp_flux_columns(names):
    """QLP renamed KSP columns to DET starting with its EM2 products.

    https://tess.mit.edu/qlp-update/ (Changes to MAST QLP light curves for EM2)
    """
    for prefix in ['DET_FLUX','KSPSAP_FLUX']:
        if prefix in names and prefix+'_ERR' in names:
            return prefix,prefix+'_ERR',[c for c in [prefix,prefix+'_SML',prefix+'_LAG'] if c in names]
    raise ValueError('Unsupported QLP flux schema')
