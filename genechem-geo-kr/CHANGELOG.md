# CHANGELOG — genechem-geo-kr

이 문서는 국문 사이트(https://genechem.imweb.me/) GEO/AEO 구조화 데이터의 월별 변경 이력을 기록합니다.
매달 `data/ingredients.json`을 갱신하고 `python3 generate.py && python3 validate.py`를 실행한 뒤,
`output/kr/combined-header-code.html`을 아임웹 SEO > Header Code에 재배포합니다.

## 2026-09 갱신 (2): meta keywords 태그 추가

- `<meta name="keywords">` 태그가 국문 페이지 Header Code에 빠져 있던 문제 보완
- `generate.py`가 Product.keywords(이미 관련성 검증을 마친 9개 키워드)를 그대로 재사용해 `output/kr/meta-tags.html`과 `combined-header-code.html` 상단에 자동 삽입
- `validate.py`에 meta keywords ↔ ingredients.json keywords 일치 여부 검증 추가 (임의 추가/누락 방지)

## 2026-09 갱신: AquaGG 초안 데이터 반영

- 폴더 구조 및 생성/검증 파이프라인 최초 구축 (`data/`, `profiles/`, `templates/`, `generate.py`, `validate.py`)
- `data/ingredients.json`: 카테고리 C(AquaGG) 데이터 초안 작성
  - INCI명, AQP3 활성화 기전, 순도/수용성/pH 안정성, 부활초 유래 스토리, 국내 사업 범위, 임상 근거 요약 반영
- `profiles/category-profiles.json`: 카테고리 C 필수 필드, FAQ 5종 패턴, keywords 9종 및 관련성 근거(keywordEvidence), 표현 규칙(과장 금지 문구) 정의
- `templates/`: Organization, Product(원료), FAQPage JSON-LD 템플릿 작성
- `output/kr/`: `generate.py` 최초 실행 결과 생성 (organization.html, aquagg-product.html, aquagg-faq.html, combined-header-code.html)
- 비고(TODO): 임상 세부 수치(연구기관명, 발표 연도, 구체 수치), 특허번호는 자료 확보 시 다음 갱신에 추가 예정
