"""Re-evaluate extended diagnostics without overwriting or rerunning discovery."""
import argparse
import json
from pathlib import Path
from .campaign import load_training
from .vetting import extended_vetting
from .pipeline import save_json,sha,now


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--campaign',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    run=json.loads((args.campaign/'run.json').read_text())
    if run['status']!='complete':parser.error('Rescreen only completed campaigns')
    args.output.mkdir(parents=True,exist_ok=False)
    rows=[]
    for path in sorted((args.campaign/'targets').glob('*.json')):
        row=json.loads(path.read_text())
        if not row.get('screened_peaks'):continue
        t,y,dy,_=load_training(row['target'],Path('data'))
        peaks=[]
        for i,p in enumerate(row['screened_peaks']):
            old=p.get('extended_vetting',{}).get('flags',[])
            retained=[f for f in p['flags'] if f not in old]
            new=extended_vetting(t,y,dy,p['best'],p['diagnostics'])
            peaks.append({'index':i,'best':p['best'],'flags':retained+new['flags'],'extended_vetting':new})
        rows.append({'tic':row['tic'],'discovery_sha256':sha(path),'peaks':peaks,
                     'followup_priority':any(not p['flags'] for p in peaks)})
        save_json(args.output/'results.json',rows)
    save_json(args.output/'run.json',{'finished_utc':now(),'reason':'Allow two-point noise bins for short-duration low-cadence transits',
        'campaign':str(args.campaign),'campaign_run_sha256':sha(args.campaign/'run.json'),
        'source_sha256':{p.name:sha(p) for p in Path(__file__).parent.glob('*.py')},
        'n_targets_with_screened_peaks':len(rows),'followup_tics':[r['tic'] for r in rows if r['followup_priority']]})
    print('Follow-up priorities:',[r['tic'] for r in rows if r['followup_priority']],flush=True)

if __name__=='__main__':main()
