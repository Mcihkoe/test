# -*- coding: utf-8 -*-
# Style: 애니메이션 (3D cartoon AI stills + Ken Burns motion) — period comedy fits a cartoon look
from engine import E, RING, ARROW

SERIES = "🍽️ 식재료 비하인드"
SEED = 8
ACCENT = "#ffd600"
TITLE = ["하루 렌탈비가 나왔던", "귀족들의 과일"]
YT_TITLE = "파인애플을 빌려서 파티하던 귀족들 ㅋㅋ"
DESCRIPTION = """
지금은 마트에서 몇 천 원이면 사는 파인애플, 18세기 유럽에선 부의 상징이었다 🍍
한 개에 지금 돈 수백만 원, 먹지도 않고 빌려서 전시만 하던 '파인애플 렌탈' 이야기!
"""
TAGS = ["파인애플", "파인애플유래", "귀족", "음식유래", "식재료", "역사", "잡학", "쇼츠", "shorts"]
THUMB_CUE = (4, "0.1")

IMAGES = {  # Canva media ids; 05/07 not generated (Canva quota) -> scene 5 reuses 01, 06 is a crop of 02
    "01.jpg": "MAHWdWsY9zA", "02.jpg": "MAHWdccQAqI", "03.jpg": "MAHWdbruo6U", "04.jpg": "MAHWdXSDU1Q",
}

SCENES = [
    dict(img="01.jpg", kb="zoomin",
         lines=[dict(tts="지금은 마트에서 몇 천 원이면 사는 파인애플, 옛날 유럽에선 부의 상징이었음.",
                     chunks=["마트에서 몇 천 원이면 사는", "파인애플", "옛날 유럽에선", "부의 상징이었음"])],
         els=[E("부의 상징", 290, 70, 150, "big", (("pop", "0.3", .45),), "--r:-6deg;color:#ffd600;-webkit-text-stroke:12px #000")],
         sfx=[("sparkle", "0.3")]),
    dict(img="02.jpg", kb="panr",
         lines=[dict(tts="콜럼버스가 처음 가져왔을 때, 유럽 사람들은 이 신기한 과일에 홀딱 반함.",
                     chunks=["콜럼버스가 처음 가져왔을 때", "유럽 사람들은", "이 신기한 과일에", "홀딱 반함"])],
         els=[E("1493년", 50, 50, 70, "tag", (("pop", "s+.2", .4),)),
              E("😍", 820, 80, 170, anims=(("pop", "0.3", .4), ("pulse", "0.3+.4", .6)))],
         sfx=[("ding", "0.3")]),
    dict(img="03.jpg", kb="zoomin",
         lines=[dict(tts="문제는, 유럽 날씨에선 거의 안 자란다는 거.", chunks=["문제는", "유럽 날씨에선", "거의 안 자란다는 거"])],
         els=[E("🥶", 780, 70, 180, anims=(("pop", "0.1", .4), ("wiggle", "0.1+.4", .4))),
              E("안 자람", 560, 560, 130, "stamp", (("stamp", "0.2", .3),))],
         sfx=[("buzz", "0.2")]),
    dict(img="04.jpg", kb="panl",
         lines=[dict(tts="귀족들은 난로 딸린 온실까지 지어서 키웠는데, 한 개 값이 지금 돈으로 수백만 원이었다고 함.",
                     chunks=["귀족들은 난로 딸린", "온실까지 지어서 키웠는데", "한 개 값이 지금 돈으로", "수백만 원이었다고 함"])],
         els=[E("🔥 난방 온실", 50, 50, 70, "tag", (("pop", "0.1", .4),)),
              E("1개 = 수백만 원", 170, 690, 110, "card", (("pop", "0.3", .45),), "--r:-3deg;color:#c62828")],
         sfx=[("ding", "0.3"), ("thump", "0.3", .5)]),
    dict(img="01.jpg", kb="zoomout",
         lines=[dict(tts="그래서 등장한 게 파인애플 렌탈. 파티 날 하루만 빌려서 식탁에 전시함.",
                     chunks=["그래서 등장한 게", "파인애플 렌탈", "파티 날 하루만 빌려서", "식탁에 전시함"])],
         els=[E("RENTAL", 330, 60, 150, "big", (("pop", "0.1", .45),), "--r:-6deg"),
              RING(360, 330, 360, "0.3"), ARROW(90, 420, "0.3+.2", 0, 230)],
         sfx=[("thump", "0.1", .6), ("pop", "0.3")]),
    dict(img="06.jpg", kb="zoomin",
         lines=[dict(tts="먹지도 않고 이 파티 저 파티 돌려 쓴 다음에야, 마지막에 팔려서 먹혔다고 함.",
                     chunks=["먹지도 않고", "이 파티 저 파티", "돌려 쓴 다음에야", "마지막에 팔려서 먹혔다고 함"])],
         els=[E("먹지 마시오 🚫", 250, 60, 90, "bubble", (("pop", "0.0", .45),), "--r:-3deg;color:#c62828"),
              E("↻", 830, 650, 200, "comic", (("pop", "0.1", .4), ("spin", "0.1+.4", 1.5)))],
         sfx=[("pop", "0.0"), ("whoosh", "0.1"), ("chomp", "0.3+.6")]),
]
