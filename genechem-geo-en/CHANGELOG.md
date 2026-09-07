# CHANGELOG — genechem-geo-en

This file tracks monthly changes to the GEO/AEO structured data for the English site
(https://genechem.co.kr/). Each month, update `data/ingredients.json`, run
`python3 generate.py && python3 validate.py`, then redeploy the contents of
`output/en/combined-header-code.html` to the site's SEO > Header Code field.

## 2026-09 update: initial 3'-SL / 6'-SL / AquaGG data

- Initial folder structure and generate/validate pipeline built (`data/`, `profiles/`, `templates/`, `generate.py`, `validate.py`), structurally parallel to `genechem-geo-kr`.
- `data/ingredients.json`: drafted all three categories
  - Category A (3'-SL): mechanism-based, hedged gut/joint health claims; explicitly states no in-house clinical data; export/overseas-only scope.
  - Category B (6'-SL): muscle growth/recovery claims backed by the GNE myopathy pilot trial (rare-disease framing) and the POSTECH exercise-performance study; export/overseas-only scope.
  - Category C (AquaGG): AQP3 activation mechanism, purity/solubility/pH specs, Resurrection Plant origin story, domestic + international scope.
- `profiles/category-profiles.json`: required fields, FAQ patterns, and evidence-phrasing rules per category (A: forbid clinical-proof language; B: require GNE myopathy + POSTECH references and rare-disease disclaimer; C: keyword relevance evidence for hydration-related terms).
- `templates/`: Organization, Product (ingredient), FAQPage JSON-LD templates.
- `output/en/`: first `generate.py` run output (organization.html, {3-sl,6-sl,aquagg}-product.html, {3-sl,6-sl,aquagg}-faq.html, combined-header-code.html).
- TODO: add specific patent numbers once confirmed; add AquaGG clinical study institution/year/figures once available.
