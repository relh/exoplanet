# Candidate manuscript

[Read the PDF](candidates.pdf), edit [the LaTeX manuscript](candidates.tex), or download the [standalone source package](candidates-source.zip).

Author: Richard Higgins, richard@relh.net. Prepared 20 October 2026 from evidence assessed through 13 October 2026. The paper covers all six unresolved signals, with 24 original diagnostic charts, search and control results, adopted clocks, catalog context, source ambiguity, conditional model weights and failed checks. It reports no validated planet or established novelty. No new observing epochs or scientific fits were used to prepare it.

With a standard TeX installation containing `latexmk`, `pdflatex`, BibTeX and the packages named in the source, run:

```sh
cd paper
python3 build.py
```

The build verifies figure hashes, writes auxiliary files under ignored `.build/`, and creates `candidates.pdf` and `candidates-source.zip`. It performs no network access or shell escape. You can also compile `candidates.tex` directly with `latexmk -pdf candidates.tex`; `candidates.bbl` is included for systems without BibTeX.

[evidence-manifest.json](evidence-manifest.json) maps every copied figure to its original repository path and SHA-256 and hashes the selected reports, numerical records, plans and scientific source files. [evidence-index.tex](evidence-index.tex) contains pinned links to the principal reports. The archive includes the figure copies and bibliography needed for a standalone build; the larger numerical evidence stays in the public research repository.

To verify the saved figures and, when available, repository evidence:

```sh
python3 prepare_assets.py --check
```

`prepare_assets.py` without `--check` refreshes copies and the index from the repository. Use that only for an intentional manuscript evidence update; it does not rerun experiments. Privacy amendments to historical plans are documented in the repository, and do not create new blind tests.

This is a preprint draft for author review. It has not been submitted to a journal or preprint server. Public repository release does not constitute external candidate submission, telescope booking or outreach. Original writing/code use the repository license; credited third-party data retain their terms.
