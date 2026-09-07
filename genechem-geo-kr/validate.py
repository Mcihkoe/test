#!/usr/bin/env python3
"""
data/ingredients.json 이 profiles/category-profiles.json 의 요구사항을 만족하는지,
그리고 output/kr/ 의 생성 결과물이 유효한 JSON-LD인지 검증한다.

체크 항목:
  1. Organization 필수 신뢰 신호(knowsAbout, 특허 보유 여부)
  2. 카테고리별 필수 필드 존재 여부
  3. 카테고리별 임상/효능 표현 규칙(과장 표현 금지, 필수 표현 포함) 위반 여부
  4. keywords 필드의 각 키워드가 본문(성분 설명)과 실제 관련이 있는지
     (keywordEvidence에 정의된 근거 문구가 본문에 실제로 등장하는지 확인)
  5. output/kr/*.html 안의 JSON-LD가 파싱 가능한 유효 JSON인지
  6. <meta name="keywords"> 태그가 존재하고 Product.keywords와 정확히 일치하는지(누락/임의추가 없는지)

사용법:
    python3 validate.py
실패 시(오류 1건 이상) exit code 1 로 종료한다.
"""
import html
import json
import re
import sys
from pathlib import Path

BASE = Path(__file__).parent
DATA_FILE = BASE / "data" / "ingredients.json"
PROFILE_FILE = BASE / "profiles" / "category-profiles.json"
OUTPUT_DIR = BASE / "output" / "kr"


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def get_path(obj, path):
    cur = obj
    for part in path.split("."):
        if isinstance(cur, dict):
            cur = cur.get(part)
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
                f"[{ingredient['id']}] 필수 필드 누락: '{field}' (참조 경로: {path}) "
                f"-> profiles/category-profiles.json 의 categories.{ingredient['category']}.requiredFields 를 만족하려면 "
                f"data/ingredients.json 에 해당 값을 채워야 합니다."
            )


def build_corpus(ingredient):
    """keywords 필드를 제외한 모든 텍스트 값을 하나의 문자열로 합쳐 '본문'을 구성한다."""
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
    return " ".join(parts)


def check_keyword_relevance(ingredient, profile, warnings):
    corpus = build_corpus(ingredient)
    evidence_map = profile.get("keywordEvidence", {})
    for kw in ingredient.get("keywords", []):
        ev = evidence_map.get(kw)
        if not ev:
            warnings.append(
                f"[{ingredient['id']}] keyword '{kw}' 에 대한 관련성 근거(keywordEvidence)가 프로필에 정의되어 있지 않습니다. "
                f"본문과 무관한 키워드 스터핑일 위험이 있으니 profiles/category-profiles.json 에 근거를 등록하세요."
            )
            continue
        must_contain = ev.get("mustContainAny", [])
        if must_contain and not any(term in corpus for term in must_contain):
            warnings.append(
                f"[{ingredient['id']}] keyword '{kw}' 의 근거 문구 {must_contain} 가 성분 설명 본문에서 발견되지 않았습니다. "
                f"본문과 무관한 키워드일 수 있으니 data/ingredients.json 의 설명 필드를 보완하거나 키워드를 재검토하세요."
            )


def check_evidence_phrasing(ingredient, profile, errors):
    rules = profile.get("evidencePhrasingRules", {})
    text = json.dumps(ingredient.get("clinicalEvidence", {}), ensure_ascii=False)
    for phrase in rules.get("forbiddenPhrases", []):
        if phrase in text:
            errors.append(
                f"[{ingredient['id']}] clinicalEvidence에 금지된 과장/오해소지 표현이 포함되어 있습니다: '{phrase}'"
            )
    required_any = rules.get("requiredPhrasesAny", [])
    if required_any and not any(p in text for p in required_any):
        errors.append(
            f"[{ingredient['id']}] clinicalEvidence에 다음 표현 중 최소 하나가 포함되어야 합니다: {required_any}"
        )


