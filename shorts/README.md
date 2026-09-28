# 쇼츠 제작 폴더

| # | 제목 (업로드용) | 길이 | 폴더 |
|---|---|---|---|
| 01 | 잠들 때 몸이 '툭' 떨어지는 이유 | 42.3초 | `01_hypnic-jerk/` |
| 02 | 케첩이 원래 생선 소스였다고? ㄷㄷ | 39.7초 | `02_ketchup/` |
| 03 | 당근이 원래 보라색이었다고? ㄷㄷ | 36.5초 | `03_carrot/` |
| 04 | 사람들이 감자를 훔치게 만든 천재 작전 ㅋㅋ | 34.4초 | `04_potato/` |

## 각 폴더 구성
- `short.mp4`: 바로 업로드 가능한 완성본 (1080×1920, 30fps, -14 LUFS 음량 정규화)
- `short_no-narration.mp4`: 내레이션만 뺀 버전 (다른 목소리로 더빙할 때)
- `thumbnail.jpg`: 커버로 고를 프레임
- `upload.txt`: 제목, 설명, 해시태그, 태그
- `subtitles.srt`: 자막 타이밍
- `spec.py`: 대본, 장면 구성, 효과음 설계

## 새 쇼츠 만들기
```bash
pip install pillow numpy imageio-ffmpeg playwright
python3 shorts/engine/engine.py shorts/05_새주제 --preview   # 장면별 미리보기
python3 shorts/engine/engine.py shorts/05_새주제             # 최종 렌더
```
`spec.py` 하나만 쓰면 됨 (기존 `02_ketchup/spec.py` 참고). 음성은 Google TTS, 폰트는 Google Fonts에서 자동으로 받음.
