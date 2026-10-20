from pathlib import Path
from functools import partial
from exoplanet.plots import plot_discovery
from exoplanet.qlp_campaign import load_qlp
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent
source=Path('results/qlp-faint-one-reserved-sector78-pilot-20261010/targets/355734358.json')
save_json(out/'plan.json',{'utc':now(),'source_sha256':sha(source),'script_sha256':sha(Path(__file__)),'policy':'Postselected highest formal-SNR flagged signal; training-only visual diagnostic, no reserved epoch opened or gates changed.'})
plot_discovery(source,out/'355734358.png',peak_index=0,loader=partial(load_qlp,bin_minutes=0))
save_json(out/'plot.json',{'utc':now(),'sha256':sha(out/'355734358.png')})
