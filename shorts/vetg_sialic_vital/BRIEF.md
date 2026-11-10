# VetG Sialic Vital — 25초 브랜드 광고 제작 패키지

- 규격: **16:9 · 1920×1080 · 30fps · 25.0초** (요청서의 "세로형"과 "16:9"가 충돌해 16:9로 맞춤. 세로 9:16이 필요하면 각 프롬프트의 `aspect_ratio`만 바꾸면 됨)
- 톤: 실사, 자연광, 부드러운 카메라 움직임, 절제된 컷 편집. 브랜드 컬러 `#2e516e`, 배경 컬러 `#fcf8f5`
- 생성 모델(권장): Higgsfield **Seedance 2.5**를 `omni_reference` 모드, 1080p로 사용. 장면마다 5초로 만든 뒤 `assemble.sh`가 필요한 길이만큼 잘라 씀
- 상태: Higgsfield 계정이 **크레딧 0 (무료 플랜)** 이라 영상은 아직 생성하지 않음. 크레딧을 충전하면 아래 순서대로 바로 생성할 수 있음

## 폴더 구성

| 경로 | 내용 |
|---|---|
| `assets/` | 제품 3종과 로고 원본, 브랜드 컬러로 바꾼 로고(`vetg_logo_brand.png`) |
| `endcard/endcard_overlay.png` | 21초부터 실사 위에 얹는 투명 엔딩 오버레이(로고, 제품명, 메인 카피, 제품 3종) |
| `endcard/endcard_full.png` | 크림 배경 엔딩 미리보기 |
| `endcard/endcard.html`, `render.js` | 엔딩 원본. 문구를 고친 뒤 `node endcard/render.js`로 다시 그림 |
| `subtitles.ass` / `.srt` | 자막(Pretendard). `.ass`는 합본용, `.srt`는 다른 편집툴용 |
| `assemble.sh` | `clips/s01~s07.mp4`와 `audio/`를 받아 최종 MP4를 만드는 스크립트 |
| `fonts/` | Pretendard (SIL OFL 1.1) |

---

## 0단계. 일관성 고정용 기준 이미지 만들기 (먼저 1회)

장면마다 같은 개와 같은 보호자가 나오게 하려고, 영상보다 **기준 이미지 2장**을 먼저 만들고 모든 장면에 `image_references`로 넣는다.

> ⚠ 첨부된 개 사진은 **러프 콜리**(갈색·흰색 장모종)라서 요청한 "흑백 보더콜리"와 다른 견종이다. 기준 이미지로 쓰지 말 것.

**REF-DOG**: 개 기준 이미지. `generate_image`, 3:2 비율
```
Photoreal reference photo of one adult black-and-white Border Collie, medium-length double coat,
glossy black body, white chest bib, white collar ring, white blaze running down the center of the face
from forehead to muzzle, white front paws, black ears with semi-erect tipped shape, warm brown eyes,
natural healthy proportions. Three views side by side on a plain warm cream (#fcf8f5) studio backdrop:
front, three-quarter, side profile. Soft natural window light, true-to-life fur texture,
no collar tag text, no props.
```

**REF-GUARDIAN**: 보호자 기준 이미지. `generate_image`, 3:2 비율
```
Photoreal reference photo of one Korean woman in her late 30s, shoulder-length dark brown hair loosely tied,
natural makeup, warm gentle expression. Wardrobe: oatmeal knit cardigan over white tee, light beige trousers.
Three views (front, three-quarter, side) on a plain warm cream (#fcf8f5) backdrop, soft natural light,
unretouched skin texture, relaxed natural hands with five fingers.
```
- 계절별 옷만 바꾼다: 가을 카멜 코트, 봄 오트밀 카디건, 여름 흰 리넨 셔츠, 겨울 아이보리 니트. 얼굴과 헤어는 그대로 유지.

**제품 레퍼런스**: `assets/muscle_care.png`, `joint_care.png`, `mind_care.png`

---

## 1단계. 장면별 영상 프롬프트

