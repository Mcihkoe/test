# CHANGELOG — genechem-geo-kr

## 2026-09 갱신 (7): 소비자 자연어 FAQ 5종 추가 (속당김/속보습, OEM 문의)

- 배경: "AQP3 활성화" 같은 전문 용어는 이미 검색에 잘 걸리지만, 일반 소비자/기업 담당자는
  그런 용어로 검색하지 않는다는 점을 실제 검색 조사로 확인 — "피부 속당김", "속보습 성분",
  "화장품 원료 OEM/ODM 업체" 같은 표현이 실제 소비자/B2B 자연어임을 확인
- `categories.C.faqPatterns`에 5개 추가:
  - 보습 클러스터(자연어): 속당김 완화, 속보습 지속력, 데일리 고보습 원료 질문 3종
  - 사업/공급 클러스터(자연어): 국내 보습 원료 공급사, OEM/ODM 배합 원료 질문 2종
- 모든 신규 FAQ는 기존 mechanism/specs/businessScope 등 이미 검증된 값만 재사용 —
  새로운 효능이나 수치를 추가하지 않음
- 조사 결과 "관절"(사이알릴락토스 계열 원료가 실제 소비자 콘텐츠에 전혀 등장하지 않음)과
  "수면/편안함"(진켐 원료 중 근거 있는 것이 전혀 없음) 카테고리는 자연어 확장 대상에서
  의도적으로 제외 — 근거 없이 관련성을 만들지 않는다는 이 프로젝트의 원칙에 따름

## 2026-09 갱신 (6): 오프페이지 노출 대응 — 원료 디렉토리/미디어 아웃리치 문구 초안 추가

- 배경: "AQP3 활성화 화장품 원료 공급 회사"처럼 브랜드명이 없는 실제 검색 질의를
  구글/Gemini에서 테스트한 결과, `site:genechem.co.kr`/`site:genechem.imweb.me`로는
  콘텐츠가 정확히 색인·요약되는 것이 확인됐으나(즉 JSON-LD/스키마 자체는 정상 작동),
  브랜드명 없는 일반 질의에서는 진켐이 전혀 노출되지 않고 원료 디렉토리형 사이트
  (대한화장품협회 성분사전, ezcos.co.kr, chemknock.co.kr, 하나케어)와 뷰티 매체
  (닥터오라클 등)만 노출됨을 확인
- 판단: 이는 온페이지 스키마 품질 문제가 아니라 오프페이지(제3자 등재/백링크) 부족
  문제 — 이 시스템(JSON-LD 생성 파이프라인)의 범위를 벗어나지만, 실제 노출 개선에
  필요한 다음 단계이므로 별도 산출물로 기록
- `outreach/directory-listings.md` 신설: 검색 시 상위 노출이 확인된 디렉토리
  사이트 등재용 회사소개/원료소개 문구 초안 (짧은 버전/긴 버전)
- `outreach/media-pitch.md` 신설: 뷰티 전문 매체 대상 보도자료 및 피칭 이메일 초안
- 두 문서 모두 `data/ingredients.json`에 이미 존재하는 검증된 사실만 재사용 —
  임상 수치, 특허번호 등 미확보 정보는 대괄호로 명시하고 절대 임의로 채우지 않음

이 문서는 국문 사이트(https://genechem.imweb.me/) GEO/AEO 구조화 데이터의 월별 변경 이력을 기록합니다.
매달 `data/ingredients.json`을 갱신하고 `python3 generate.py && python3 validate.py`를 실행한 뒤,
`output/kr/combined-header-code.html`을 아임웹 SEO > Header Code에 재배포합니다.

## 2026-09 갱신 (5): 사이트 전체 meta description을 회사 소개로 정정, 원료별 페이지 전용 description 분리

- 문제: 사이트 전체 Header Code(모든 페이지의 <head>에 삽입됨)에 "AquaGG는 ~" 식 제품 한정 설명을 넣었던 것은
  오류였음 — 진켐은 AquaGG만 있는 회사가 아니고(3'-SL/6'-SL은 영문 사이트 전용), 홈/회사소개 등
  다른 페이지에도 이 설명이 그대로 노출되어 실제 페이지 내용과 어긋남
- 판단 기준: Google은 페이지 내용과 어긋나는 meta description을 무시/재생성하며, meta description은
  랭킹 신호가 아니라 스니펫/CTR에만 영향을 준다 — 즉 "회사 전체" 쿼리에는 회사 소개가, "AquaGG" 쿼리에는
  제품 소개가 매칭되어야 함
- `profiles/category-profiles.json`:
  - `meta.siteMetaDescription` → 회사(진켐/GeneChem) 소개 문구로 교체 (87자)
  - `meta.productPageMetaDescriptions.aquagg` 신설 → 기존 제품 설명 문구를 여기로 이동
- `generate.py`가 원료별로 `{id}-meta-description.html`을 별도 생성 — 이건 Header Code가 아니라
  아임웹의 "페이지별 SEO 설정"(AquaGG 페이지 자체)에 직접 붙여넣는 용도
- `validate.py`에 (1) siteMetaDescription이 회사명을 포함하는지, (2) 원료별 페이지 설명이 각각
  정의되어 있는지 검증 추가

## 2026-09 갱신 (4): meta description 태그 추가

- 실제 사이트에 `<meta name="description">`도 비어 있던 것을 확인 → 추가
- `profiles/category-profiles.json`의 `meta.siteMetaDescription`에 검색결과 스니펫용 문구(97자, 155자 권장 길이 이내)를 직접 관리
- `generate.py`가 이 문구를 `output/kr/meta-tags.html`, `combined-header-code.html` 상단(description → keywords 순)에 자동 삽입
- `validate.py`에 meta description 존재 여부, 길이(155자 초과 시 경고), 실제 출력물과의 일치 여부 검증 추가

## 2026-09 갱신 (3): 키워드 클러스터별 FAQ 대폭 확장

- 실제 AI 채팅창 검색 테스트 결과 "관련 정보가 안 뜬다"는 피드백에 대응
  (단, "모든 질문 방식에서 항상 상단 노출"은 스키마/코드로 보장 가능한 목표가 아님을 별도 안내함 —
  실시간 검색형 AI는 검색엔진 색인/권위 싸움, 정적 학습형 AI는 학습 데이터 자체를 바꿀 수 없기 때문)
- 코드/스키마 범위 내에서 할 수 있는 것: 같은 사실을 다양한 실제 검색 문구로 커버하는 FAQ 확장
- `category-profiles.json`의 FAQ를 5개 → 23개로 확장, 키워드 클러스터별로 구성
  (보습 / 부활초·브랜드 / 메커니즘 / 피부장벽 / 탄력 / 제형 / 신뢰·근거 / 사업·공급)
- 모든 신규 FAQ는 기존에 확보된 사실(mechanism, specs, originStory, businessScope,
  clinicalEvidence, 조직 knowsAbout/특허)만 재사용 — 새로운 임상 수치나 효능을 지어내지 않음
- 근거가 불충분한 질문(예: 손상된 피부 장벽에 대한 효과)은 명확히 헤징 처리
- Product.keywords에 "글리세릴글루코사이드", "제형 안정성" 2개 추가 (모두 실제 본문 근거 있음, keywordEvidence 등록)
- Organization의 knowsAbout/특허 정보를 FAQ 컨텍스트에서 참조할 수 있도록 generate.py의
  build_context()에 org_knowsAbout_joined, org_patent_note 필드 추가

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
