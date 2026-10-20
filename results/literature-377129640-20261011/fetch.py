from pathlib import Path
from exoplanet.pipeline import fetch,save_json,sha
out=Path(__file__).parent
url='https://assets-eu.researchsquare.com/files/rs-9006720/v1/24189093-160c-4855-ba37-71ab0cde7135.pdf?c=1773234165'
p=Path('data/literature/rs-9006720-v1.pdf')
r=fetch(url,p);save_json(out/'source.json',{'script_sha256':sha(Path(__file__)),'path':str(p),'source':r,'doi':'10.21203/rs.3.rs-9006720/v1','limits':'Preprint, not independently validated binary classification. Exact TIC/position match checked separately.'});print(p)
