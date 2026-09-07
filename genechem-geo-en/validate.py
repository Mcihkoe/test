#!/usr/bin/env python3
"""
Validates data/ingredients.json against profiles/category-profiles.json requirements
and checks that output/en/ contains valid, well-formed JSON-LD.

Checks performed:
  1. Organization trust signals (knowsAbout, patent-holder status)
  2. Per-category required fields present and non-empty
  3. Per-category evidence-phrasing rules:
       - forbidden overclaiming phrases must NOT appear
       - required hedging/framing phrases must appear (any-of, and all-of where declared)
  4. Each declared keyword has relevance evidence, and that evidence text actually
     appears in the ingredient's own descriptive content (not just the keywords list)
  5. output/en/*.html contains parseable JSON-LD with required schema.org fields

Usage:
    python3 validate.py
Exits with code 1 if any error is found.
"""
import json
import sys
from pathlib import Path

BASE = Path(__file__).parent
DATA_FILE = BASE / "data" / "ingredients.json"
PROFILE_FILE = BASE / "profiles" / "category-profiles.json"
OUTPUT_DIR = BASE / "output" / "en"


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def get_path(obj, path):
    cur = obj
    for part in path.split("."):
        if isinstance(cur, dict):
            cur = cur.get(part)
        elif isinstance(cur, list):
            cur = cur[int(part)] if part.isdigit() and int(part) < len(cur) else None
        else:
            return None
    return cur


def is_empty(value):
    return value is None or value == "" or value == [] or value == {}


def check_required_fields(ingredient, profile, errors):
    for field in profile.get("requiredFields", []):
        path = profile.get("fieldPaths", {}).get(field, field)
        value = get_path(ingredient, path)
        if is_empty(value):
            errors.append(
                f"[{ingredient['id']}] Missing required field: '{field}' (path: {path}) "
                f"-> add this value in data/ingredients.json to satisfy "
                f"profiles/category-profiles.json categories.{ingredient['category']}.requiredFields."
            )


def build_corpus(ingredient):
    """Concatenate every text value on the ingredient except 'keywords' into one search corpus."""
    parts = []

    def walk(obj, key=None):
        if key == "keywords":
            return
        if isinstance(obj, dict):
            for k, v in obj.items():
                walk(v, k)
        elif isinstance(obj, list):
            for v in obj:
                walk(v, key)
        elif isinstance(obj, str):
            parts.append(obj)

    walk(ingredient)
    return " ".join(parts).lower()


def check_keyword_relevance(ingredient, profile, warnings):
    corpus = build_corpus(ingredient)
    evidence_map = profile.get("keywordEvidence", {})
    for kw in ingredient.get("keywords", []):
        ev = evidence_map.get(kw)
        if not ev:
            warnings.append(
                f"[{ingredient['id']}] keyword '{kw}' has no relevance evidence (keywordEvidence) defined in the profile. "
                f"This risks looking like unrelated keyword stuffing — add evidence in profiles/category-profiles.json."
            )
            continue
        must_contain = ev.get("mustContainAny", [])
        if must_contain and not any(term.lower() in corpus for term in must_contain):
            warnings.append(
                f"[{ingredient['id']}] keyword '{kw}' evidence terms {must_contain} were not found in the ingredient's "
                f"own descriptive content. This keyword may be unrelated to the actual page content — "
                f"update data/ingredients.json or reconsider the keyword."
            )


def check_evidence_phrasing(ingredient, profile, errors):
    rules = profile.get("evidencePhrasingRules", {})
    text = json.dumps(ingredient.get("clinicalEvidence", {}), ensure_ascii=False).lower()
    for phrase in rules.get("forbiddenPhrases", []):
        if phrase.lower() in text:
            errors.append(
                f"[{ingredient['id']}] clinicalEvidence contains a forbidden overclaiming phrase: '{phrase}'"
            )
    required_any = rules.get("requiredPhrasesAny", [])
    if required_any and not any(p.lower() in text for p in required_any):
        errors.append(
            f"[{ingredient['id']}] clinicalEvidence must contain at least one of: {required_any}"
        )
    required_all = rules.get("requiredPhrasesAll", [])
    missing_all = [p for p in required_all if p.lower() not in text]
    if missing_all:
        errors.append(
            f"[{ingredient['id']}] clinicalEvidence is missing required reference(s): {missing_all} "
            f"(all of {required_all} must be documented)"
        )


def check_organization(org, meta, errors, warnings):
    if is_empty(org.get("knowsAbout")):
        errors.append("[organization] knowsAbout is empty (must state Enzyme Engineering / Glycosylation)")
    else:
        for term in meta.get("orgRequiredKnowsAbout", []):
            if term not in org["knowsAbout"]:
                errors.append(f"[organization] knowsAbout is missing required item: '{term}'")
    if not org.get("patents", {}).get("hasPatents"):
        warnings.append("[organization] patent-holder trust signal (patents.hasPatents=true) is not set.")


def validate_output_files(errors):
    if not OUTPUT_DIR.exists():
        errors.append(f"[output] {OUTPUT_DIR} does not exist. Run generate.py first.")
        return
    html_files = list(OUTPUT_DIR.glob("*.html"))
    if not html_files:
        errors.append(f"[output] No .html files found in {OUTPUT_DIR}. Run generate.py first.")
        return
    for f in html_files:
        text = f.read_text(encoding="utf-8")
        if '<script type="application/ld+json">' not in text:
            errors.append(f"[output] {f.name}: missing <script type=\"application/ld+json\"> tag.")
            continue
        json_str = text.split('<script type="application/ld+json">', 1)[-1].rsplit("</script>", 1)[0]
        try:
            parsed = json.loads(json_str)
        except json.JSONDecodeError as e:
            errors.append(f"[output] {f.name}: failed to parse JSON-LD - {e}")
            continue
        nodes = parsed.get("@graph", [parsed]) if isinstance(parsed, dict) else []
        for node in nodes:
            if "@type" not in node:
                errors.append(f"[output] {f.name}: node is missing '@type'.")


def main():
    data = load_json(DATA_FILE)
    profiles = load_json(PROFILE_FILE)
    org = data["organization"]
    ingredients = data["ingredients"]
    meta = profiles.get("meta", {})

    errors = []
    warnings = []

    check_organization(org, meta, errors, warnings)

    for ingredient in ingredients:
        cat_id = ingredient.get("category")
        profile = profiles.get("categories", {}).get(cat_id)
        if not profile:
            errors.append(f"[{ingredient.get('id')}] Unknown category '{cat_id}' (not defined in profiles.categories)")
            continue
        check_required_fields(ingredient, profile, errors)
        check_keyword_relevance(ingredient, profile, warnings)
        check_evidence_phrasing(ingredient, profile, errors)

    validate_output_files(errors)

    print("=" * 70)
    print(f"Validation result: {len(errors)} error(s) / {len(warnings)} warning(s)")
    print("=" * 70)
    for e in errors:
        print(f"[ERROR] {e}")
    for w in warnings:
        print(f"[WARNING] {w}")
    if not errors and not warnings:
        print("All checks passed.")

    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
