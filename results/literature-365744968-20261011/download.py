from pathlib import Path
from exoplanet.pipeline import fetch,save_json,sha
out=Path(__file__).parent
p=Path('data/literature/bell-2017-32ori.pdf')
save_json(out/'source.json',fetch('https://arxiv.org/pdf/1703.00015',p))
save_json(out/'download.json',{'script_sha256':sha(Path(__file__)),'path':str(p)})
