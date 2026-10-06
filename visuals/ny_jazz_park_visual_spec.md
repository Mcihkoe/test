# 비주얼 초안: New York 오후 재즈 파크

장르: 뉴욕 오후에 듣는 Jazzy 파크 음악 (BGM 플레이리스트)
초안 파일: `ny_jazz_park_bg.svg` (벡터 원본), `ny_jazz_park_bg.png` (1920×1080)

## 1. 콘셉트
- 시간대: 늦은 오후(골든아워), 따뜻한 오렌지·크림 톤
- 장소: 센트럴파크 느낌의 공원 + 멀리 맨해튼 스카이라인(안개 낀 실루엣)
- 소품: 벤치, 가로등, 단풍 든 나무, 색소폰(재즈 상징), 떠다니는 음표
- 무드: 여유, 따뜻함, 도시 속 쉼표. 눈이 편한 저채도 + 약한 필름 그레인

## 2. 컬러 팔레트
| 용도 | 색상 |
|---|---|
| 하늘 상단 | #F4A261 |
| 하늘 하단/빛 | #FDECCF |
| 건물 실루엣 | #C98F6B |
| 잔디 | #6B8F4E → #3F5F37 |
| 단풍 포인트 | #E29A2F, #C4572A |
| 가로등 불빛 | #FFE9A0 |

## 3. 영상 제작 시 움직임 (ffmpeg/편집용 레이어 분리 제안)
정지 이미지 한 장만 쓰면 반복 콘텐츠로 보일 수 있으므로 약한 움직임을 추가합니다.
1. 배경 전체 느린 줌인/팬 (60초에 3~5%)
2. 음표 레이어가 천천히 위로 떠오르며 페이드
3. 햇빛 광선 레이어의 은은한 밝기 깜빡임(반짝임)
4. 가로등 불빛 미세 펄스, 나뭇잎 흔들림(선택)
5. 하단 또는 모서리에 "Now Playing: 곡명" 텍스트 오버레이(선택)

## 4. AI 이미지/영상 생성용 프롬프트 (고품질 버전 제작 시)
**이미지 (영문 권장)**
```
Cozy New York park in the late afternoon, golden hour, warm orange and cream sky,
hazy Manhattan skyline in the distance, autumn trees with amber leaves,
a wooden park bench and a vintage street lamp, a saxophone resting on the bench,
soft film grain, lo-fi jazz illustration style, flat vector-like shapes with painterly light,
calm relaxing mood, no people, no text, wide 16:9, 1920x1080
```
**네거티브**: text, logo, watermark, realistic faces, brand names, cluttered details

**루프 영상(5~10초) 프롬프트 추가**
```
Gentle camera push-in, leaves swaying slightly, sunlight flickering through trees,
floating musical notes drifting upward, seamless loop
```

## 5. 시리즈화 (채널 통일감)
- 같은 구도 틀에서 시간/계절만 변경: 오후(이 초안) / 비 오는 저녁 / 눈 오는 겨울 / 새벽
- 썸네일: 같은 배경 + 큰 글씨 1~2줄 ("NY Afternoon Jazz | 2 Hours"), 폰트·위치 고정
- 곡 분위기별 배경 매칭 규칙을 표로 관리 (예: 느린 템포=저녁 노을, 밝은 스윙=한낮 햇빛)

## 6. 주의
- 실존 상표·간판·유명 건물 로고 사용 금지, 사람 얼굴 생략(초상권/AI 합성 표기 리스크 감소)
- AI 이미지 서비스를 쓸 경우 상업적 이용 가능 여부 확인
- 유튜브 설명란에 AI 활용 사실 표기 권장
