#!/usr/bin/env python3
"""
data/ingredients.json + profiles/category-profiles.json + templates/*.json 을 읽어
페이지별(Organization / Product / FAQPage) JSON-LD를 생성하고,
output/kr/ 아래에 <script type="application/ld+json"> 로 감싼 .html 파일로 저장한다.

사용법:
    python3 generate.py

ingredients.json만 수정하고 이 스크립트를 다시 실행하면 output/kr/ 전체가 재생성된다.
"""
import html
import json
import re
from pathlib import Path

BASE = Path(__file__).parent
DATA_FILE = BASE / "data" / "ingredients.json"
PROFILE_FILE = BASE / "profiles" / "category-profiles.json"
TEMPLATE_DIR = BASE / "templates"
OUTPUT_DIR = BASE / "output" / "kr"


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def get_path(obj, path):
    """'a.b.c' 형태의 점(dot) 경로로 중첩 dict 값을 조회. 'a.b|join(, )' 형태면 리스트를 join."""
    filt = None
    if "|" in path:
        path, filt = path.split("|", 1)
    cur = obj
    for part in path.split("."):
        if isinstance(cur, dict):
            cur = cur.get(part)
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
    """템플릿 JSON을 순회하며 값이 정확히 '$key' 문자열이면 context[key]로 치환한다."""
    if isinstance(node, dict):
        return {k: substitute(v, context) for k, v in node.items()}
    if isinstance(node, list):
        return [substitute(v, context) for v in node]
    if isinstance(node, str) and node.startswith("$") and node[1:] in context:
        return context[node[1:]]
    return node


def build_context(ingredient, org, profile):
    ctx = {}
    for key, path in profile.get("contextMap", {}).items():
        ctx[key] = get_path(ingredient, path)
    ctx["id"] = ingredient["id"]
    ctx["name"] = ingredient.get("name")
    ctx["org_name"] = org["name"]
    ctx["org_url"] = org["url"]
    ctx["org_knowsAbout_joined"] = ", ".join(org.get("knowsAbout", []))
    ctx["org_patent_note"] = org.get("patents", {}).get("note", "")
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


def build_meta_keywords_tag(ingredients):
    """이미 Product 스키마 keywords에 등록되고 validate.py로 관련성 검증을 마친 키워드만 그대로
    <meta name="keywords">에 반영한다. 새로운 단어를 여기서 추가하지 않는다(키워드 스터핑 방지)."""
    seen = []
    for ingredient in ingredients:
        for kw in ingredient.get("keywords", []):
            if kw not in seen:
                seen.append(kw)
    content = html.escape(", ".join(seen), quote=True)
    return f'<meta name="keywords" content="{content}">\n'


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

        product_jsonld = substitute(product_template, product_ctx)
        (OUTPUT_DIR / f"{ingredient['id']}-product.html").write_text(wrap_script(product_jsonld), encoding="utf-8")

        faq_items = build_faq_items(profile, ctx)
        faq_jsonld = substitute(faq_template, {"faqItems": faq_items})
        (OUTPUT_DIR / f"{ingredient['id']}-faq.html").write_text(wrap_script(faq_jsonld), encoding="utf-8")

        graph.append(strip_context(product_jsonld))
        graph.append(strip_context(faq_jsonld))
        generated.append(ingredient["id"])

    meta_keywords_tag = build_meta_keywords_tag(ingredients)
    (OUTPUT_DIR / "meta-tags.html").write_text(meta_keywords_tag, encoding="utf-8")

    combined = {"@context": "https://schema.org", "@graph": graph}
    (OUTPUT_DIR / "combined-header-code.html").write_text(
        meta_keywords_tag + wrap_script(combined), encoding="utf-8"
    )

    print(f"[generate] {len(generated)}개 원료({', '.join(generated)}) JSON-LD 생성 완료 -> {OUTPUT_DIR}")
    print("[generate] meta keywords는 Product.keywords와 동일한 값으로 자동 생성됩니다 (임의 추가 없음).")
    print("[generate] combined-header-code.html 에 meta keywords + Organization + 전체 원료 Product/FAQ(@graph)가 합쳐져 있습니다.")
    print("[generate] 아임웹 SEO > Header Code 필드에는 combined-header-code.html 내용을 그대로 붙여넣으면 됩니다.")


if __name__ == "__main__":
    main()
