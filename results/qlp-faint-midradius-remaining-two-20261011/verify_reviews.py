"""Inventory completed initial reviews without treating them as candidate validation."""
from pathlib import Path
import json
from exoplanet.pipeline import sha,save_json,now
out=Path(__file__).parent;read=lambda p:json.loads(p.read_text());terminal=read(out/'terminal-verification.json');rows=[]
for item in terminal['followups']:
 p=Path(item['path']);r=read(p/'review.json');f=read(p/'frozen.json');parent=out/'targets'/f"{item['tic']}.json"
 assert sha(parent)==f['discovery_sha256']
 for n,h in item['artifacts'].items():assert sha(p/n)==h
 for n,h in r['artifacts'].items():assert sha(p/n)==h
 assert r['artifacts']['ASSESSMENT.md']==sha(p/'ASSESSMENT.md')
 rows.append({'tic':item['tic'],'peak_index':item['peak_index'],'path':str(p),'review_sha256':sha(p/'review.json'),'assessment_sha256':sha(p/'ASSESSMENT.md'),'has_source_review':(p/'source_review.json').exists(),'initial_review_complete':True})
assert len(rows)==71 and len({(r['tic'],r['peak_index']) for r in rows})==71
save_json(out/'review-inventory.json',{'utc':now(),'script_sha256':sha(Path(__file__)),'terminal_verification_sha256':sha(out/'terminal-verification.json'),'n_initial_reviews':len(rows),'rows':rows,'limits':'Verifies artifact identity and presence of initial assessments for all71 completed followups. Plot interpretation was recorded during individual reviews. Presence of a source report is not host attribution or completion of scientific vetting. Review inventory does not promote any result to planet candidate.'})
print('Verified all 71 initial review artifact sets.')
