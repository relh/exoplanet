"""Build the manuscript locally without downloads, shell escape, or new science."""
from pathlib import Path
import hashlib
import json
import os
import re
import shutil
import subprocess
import zipfile

HERE = Path(__file__).resolve().parent
os.chdir(HERE)
subprocess.run([os.sys.executable, "prepare_assets.py", "--check"], check=True)
latexmk = shutil.which("latexmk")
if not latexmk:
    matches = sorted((Path.home() / ".TinyTeX/bin").glob("*/latexmk"))
    if matches:
        latexmk = str(matches[0])
assert latexmk, "Install TeX Live, MiKTeX, or TinyTeX with latexmk and BibTeX; then rerun python3 build.py"
env = dict(os.environ)
env["PATH"] = str(Path(latexmk).parent) + os.pathsep + env.get("PATH", "")
env["SOURCE_DATE_EPOCH"] = "1792454400"  # 2026-10-20 00:00:00 UTC
env["FORCE_SOURCE_DATE"] = "1"
subprocess.run([latexmk, "-pdf", "-interaction=nonstopmode", "-halt-on-error", "-outdir=.build", "-pdflatex=pdflatex -no-shell-escape %O %S", "candidates.tex"], check=True, env=env)
log = Path(".build/candidates.log").read_text(errors="replace")
for pattern in [r"LaTeX Warning:.*undefined", r"Citation .* undefined", r"Reference .* undefined", r"There were undefined", r"Multiply defined", r"Float too large", r"Overfull \\hbox"]:
    assert not re.search(pattern, log), f"Unresolved build warning: {pattern}"
shutil.copyfile(".build/candidates.pdf", "candidates.pdf")
shutil.copyfile(".build/candidates.bbl", "candidates.bbl")
verification = {
    "compiled_successfully": True,
    "unresolved_citations_or_references": False,
    "oversized_floats_or_overfull_lines": False,
    "new_observing_data_or_fits": False,
    "figure_copies_verified": 24,
    "source_records_in_evidence_manifest": len(json.loads(Path("evidence-manifest.json").read_text())["source_records"]),
    "pdf_sha256": hashlib.sha256(Path("candidates.pdf").read_bytes()).hexdigest(),
    "shell_escape_enabled": False,
}
Path("build-verification.json").write_text(json.dumps(verification, indent=2) + "\n")
files = sorted([p for p in HERE.rglob("*") if p.is_file() and ".build" not in p.parts and "__pycache__" not in p.parts and p.suffix not in {".zip", ".pdf"}])
with zipfile.ZipFile("candidates-source.zip", "w", compression=zipfile.ZIP_DEFLATED) as archive:
    for p in files:
        info = zipfile.ZipInfo("candidates/" + p.relative_to(HERE).as_posix(), date_time=(2026, 10, 20, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o100644 << 16
        archive.writestr(info, p.read_bytes())
print("Built candidates.pdf and candidates-source.zip; no new observing data or scientific fits used.")