모든 장면에 공통으로 붙이는 **스타일 꼬리말**과 **네거티브**:
```
STYLE: photoreal live-action commercial, shot on cinema camera, 35mm/50mm lens, shallow depth of field,
natural daylight, true-to-life fur and fabric texture, gentle stabilized camera move, warm premium family mood,
calm restrained pacing, no on-screen text.
AVOID: animation, cartoon, frozen/still subject, exaggerated facial expression, unnatural joints,
extra legs or paws, extra fingers, breed/face/coat-marking change between shots, warped product, warped logo,
any generated letters or subtitles.
```

| # | 시간 | 길이(잘라 쓸 길이) | 레퍼런스 |
|---|---|---|---|
| s01 | 0–3초 | 3초 | REF-DOG, REF-GUARDIAN |
| s02 | 3–6초 | 3초 | REF-DOG, REF-GUARDIAN |
| s03 | 6–10초 | 4초 | REF-DOG, REF-GUARDIAN, muscle_care |
| s04 | 10–14초 | 4초 | REF-DOG, REF-GUARDIAN, joint_care |
| s05 | 14–18초 | 4초 | REF-DOG, REF-GUARDIAN, mind_care |
| s06 | 18–21초 | 3초 | REF-DOG, REF-GUARDIAN, 제품 3종 |
| s07 | 21–25초 | 4초 | REF-DOG, REF-GUARDIAN |

### s01 · 가을 훅 (0–3초)
```
Autumn park path carpeted with fallen orange and yellow leaves, late-afternoon golden side light.
Medium-wide tracking shot from behind and slightly low: the black-and-white Border Collie from the reference
walks a few steps ahead on a loose leash, then gradually slows, stops and turns its head back toward its guardian.
The guardian (camel coat) also stops, then gently bends her knees and lowers herself to the dog's eye level.
Leaves rustle and drift; real paw placement and weight shift; subtle breeze in the fur.
Keep the lower third of the frame calm for subtitles.
```
### s02 · 교감 (3–6초)
```
Same autumn path, same light. Close-up at dog eye level: the guardian's hand slowly strokes the dog's shoulder;
the Border Collie lifts its head, meets her eyes and leans its cheek lightly into her palm.
Soft blink, natural breathing, warm backlight rim on the fur. Slow push-in, very gentle.
```
### s03 · 봄 · Muscle Care (6–10초)
```
Spring garden in bloom (tulips, cherry blossom petals), bright soft morning light.
0–2.5s: side tracking shot at knee height, the Border Collie trots relaxed beside the guardian (oatmeal cardigan),
realistic gait, visible weight transfer, ears and coat bouncing naturally.
2.5–4s: cut to a close-up of the blue-labeled MUSCLE CARE dropper bottle and its box (exactly as the reference image)
standing on a wooden garden table, petals and blurred garden behind, slow lateral slide.
```
### s04 · 여름 · Joint Care (10–14초)
```
Summer, dappled shade under a large leafy tree on a lawn, warm high sun with soft leaf shadows.
0–2.5s: the Border Collie, lying in the shade, rises up slowly and comfortably, stretches briefly,
and follows the guardian (white linen shirt) a few unhurried steps. Natural joint movement, no limping, no jumping.
2.5–4s: close-up of the purple-labeled JOINT CARE bottle and box (exactly as reference) on a linen picnic cloth
in the shade, leaf shadows gently moving across.
```
### s05 · 겨울 · Mind Care (14–18초)
```
Warm cozy living room, large window showing a snow-covered garden, soft diffused winter daylight plus warm lamp glow.
0–2.5s: the guardian (ivory knit) sits on the floor rug and makes a small inviting hand gesture; the Border Collie
turns its head toward her, walks over and touches her open hand with its nose. Attentive, calm eyes.
2.5–4s: close-up of the green-labeled MIND CARE bottle and box (exactly as reference) on a wooden side table
by the window, snow softly out of focus behind.
```
### s06 · 매일의 돌봄 (18–21초)
```
Bright morning kitchen in warm cream tones (#fcf8f5), soft window light.
The guardian places the dog's breakfast bowl on a low wooden mat, then sets the three VetG Sialic Vital boxes
(blue, purple, green, exactly as reference) neatly beside the bowl. The Border Collie sits waiting beside her,
tail sweeping gently on the floor. No pouring, no dosing, no measuring shown. Medium shot, slow dolly-in.
```
### s07 · 브랜드 엔딩 배경 (21–25초)
```
Warm cream-colored (#fcf8f5) minimal living space, soft natural light. Static, locked-off medium shot,
subject placed on the RIGHT half of the frame: the guardian sits on a cream sofa, the Border Collie rests its head
on her lap, relaxed; she slowly strokes its head. Natural breathing and an occasional soft blink continue.
Keep the LEFT 45% of the frame clean and uncluttered (soft blurred wall) for logo and copy added in post.
No products, no text in frame.
```
s07에는 제품과 로고를 생성하지 않고 `endcard_overlay.png`(실제 제품 사진과 로고)를 얹는다. 그래야 패키지 글자가 변형되지 않는다.

