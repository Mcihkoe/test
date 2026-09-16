# 자연어 질문 우선순위 TOP 20 (KR + EN)

## 중요한 전제

이 리스트는 **Claude/ChatGPT/Gemini/삼성 Galaxy AI의 실제 사용량 데이터(텔레메트리)가 아닙니다.**
각 회사의 내부 쿼리 통계는 외부(이 세션 포함)에서 접근할 수 없습니다 — 그런 데이터가 있는 것처럼
순위를 매기면 없는 근거를 지어내는 것이므로, 이 프로젝트 전체가 지켜온 "근거 없이 관련성 만들지
않기" 원칙에 위배됩니다.

대신 이 TOP 20은 다음 기준으로 리서치를 통해 선정한 **우선순위 자연어**입니다:
1. 실제 검색엔진(구글) 결과에서 확인된 소비자/B2B 자연어 표현 (2026-09 조사)
2. 진켐 원료(AquaGG, 3'-SL, 6'-SL)의 실제 근거 데이터와 매칭되는 질문만 선정
3. 근거 없는 카테고리(관절 직접 클레임, 수면/편안함)는 제외 — 별도 조사 문서 참고

## 참고: 워드프레스 관련

진켐 사이트는 워드프레스가 아니라 **아임웹**으로 운영됩니다. "자연어 질문을 넣어야 상위 노출된다"는
조언은 워드프레스의 SEO 플러그인(Yoast 등)을 예로 든 일반론이고, 아임웹에서의 동일한 역할은
이미 진행 중인 **Header Code 필드의 FAQPage 스키마**가 담당합니다 — 별도로 CMS를 옮기거나
새로 설정할 것은 없습니다.

## 상태 표기
- **반영됨**: `profiles/category-profiles.json`의 FAQPage에 이미 있고, Header Code에 배포된 질문
- **신규 제안**: 검색 조사에서 나온 변형 표현이지만 아직 FAQ 파이프라인에 넣지 않은 것 — 근거는 있으나 실제 반영 여부는 확인 필요

---

## KR — genechem.imweb.me (AquaGG)

| # | 자연어 질문 | 상태 | 근거 |
|---|---|---|---|
| 1 | 세안 후 피부가 자꾸 당겨요. 어떤 보습 원료가 도움이 될까요? | 반영됨 | "피부 속당김" 실제 검색 조사 |
| 2 | 속당김 없이 촉촉함이 오래가는 원료가 있나요? | 반영됨 | 동일 |
| 3 | 매일 쓰기 좋은 고보습 원료를 찾고 있는데 추천해주실 수 있나요? | 반영됨 | "속보습 로션" 검색 패턴 |
| 4 | 국내에서 보습 기능성 화장품 원료를 공급하는 회사가 있나요? | 반영됨 | B2B/OEM 자연어 조사 |
| 5 | 화장품 OEM/ODM 진행 시 배합할 기능성 원료는 어디서 구할 수 있나요? | 반영됨 | 동일 |
| 6 | 피부 당김 없이 하루종일 촉촉하게 유지하려면 어떤 성분을 써야 하나요? | 신규 제안 | 1·2번의 변형 표현 — 커버리지 보강용 |
| 7 | 일반 보습 성분(글리세린/히알루론산)과 다른 신개념 보습 원료가 있나요? | 반영됨 (기존) | vs-conventional FAQ |
| 8 | 부활초에서 유래한 화장품 성분이 진짜 효과 있나요? | 반영됨 (기존) | origin-story FAQ |
| 9 | 피부 탄력 개선에 도움되는 원료 뭐가 있어요? | 반영됨 (기존) | elasticity-benefit FAQ |
| 10 | 피부 장벽 강화에 좋은 원료 추천해주세요 | 반영됨 (기존) | skin-barrier-benefit FAQ |

## EN — genechem.co.kr (3'-SL / 6'-SL / AquaGG)

| # | Natural-language question | Status | Basis |
|---|---|---|---|
| 11 | What ingredient can help with muscle recovery after exercise? | Live | 6'-SL, POSTECH study |
| 12 | Is there an ingredient that helps counter muscle loss as people age? | Live | 6'-SL, GNE myopathy trial (rare-disease framing kept) |
| 13 | What's a newer ingredient for strength and muscle support in sports nutrition products? | Live | 6'-SL |
| 14 | Where can I source 6'-sialyllactose for a sports nutrition product? | Live | 6'-SL, Sejong City facility |
| 15 | Is there a company that manufactures 3'-sialyllactose at commercial scale? | Live | 3'-SL, Sejong City facility |
| 16 | What ingredient helps with skin that feels tight and dehydrated? | Live | AquaGG, AQP3 mechanism |
| 17 | What's a good high-purity hydration ingredient for daily skincare formulations? | Live | AquaGG specs |
| 18 | What ingredient is backed by real clinical research for muscle health, not just marketing claims? | Proposed — not yet added | Restates 6'-SL's GNE myopathy + POSTECH evidence; must keep rare-disease disclaimer intact |
| 19 | Is there a gut health ingredient derived from breast milk sugars (HMOs)? | Proposed — not yet added | Restates 3'-SL's HMO mechanism; must stay hedged (no clinical data) |
| 20 | What's a novel HMO ingredient that supplement brands are starting to use? | Proposed — not yet added | General 3'-SL/6'-SL framing, B2B-facing |

## 다음 단계

- #6, #18, #19, #20은 근거 데이터는 이미 있지만 실제 `category-profiles.json` FAQPage에는
  아직 추가하지 않았습니다. 추가를 원하시면 이전과 동일한 방식(기존 검증된 사실만 재사용,
  `generate.py` → `validate.py` 재실행)으로 반영할 수 있습니다.
- 이 리스트는 실측 데이터가 아니므로, 실제 효과는 배포 후 Rich Results Test / 실검색 테스트로
  검증해야 합니다.
