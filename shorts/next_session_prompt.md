유튜브 쇼츠 채널 "이게 된다고?"의 2차 영상 제작이야. 이 브랜치의 shorts/ 폴더에 1차 작업물(파이프라인 shorts/tools/make.py·render.py·check.py, 에피소드 spec.json들, plans.md, plans_v2.md, upload.md)이 있으니 먼저 읽고 1차 방식을 파악해 줘.

배경: 이전 세션에서 yt-dlp로 받으려니 영상 데이터 단계에서 HTTP 403이 났고 로그에 "PO Token Providers: none"이 찍혔어. 지금은 .claude/settings.json에 yt-dlp, npm ci, npx tsc, node 실행 허용 규칙을 넣어 뒀어.

1. pip install -U --pre "yt-dlp[default]" bgutil-ytdlp-pot-provider 로 설치. scratchpad에 https://github.com/Brainicism/bgutil-ytdlp-pot-provider 를 clone해서 server 폴더에서 npm ci → npx tsc → node build/main.js 로 PO 토큰 서버(127.0.0.1:4416)를 백그라운드로 띄워.
2. 테스트로 https://www.youtube.com/shorts/kbWJfqYP6_8 한 편만 shorts/raw/ref/ 로 받아 봐. (a) web+PO 토큰 (b) mweb+PO 토큰 (c) 옵션 없이 순서로, 요청 사이 15초 이상 간격.
3. 받아지면 shorts/pc/refs.txt 나머지 레퍼런스를 30초 간격으로 받고, 1차 때처럼 프레임 시트·받아쓰기·사실 확인·장면 계획 후 바로 make.py로 렌더해 (승인 대기 없이).
   - 원본 출처 표기 없음 / 빨간 원 없음 / 모든 영상 하단에 "이게 된다고?" / check.py로 점검
4. 완성 mp4는 shorts/out/ 에 두고 SendUserFile로 나한테 보내서 바로 내려받을 수 있게 해. 편마다 업로드용 제목·설명도 upload.md 형식으로 정리. mp4·raw 영상은 커밋하지 마.
5. PO 토큰을 붙여도 403/429/봇 확인으로 막히면 다른 우회 시도 없이 오류를 정리해 보고하고 멈춰. 쿠키·API 키를 붙여넣으라고 하지 말고 cookies*.txt는 커밋하지 마.
