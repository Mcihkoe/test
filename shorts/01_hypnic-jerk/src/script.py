# -*- coding: utf-8 -*-
# Short #1 — 잠들 때 몸이 '툭' 떨어지는 이유 (입면 경련 / hypnic jerk)
# Each scene = one visual; each line = one narration sentence split into on-screen subtitle chunks.
# "tts" is what the voice reads (numbers spelled out); "chunks" are what the viewer sees.

TITLE = ["잠들 때 몸이 '툭'", "떨어지는 진짜 이유"]
YT_TITLE = "잠들 때 몸이 '툭' 떨어지는 이유"

SCENES = [
    dict(id="bed", lines=[
        dict(tts="잠들기 직전, 몸이 갑자기 툭! 하고 떨어지는 느낌.",
             chunks=["잠들기 직전", "몸이 갑자기", "툭!", "하고 떨어지는 느낌"]),
        dict(tts="한 번쯤 겪어보셨죠?",
             chunks=["한 번쯤", "겪어보셨죠?"]),
    ]),
    dict(id="stats", lines=[
        dict(tts="이걸 입면 경련이라고 하는데, 무려 열 명 중 일곱 명이 겪는다고 함.",
             chunks=["이걸 '입면 경련'이라고", "하는데", "무려 10명 중", "7명이 겪는다고 함"]),
    ]),
    dict(id="brain", lines=[
        dict(tts="원인은 바로, 뇌의 착각.",
             chunks=["원인은 바로", "뇌의 착각"]),
    ]),
    dict(id="relax", lines=[
        dict(tts="잠이 들면서 온몸의 근육이 한순간에 풀리는데,",
             chunks=["잠이 들면서", "온몸의 근육이", "한순간에 풀리는데"]),
    ]),
    dict(id="alarm", lines=[
        dict(tts="뇌가 이걸, 지금 추락하고 있다고 오해해버림.",
             chunks=["뇌가 이걸", "'지금 추락 중'이라고", "오해해버림"]),
    ]),
    dict(id="zap", lines=[
        dict(tts="그래서 몸을 지키려고, 근육에 긴급 신호를 보내 움찔! 하게 만드는 것.",
             chunks=["그래서 몸을 지키려고", "근육에 긴급 신호를 보내", "움찔!", "하게 만드는 것"]),
    ]),
    dict(id="monkey", lines=[
        dict(tts="나무 위에서 자던 원숭이 조상 시절의 흔적이라는 가설도 있음.",
             chunks=["나무 위에서 자던", "원숭이 조상 시절의", "흔적이라는 가설도 있음"]),
        dict(tts="그땐 자다 떨어지면, 끝이었으니까.",
             chunks=["그땐 자다 떨어지면", "끝이었으니까"]),
    ]),
    dict(id="triggers", lines=[
        dict(tts="특히 커피, 스트레스, 피로가 쌓인 날 더 자주 나타남.",
             chunks=["특히 커피", "스트레스", "피로가 쌓인 날", "더 자주 나타남"]),
    ]),
    dict(id="ending", lines=[
        dict(tts="그러니까 오늘 밤 툭! 했다면, 당신 뇌가 당신을 구하려던 겁니다.",
             chunks=["그러니까 오늘 밤", "툭! 했다면", "당신 뇌가", "당신을 구하려던 겁니다"]),
    ]),
]
