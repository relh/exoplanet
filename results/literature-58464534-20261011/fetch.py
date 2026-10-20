from pathlib import Path
from exoplanet.pipeline import fetch,save_json,sha
out=Path(__file__).parent
sources={
'oddo2025': 'https://arxiv.org/pdf/2508.13941v2',
'gan2023':'https://research.usq.edu.au/download/57f72496f6d854921bb37622f9ed8c4c56c79c8e9d986bba88a70a89478c079f/24998495/Gan_2023_AJ_165_17.pdf'}
for name,url in sources.items():
 p=Path(f'data/literature/{name}.pdf')
 try:save_json(out/f'{name}-source.json',{'path':str(p),'source':fetch(url,p),'script_sha256':sha(Path(__file__))})
 except Exception as exc:save_json(out/f'{name}-error.json',{'error':repr(exc),'url':url})
