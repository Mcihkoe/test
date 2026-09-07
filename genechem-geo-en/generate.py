#!/usr/bin/env python3
"""
Reads data/ingredients.json + profiles/category-profiles.json + templates/*.json
and generates per-page JSON-LD (Organization / Product / FAQPage), writing each as
a <script type="application/ld+json"> snippet under output/en/.

Usage:
    python3 generate.py

Editing ingredients.json and re-running this script regenerates all of output/en/.
"""
import json
import re
from pathlib import Path

BASE = Path(__file__).parent
DATA_FILE = BASE / "data" / "ingredients.json"
PROFILE_FILE = BASE / "profiles" / "category-profiles.json"
TEMPLATE_DIR = BASE / "templates"
OUTPUT_DIR = BASE / "output" / "en"


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def get_path(obj, path):
    """Dotted-path getter, e.g. 'a.b.0.c'. Supports a trailing '|join(sep)' filter on a list result."""
    filt = None
    if "|" in path:
        path, filt = path.split("|", 1)
    cur = obj
    for part in path.split("."):
        if isinstance(cur, dict):
            cur = cur.get(part)
        elif isinstance(cur, list):
            cur = cur[int(part)] if part.isdigit() and int(part) < len(cur) else None
        else:
            return None
        if cur is None:
            return None
    if filt:
        m = re.match(r"join\((.*)\)", filt)
        if m and isinstance(cur, list):
            cur = m.group(1).join(str(x) for x in cur)
    return cur


def substitute(node, context):
    """Walk template JSON; a string value that is exactly '$key' is replaced with context[key]."""
    if isinstance(node, dict):
        return {k: substitute(v, context) for k, v in node.items()}
    if isinstance(node, list):
        return [substitute(v, context) for v in node]
    if isinstance(node, str) and node.startswith("$") and node[1:] in context:
        return context[node[1:]]
    return node


def is_empty(value):
    return value is None or value == "" or value == [] or value == {}


def prune_empty(node):
    """Drop dict keys whose resolved value is empty/None (e.g. alternateName absent for non-INCI ingredients)."""
    if isinstance(node, dict):
        return {k: prune_empty(v) for k, v in node.items() if not is_empty(v)}
    if isinstance(node, list):
        return [prune_empty(v) for v in node]
    return node


def build_context(ingredient, org, profile):
    ctx = {}
    for key, path in profile.get("contextMap", {}).items():
        ctx[key] = get_path(ingredient, path)
    ctx["id"] = ingredient["id"]
    ctx["name"] = ingredient.get("name")
    ctx["org_name"] = org["name"]
    ctx["org_url"] = org["url"]
    return ctx


def build_additional_properties(ingredient, profile):
    props = []
    for field in profile.get("additionalPropertyFields", []):
        value = get_path(ingredient, field["path"])
        if value is None:
            continue
        if isinstance(value, list):
            value = ", ".join(str(v) for v in value)
        props.append({"@type": "PropertyValue", "name": field["label"], "value": str(value)})
    return props


class _SafeDict(dict):
    def __missing__(self, key):
        return "{" + key + "}"


def render_text(template_str, ctx):
    return template_str.format_map(_SafeDict(ctx))


def build_faq_items(profile, ctx):
    items = []
    for pattern in profile.get("faqPatterns", []):
        items.append({
            "@type": "Question",
            "name": pattern["question"],
            "acceptedAnswer": {"@type": "Answer", "text": render_text(pattern["answerTemplate"], ctx)},
        })
    return items


def wrap_script(data):
    body = json.dumps(data, ensure_ascii=False, indent=2)
    return f'<script type="application/ld+json">\n{body}\n</script>\n'


def strip_context(node):
    return {k: v for k, v in node.items() if k != "@context"}


def main():
    data = load_json(DATA_FILE)
    profiles = load_json(PROFILE_FILE)
    org = data["organization"]
    ingredients = data["ingredients"]

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    org_template = load_json(TEMPLATE_DIR / "organization.template.json")
    product_template = load_json(TEMPLATE_DIR / "product.template.json")
    faq_template = load_json(TEMPLATE_DIR / "faqpage.template.json")

    org_additional_property = []
    if org.get("patents", {}).get("hasPatents"):
        org_additional_property.append(
            {"@type": "PropertyValue", "name": "Patents", "value": org["patents"].get("note", "")}
        )

    org_ctx = {
        "org_name": org["name"],
        "org_alternateName": org.get("alternateName", ""),
        "org_url": org["url"],
        "org_description": org.get("description", ""),
        "org_knowsAbout": org.get("knowsAbout", []),
        "org_additionalProperty": org_additional_property,
    }
    org_jsonld = substitute(org_template, org_ctx)
    (OUTPUT_DIR / "organization.html").write_text(wrap_script(org_jsonld), encoding="utf-8")

    graph = [strip_context(org_jsonld)]
    generated = []

    for ingredient in ingredients:
        cat_id = ingredient["category"]
        profile = profiles["categories"][cat_id]
        ctx = build_context(ingredient, org, profile)

        product_ctx = dict(ctx)
        product_ctx["productCategory"] = profile.get("label", "")
        product_ctx["description"] = render_text(profile.get("descriptionTemplate", "{name}"), ctx)
        product_ctx["audienceType"] = profile.get("audienceType", "B2B")
        product_ctx["additionalProperty"] = build_additional_properties(ingredient, profile)
        product_ctx["keywords"] = ingredient.get("keywords", profile.get("keywords", []))
        product_ctx["altName"] = ingredient.get("inciName")

        product_jsonld = prune_empty(substitute(product_template, product_ctx))
        (OUTPUT_DIR / f"{ingredient['id']}-product.html").write_text(wrap_script(product_jsonld), encoding="utf-8")

        faq_items = build_faq_items(profile, ctx)
        faq_jsonld = substitute(faq_template, {"faqItems": faq_items})
        (OUTPUT_DIR / f"{ingredient['id']}-faq.html").write_text(wrap_script(faq_jsonld), encoding="utf-8")

        graph.append(strip_context(product_jsonld))
        graph.append(strip_context(faq_jsonld))
        generated.append(ingredient["id"])

    combined = {"@context": "https://schema.org", "@graph": graph}
    (OUTPUT_DIR / "combined-header-code.html").write_text(wrap_script(combined), encoding="utf-8")

    print(f"[generate] Generated JSON-LD for {len(generated)} ingredient(s): {', '.join(generated)} -> {OUTPUT_DIR}")
    print("[generate] combined-header-code.html contains Organization + all ingredient Product/FAQ nodes in one @graph.")
    print("[generate] Paste the contents of combined-header-code.html into the site's SEO > Header Code field.")


if __name__ == "__main__":
    main()