def check_organization(org, meta, errors, warnings):
    if is_empty(org.get("knowsAbout")):
        errors.append("[organization] knowsAbout 필드가 비어있습니다 (효소공학/글리코실레이션 명시 필요)")
    else:
        for term in meta.get("orgRequiredKnowsAbout", []):
            if term not in org["knowsAbout"]:
                errors.append(f"[organization] knowsAbout에 필수 항목이 없습니다: '{term}'")
    if not org.get("patents", {}).get("hasPatents"):
        warnings.append("[organization] 특허 보유 신뢰 신호(patents.hasPatents=true)가 설정되어 있지 않습니다.")


def validate_output_files(errors):
    if not OUTPUT_DIR.exists():
        errors.append(f"[output] {OUTPUT_DIR} 가 존재하지 않습니다. generate.py를 먼저 실행하세요.")
        return
    html_files = list(OUTPUT_DIR.glob("*.html"))
    if not html_files:
        errors.append(f"[output] {OUTPUT_DIR} 에 생성된 .html 파일이 없습니다. generate.py를 먼저 실행하세요.")
        return
    for f in html_files:
        if f.name == "meta-tags.html":
            continue  # <meta> 전용 파일은 아래 check_meta_keywords()에서 별도 검증
        text = f.read_text(encoding="utf-8")
        if '<script type="application/ld+json">' not in text:
            errors.append(f"[output] {f.name}: <script type=\"application/ld+json\"> 태그가 없습니다.")
            continue
        json_str = text.split('<script type="application/ld+json">', 1)[-1].rsplit("</script>", 1)[0]
        try:
            parsed = json.loads(json_str)
        except json.JSONDecodeError as e:
            errors.append(f"[output] {f.name}: JSON-LD 파싱 실패 - {e}")
            continue
        nodes = parsed.get("@graph", [parsed]) if isinstance(parsed, dict) else []
        for node in nodes:
            if "@type" not in node:
                errors.append(f"[output] {f.name}: 노드에 '@type' 필드가 없습니다.")


def expected_meta_keywords(ingredients):
    seen = []
    for ingredient in ingredients:
        for kw in ingredient.get("keywords", []):
            if kw not in seen:
                seen.append(kw)
    return seen


def check_meta_keywords(ingredients, errors):
    """<meta name="keywords">가 존재하고, Product.keywords와 정확히 일치하는지(임의 추가/누락 없는지) 확인한다."""
    expected = expected_meta_keywords(ingredients)
    expected_content = ", ".join(expected)

    for fname in ("meta-tags.html", "combined-header-code.html"):
        f = OUTPUT_DIR / fname
        if not f.exists():
            errors.append(f"[output] {fname} 가 없습니다. generate.py를 먼저 실행하세요.")
            continue
        text = f.read_text(encoding="utf-8")
        m = re.search(r'<meta\s+name="keywords"\s+content="([^"]*)"', text)
        if not m:
            errors.append(f"[output] {fname} 에 <meta name=\"keywords\"> 태그가 없습니다.")
            continue
        actual_content = html.unescape(m.group(1))
        if actual_content != expected_content:
            errors.append(
                f"[output] {fname} 의 meta keywords가 data/ingredients.json의 keywords와 다릅니다.\n"
                f"         기대값: {expected_content}\n"
                f"         실제값: {actual_content}\n"
                f"         -> generate.py를 다시 실행해서 재생성하세요."
            )


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
            errors.append(f"[{ingredient.get('id')}] 알 수 없는 카테고리: '{cat_id}' (profiles.categories에 정의되지 않음)")
            continue
        check_required_fields(ingredient, profile, errors)
        check_keyword_relevance(ingredient, profile, warnings)
        check_evidence_phrasing(ingredient, profile, errors)

    validate_output_files(errors)
    check_meta_keywords(ingredients, errors)

    print("=" * 70)
    print(f"검증 결과: 오류 {len(errors)}건 / 경고 {len(warnings)}건")
    print("=" * 70)
    for e in errors:
        print(f"[ERROR] {e}")
    for w in warnings:
        print(f"[WARNING] {w}")
    if not errors and not warnings:
        print("모든 검증을 통과했습니다.")

    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