### 제품 클로즈업 처리 원칙
- s03, s04, s05, s06에서 생성된 라벨 글자가 조금이라도 틀어지면 그 컷은 쓰지 않는다. 대신 같은 구도로 **제품 없이 배경만 생성**하고, 원본 제품 사진을 합성한다(그림자와 색온도는 수동으로 맞춤).
- 지금 제품 이미지는 약 270×370px로 작고, **대각선 워터마크**가 비친다. 최종본에는 고해상도 원본 PNG(워터마크 없음, 배경 투명 권장)로 바꿔 넣는다. 파일명만 같으면 `node endcard/render.js`로 엔딩이 다시 만들어진다.

---

## 2단계. 사운드

**BGM**: 따뜻한 피아노에 은은한 현악, 약 72 BPM. 0초에 피아노 단음으로 시작, 6초에 현악 진입, 21초에 해결 화음, 24.4초부터 페이드아웃.
**현장음**: 낙엽 밟는 소리와 바람(s01–02), 새소리와 발걸음(s03), 매미 소리 아주 작게와 잔디(s04), 실내 룸톤과 옷깃 소리(s05), 그릇 내려놓는 소리와 꼬리가 바닥 쓰는 소리(s06). Seedance의 `generate_audio=true`로 생성한 현장음을 쓰고, 합본 때 −10dB로 낮춘다.

**내레이션**: 30대 여성, 차분하고 따뜻한 톤. 요청 원문 그대로이며 시점만 나눔.

| 시작 | 문장 |
|---|---|
| 0.4초 | 조금 느려진 걸음이 마음에 걸릴 때. |
| 3.4초 | 함께할 내일을 위해, |
| 7.0초 | 근육, |
| 11.0초 | 관절, |
| 15.0초 | 인지 건강 케어. |
| 18.5초 | 매일의 작은 돌봄. |
| 21.8초 | 사계절 내내, 우리 곁에. VetG. |

내레이션 파일 하나(`audio/narration.wav`, 25초, 위 시점에 맞춰 배치)로 만들면 `assemble.sh`가 BGM을 자동으로 덕킹한다.

---

## 3단계. 합본

```bash
bash shorts/vetg_sialic_vital/assemble.sh
```
- 결과물은 `out/vetg_sialic_vital_25s.mp4` (1080p, H.264, AAC)
- 테스트 화면 7개로 미리 돌려 봤음: 25.0초, 1920×1080, 자막과 엔딩 오버레이 위치 정상

## 표현 검수 체크리스트
- [ ] 복용 전후 비교, "회복", "치료", "치매 예방" 같은 표현이 없다 (지금 카피는 모두 "건강 케어"로만 표현)
- [ ] 급여량이나 급여 장면이 보이지 않는다 (s06은 제품을 그릇 옆에 두기만 함)
- [ ] 7개 컷 모두 같은 보더콜리다 (흰 블레이즈, 흰 가슴, 흰 앞발)
- [ ] 제품 색이 맞다: Muscle 블루 / Joint 퍼플 / Mind 그린
- [ ] 화면 안에서 생성된 글자가 없다 (자막과 로고는 모두 후편집으로 넣음)
- [ ] "동물병원 전용" 표기가 실제 제품 표시사항과 일치한다
