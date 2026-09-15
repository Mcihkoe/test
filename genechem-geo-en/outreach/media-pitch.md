# Trade media pitch / press release drafts

Mirrors `genechem-geo-kr/outreach/media-pitch.md`. Target outlets are chosen
from what actually surfaced in 2026-09 search testing for brand-less queries:

- **NutraIngredients** — already published two promotional features on
  GeneChem's Sejong City HMO plant. Good candidate for a **follow-up** pitch
  (new angle: ingredient-level supply for 3'-SL/6'-SL) rather than a cold
  intro.
- **IngredientsNetwork**, **Nutritional Outlook** — appeared adjacent to HMO
  ingredient manufacturer results; standard nutrition-trade press targets.
- **Cosmetics & Toiletries** — appeared directly in the "AQP3 activation
  cosmetic ingredient" search result set; relevant for AquaGG.

> ⚠️ Every claim below is copied from `data/ingredients.json` /
> `profiles/category-profiles.json` as already vetted for this project. Do
> **not** add clinical numbers, percentages, or participant counts that
> aren't already in that file — 3'-SL explicitly has no in-house clinical
> data, and 6'-SL's claims must stay scoped to the GNE myopathy / POSTECH
> studies already on record, with the rare-disease disclaimer intact.

---

## Press release draft — AquaGG (cosmetic ingredient trade press)

**Headline:** GeneChem Supplies AQP3-Activating Cosmetic Ingredient AquaGG to Global Formulators

**Lead**
GeneChem Inc., a biotechnology company specializing in enzyme engineering and
glycosylation technology, supplies AquaGG (2-α-Glyceryl Glucoside), a
cosmetic functional ingredient that specifically activates Aquaporin-3
(AQP3), the key water channel protein in skin cells, to cosmetic
manufacturers and brands worldwide.

**Body**
AquaGG is produced by GeneChem via a proprietary enzymatic process and is
inspired by the Resurrection Plant's ability to retain moisture and stay
hydrated under extreme drought conditions. Unlike conventional moisturizing
ingredients such as glycerin or hyaluronic acid, which typically work by
forming a surface film or drawing in external moisture, AquaGG activates the
skin's own water transport channels directly.

The ingredient delivers deep, long-lasting hydration, a reinforced skin
barrier, and supported collagen/elastin production for improved elasticity.
AquaGG is a high-purity ingredient (over 90% purity), water-soluble, and
stable across a pH 3-9 range, making it straightforward to formulate into a
wide range of cosmetic products.

[Specific institution, publication year, and result figures to be added once
available — not yet confirmed.]

AquaGG is supplied to cosmetic manufacturers and brands both domestically in
Korea and internationally.

**Company boilerplate**
GeneChem Inc. is a biotechnology company specializing in enzyme engineering
and glycosylation technology, producing functional ingredients via
proprietary enzymatic processes for the food, supplement, and cosmetic
industries. https://genechem.co.kr/

**Media contact**
- Name: [ ]
- Phone: [ ]
- Email: [ ]

---

## Press release draft — 3'-Sialyllactose (HMO / nutrition trade press)

**Headline:** GeneChem Supplies 3'-Sialyllactose (3'-SL), an HMO-Derived Ingredient Explored for Gut Health

**Lead**
GeneChem Inc. supplies 3'-Sialyllactose (3'-SL), a human milk oligosaccharide
(HMO)-derived functional ingredient produced via a proprietary enzymatic
process, to supplement and food manufacturers worldwide.

**Body**
As an HMO-derived ingredient, 3'-SL is being explored for its potential to
strengthen the gut mucosal barrier, help modulate the gut microbiome, and
help reduce inflammation, based on the known mechanism of HMOs and
structural rationale. Based on this same mechanism, 3'-SL is also being
explored for potential relevance to joint nutrition.

No in-house clinical trial data is currently available for 3'-SL. These
statements are mechanism-based and exploratory, grounded in the established
mechanism of HMOs and structural rationale, and should not be interpreted as
proven clinical efficacy.

3'-SL is covered under GeneChem's sialyllactose composition patents (specific
patent numbers to be confirmed). It is supplied for export/overseas markets
only and is not available for the domestic Korean market.

**Company boilerplate**
GeneChem Inc. is a biotechnology company specializing in enzyme engineering
and glycosylation technology, operating a commercial-scale sialyllactose
production facility in Sejong City, Korea. https://genechem.co.kr/

**Media contact**
- Name: [ ]
- Phone: [ ]
- Email: [ ]

---

## Press release draft — 6'-Sialyllactose (sports nutrition trade press)

**Headline:** GeneChem's 6'-Sialyllactose (6'-SL) Shows Muscle-Physiology Benefits in Rare-Disease Pilot Trial and POSTECH Exercise Study

**Lead**
GeneChem Inc. supplies 6'-Sialyllactose (6'-SL), a human milk oligosaccharide
(HMO)-derived functional ingredient, to supplement and sports nutrition
manufacturers, with clinical and research data supporting its role in
muscle physiology.

**Body**
In a pilot clinical trial in patients with GNE myopathy, a rare genetic
muscle disease, participants underwent a 12-week treatment with high-dose
(6g/day) or low-dose (3g/day) 6'-SL. Free sialic acid levels increased
significantly from baseline in both dose groups after 12 weeks. At 96 weeks,
the high-dose group showed improving trends in motor function measures, such
as hand grip strength and hip flexion. These results reflect a rare-disease
patient population (GNE myopathy) and should not be generalized as
muscle-building efficacy claims for the general healthy population or
typical sports nutrition consumers.

Separately, in a collaborative study with Pohang University of Science and
Technology (POSTECH), 6'-SL demonstrated a measurable effect on exercise
performance and muscle strength. This study was published and indexed on
PubMed.

6'-SL is covered under GeneChem's sialyllactose composition patents (specific
patent numbers to be confirmed). It is supplied for export/overseas markets
only and is not available for the domestic Korean market.

**Company boilerplate**
GeneChem Inc. is a biotechnology company specializing in enzyme engineering
and glycosylation technology, operating a commercial-scale sialyllactose
production facility in Sejong City, Korea. https://genechem.co.kr/

**Media contact**
- Name: [ ]
- Phone: [ ]
- Email: [ ]

---

## Short pitch email (any of the three, adapt subject/ingredient)

**Subject:** [Press release] GeneChem — [ingredient name] for [manufacturer audience]

Hi [editor name],

I'm reaching out from GeneChem Inc., a biotechnology company specializing in
enzyme engineering and glycosylation technology. [If pitching NutraIngredients:
"Following your coverage of our Sejong City HMO production facility, I wanted
to share an update on..."] We supply [ingredient name] to [supplement / food /
cosmetic] manufacturers, and thought it might be a fit for [outlet name]'s
ingredient coverage.

I've attached a press release with the details. Happy to provide additional
technical data sheets or connect you with our R&D team for further
background.

Thank you for considering,
[Name], GeneChem Inc.
[Phone] / [Email]

---

## Pre-send checklist

- [ ] No clinical numbers/percentages added beyond what's in `data/ingredients.json`
- [ ] 3'-SL copy stays hedged (mechanism-based / exploratory language only)
- [ ] 6'-SL copy keeps GNE myopathy + POSTECH + rare-disease disclaimer together, never split apart
- [ ] Contact name/phone/email filled with real information
- [ ] Patent numbers added once `organization.patents.patentNumbers` is populated
- [ ] For NutraIngredients specifically: reference the existing 2022 promotional
      features as context, don't pitch as if this is the first contact
- [ ] After publication, confirm the article links back to genechem.co.kr
