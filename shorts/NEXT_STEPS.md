# 05~08 렌더링 마무리 절차

막힌 이유: 이 환경에서 `media.canva.com` 접속이 네트워크 정책으로 차단됨.

1. 환경 설정 → Network access에 `media.canva.com`, `export-download.canva.com` 허용 (적용 안 되면 새 세션에서 진행)
2. 아직 안 만든 이미지 생성 (각 spec.py의 `IMAGES`에서 값이 `None`인 것)
   - 07_coffee 02.jpg: 염소 떼와 함께 있는 목동 (첫 시도는 Canva 안전 필터에 걸려서 문구를 바꿔야 함)
   - 08_pineapple 05/06/07.jpg: 귀족 파티 중앙의 파인애플 / 은쟁반에 파인애플을 나르는 하인 / 파인애플 지붕 석조 건물
   - 스타일 문구: "3D animated cartoon style like a Pixar film ..., square composition, no text"
3. Canva `get-assets`로 media id의 이미지를 받아 `shorts/NN_xxx/images/NN.jpg`로 저장 (1024px 이상)
4. `python3 shorts/engine/engine.py shorts/05_banana` (06, 07, 08도 같은 방식)
