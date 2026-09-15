# B2B ingredient directory / marketplace listing drafts

This document mirrors `genechem-geo-kr/outreach/directory-listings.md`, adapted to
what real search testing (2026-09) showed for the English/export site.

**Key finding:** unlike AquaGG in the Korean market, GeneChem's sialyllactose
business already has some third-party coverage (two NutraIngredients.com
promotional features about the Sejong City HMO plant), and shows up when the
query is broad enough ("sialyllactose HMO ingredient manufacturer company").
But narrower, buyer-intent queries ("3'-sialyllactose ingredient supplier
manufacturer B2B", "AQP3 activation cosmetic ingredient supplier",
"6'-sialyllactose supplier muscle recovery supplement ingredient") return
only competitor supplier sites and ingredient marketplaces — genechem.co.kr
itself is absent from all three.

**Target platforms** (confirmed appearing for these exact queries in 2026-09):
- **SpecialChem — Cosmetic Ingredients Master Catalog** (specialchem.com/cosmetics) — for AquaGG
- **MakingCosmetics** (wholesale cosmetic ingredient supplier listings) — for AquaGG
- Sialyllactose/HMO ingredient sourcing is dominated by direct competitor sites
  rather than neutral directories, so for 3'-SL/6'-SL the higher-leverage move
  is a **B2B ingredient sourcing platform listing** (e.g. Knowde, IngredientsNetwork,
  ECHEMI) rather than a "directory" in the KR sense — see note in section 4.

> ⚠️ Each platform has its own listing/verification process (company
> registration, sometimes a paid or accredited-supplier tier). The copy below
> is submission text; the actual account setup and any fees are a separate,
> internal decision GeneChem needs to make per platform.

---

## 1. Company profile (for listing forms)

### Short version (~40 words)
> GeneChem Inc. is a biotechnology company specializing in enzyme engineering
> and glycosylation technology, producing functional ingredients — including
> 3'-Sialyllactose, 6'-Sialyllactose, and AquaGG — via proprietary enzymatic
> processes for the food, supplement, and cosmetic industries.

### Long version (~120 words)
> GeneChem Inc. is a biotechnology company specializing in enzyme engineering
> and glycosylation technology. Through proprietary enzymatic processes,
> GeneChem produces functional ingredients for the food, supplement, and
> cosmetic industries, including human milk oligosaccharide (HMO)-derived
> ingredients 3'-Sialyllactose and 6'-Sialyllactose, and the cosmetic
> ingredient AquaGG (2-α-Glyceryl Glucoside). GeneChem operates a
> commercial-scale sialyllactose production facility in Sejong City, Korea.
> GeneChem holds patents related to sialyllactose compositions and its
> enzymatic production processes. 3'-SL and 6'-SL are supplied for
> export/overseas markets only; AquaGG is supplied both domestically and
> internationally.

---

## 2. Ingredient listings

### AquaGG (for SpecialChem / MakingCosmetics-type cosmetic ingredient catalogs)

| Field | Value |
|---|---|
| Ingredient name | AquaGG |
| INCI name | 2-α-Glyceryl Glucoside |
| Category | Cosmetic functional ingredient (hydration) |
| Mechanism | Specifically activates Aquaporin-3 (AQP3), the key water channel protein in skin cells |
| Key effects | Deep, long-lasting hydration; reinforced skin barrier; supported collagen/elastin production for improved elasticity |
| Purity | Over 90% |
| Solubility | Water-soluble |
| pH stability | pH 3-9 |
| Origin | Inspired by the Resurrection Plant's ability to retain moisture under extreme drought |
| Supply scope | Domestic (Korea) and international |
| Production | Proprietary enzymatic process |

**One-paragraph listing description:**
> AquaGG (2-α-Glyceryl Glucoside) is a cosmetic functional ingredient produced
> by GeneChem via a proprietary enzymatic process. It specifically activates
> Aquaporin-3 (AQP3), the skin's key water channel protein, delivering deep,
> long-lasting hydration, a reinforced skin barrier, and supported
> collagen/elastin production for improved elasticity. It is a high-purity
> (over 90%) ingredient, water-soluble, and stable across pH 3-9, making it
> suitable for a wide range of cosmetic formulations.

### 3'-Sialyllactose (3'-SL) — for HMO/nutrition ingredient sourcing platforms

> ⚠️ Per this project's evidence-phrasing rules, 3'-SL has **no in-house
> clinical trial data**. Any listing copy must stay mechanism-based/hedged —
> never state or imply proven efficacy.

**One-paragraph listing description:**
> 3'-Sialyllactose (3'-SL) is a human milk oligosaccharide (HMO)-derived
> functional ingredient produced by GeneChem via a proprietary enzymatic
> process, supplied as a B2B ingredient for supplement and food
> manufacturers. As an HMO-derived ingredient, 3'-SL is being explored for
> its potential to support the gut mucosal barrier, help modulate the gut
> microbiome, and help reduce inflammation, based on the known mechanism of
> HMOs and structural rationale. No in-house clinical trial data is
> currently available for 3'-SL. Supply scope: overseas/export only (not
> available for the domestic Korean market).

### 6'-Sialyllactose (6'-SL) — for HMO/sports nutrition ingredient sourcing platforms

> ⚠️ Must keep the GNE myopathy + POSTECH framing and rare-disease disclaimer
> intact per this project's evidence rules — never generalize the GNE trial
> results to "muscle building for general/healthy users."

**One-paragraph listing description:**
> 6'-Sialyllactose (6'-SL) is a human milk oligosaccharide (HMO)-derived
> functional ingredient produced by GeneChem via a proprietary enzymatic
> process, supplied as a B2B ingredient for supplement and sports nutrition
> manufacturers supporting muscle growth, muscle recovery, and strength.
> Clinical and research data support 6'-SL's role in muscle physiology,
> including a pilot clinical trial in patients with GNE myopathy (a rare
> genetic muscle disease) and a collaborative exercise-performance study with
> Pohang University of Science and Technology (POSTECH), published and
> indexed on PubMed. The GNE myopathy trial results reflect a rare-disease
> patient population and should not be generalized as muscle-building
> efficacy claims for the general healthy population or typical sports
> nutrition consumers. Supply scope: overseas/export only (not available for
> the domestic Korean market).

---

## 3. Fields to fill in (GeneChem internal info — not fabricated)

- Contact name / department:
- Phone:
- Email:
- Business registration number:
- Official site: https://genechem.co.kr/ (EN) / https://genechem.imweb.me/ (KR, AquaGG domestic only)
- Patent numbers: (held, per `organization.patents.note`; specific numbers to be
  added once `data/ingredients.json` → `organization.patents.patentNumbers` is filled)

---

## 4. Note on Siallac® — an existing asset worth connecting

Search testing turned up something not previously captured in this project's
data: GeneChem's own site (genechem.co.kr/Notices) has announced **"Siallac®
Gut Health"** as one of its own brands, and a separate site (siallac.com,
with Amazon listings) already ranks for consumer-facing 3'-SL/6'-SL queries
("6'-sialyllactose supplier muscle recovery supplement ingredient").

This is a downstream consumer brand, out of scope for this B2B ingredient
GEO system per this project's own scope note (finished consumer products are
excluded, same as Danagel). Confirmed with GeneChem: Siallac is a brand page
managed by an external marketing agency, so cross-linking or connecting it
to genechem.co.kr (site-level links, shared JSON-LD, etc.) is **not** being
pursued — that's the agency's domain to manage, not this project's. No
action taken here; this note is kept only as a factual record of what
search testing found, not a recommendation.
