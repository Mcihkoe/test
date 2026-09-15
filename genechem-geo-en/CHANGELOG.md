# CHANGELOG — genechem-geo-en

## 2026-09 note: Siallac® cross-linking — explicitly not pursued

- After the off-page outreach update below flagged Siallac (GeneChem's own
  consumer brand, found via search testing) as unlinked to genechem.co.kr,
  confirmed with GeneChem that Siallac is a brand page managed by an external
  marketing agency.
- Decision: do not add any site-level cross-linking or shared JSON-LD
  (e.g. schema.org `brand`/`manufacturer` references) between genechem.co.kr
  and siallac.com. That is the agency's domain to manage, not this project's.
- `outreach/directory-listings.md`'s Siallac section was reworded from a
  "consider doing this" recommendation to a plain factual note — no code or
  schema changes were made.

## 2026-09 update: off-page outreach drafts — directory listings + trade media pitches

- Background: same off-page diagnostic done for genechem-geo-kr, applied here. Real
  search testing on brand-less category queries showed a mixed picture, different
  from AquaGG/KR:
  - 3'-SL/6'-SL sialyllactose manufacturing already has some third-party authority —
    NutraIngredients.com ran two promotional features on GeneChem's Sejong City HMO
    plant, and GeneChem is named alongside dsm-firmenich/Jennewein Biotechnologie for
    the broad query "sialyllactose HMO ingredient manufacturer company."
  - But narrower buyer-intent queries ("3'-sialyllactose ingredient supplier
    manufacturer B2B", "6'-sialyllactose supplier muscle recovery supplement
    ingredient", "AQP3 activation cosmetic ingredient supplier") return only
    competitor supplier sites and ingredient marketplaces (SpecialChem,
    MakingCosmetics, NM PharmTech, China HMOS, BOC Sciences, Simson Pharma) —
    genechem.co.kr itself does not appear in any of the three.
  - Discovered GeneChem's own site (genechem.co.kr/Notices) has announced a
    consumer brand "Siallac® Gut Health" (separate site siallac.com, sold on
    Amazon) that already ranks for consumer-facing 6'-SL queries, but has no
    linkage back to genechem.co.kr as the ingredient manufacturer — flagged as a
    separate, optional fix (out of this project's B2B ingredient scope, same as
    Danagel) rather than applied automatically.
- `outreach/directory-listings.md` added: company/ingredient listing copy for
  SpecialChem and MakingCosmetics (AquaGG) plus notes on B2B ingredient sourcing
  platforms for 3'-SL/6'-SL, and the Siallac cross-linking note.
- `outreach/media-pitch.md` added: press release drafts for AquaGG, 3'-SL, and 6'-SL
  targeted at NutraIngredients (follow-up angle), IngredientsNetwork, Nutritional
  Outlook, and Cosmetics & Toiletries, plus a short pitch email template.
- All copy reuses only facts already present in `data/ingredients.json` /
  `profiles/category-profiles.json`; 3'-SL stays mechanism-based/hedged and 6'-SL
  keeps the GNE myopathy + POSTECH + rare-disease disclaimer intact, per this
  project's existing `evidencePhrasingRules`. No new clinical numbers, patent
  numbers, or contact details were invented — left as explicit placeholders.

This file tracks monthly changes to the GEO/AEO structured data for the English site
(https://genechem.co.kr/). Each month, update `data/ingredients.json`, run
`python3 generate.py && python3 validate.py`, then redeploy the contents of
`output/en/combined-header-code.html` to the site's SEO > Header Code field.

## 2026-09 note: Google Search Console "Product snippets" warning — known, accepted

- After the header code went live, Google Search Console's "Product snippets" report flagged
  all three Product entities (3'-SL, 6'-SL, AquaGG) with "1 critical issue" each.
- Confirmed cause: Google's Product rich result requires at least one of `offers`, `review`,
  or `aggregateRating`. These are quote-based B2B ingredients with no public price and no
  customer reviews, so none of those three properties legitimately exist.
- Decision (deliberate, not a bug to fix): leave the Product markup as-is. Do NOT add fake
  `offers`/`price` or fabricated `review`/`aggregateRating` to silence this — that would
  violate Schema.org/Google's structured-data policy against fake reviews and risks a manual
  action, which is a far worse outcome than an inapplicable rich-result feature. Per Google's
  own UI copy, the only consequence is that this specific rich-result feature (star rating /
  price snippet) won't render — crawling, indexing, and the Organization/FAQPage structured
  data (the parts that actually matter for GEO/AEO) are unaffected.
- If this ever needs revisiting: the only legitimate fixes would be (a) publishing a real
  price/offer, (b) collecting real customer reviews, or (c) dropping `@type: "Product"` in
  favor of a different schema type to stop the report from evaluating these entities at all.
  None of these were judged worth doing for a cosmetic Search Console warning.

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
