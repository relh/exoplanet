"""Training-only visual check; retain flags and do not open reserved epochs."""
from pathlib import Path
from functools import partial
from exoplanet.plots import plot_discovery
from exoplanet.qlp_campaign import load_qlp
from exoplanet.pipeline import save_json,sha,now
out=Path(__file__).parent
source=out/'targets/30943870.json'
dest=out/'30943870-flagged.png'
assert not dest.exists()
plot_discovery(source,dest,peak_index=0,loader=partial(load_qlp,bin_minutes=0))
save_json(out/'flagged-plot.json',{'utc':now(),'source_sha256':sha(source),'script_sha256':sha(Path(__file__)),'plot_sha256':sha(dest),'policy':'Training-only diagnostic of a large-duty-cycle flagged peak. Flags unchanged; no candidate promotion; reserved epochs remain unopened.'})
