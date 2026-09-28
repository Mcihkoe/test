# -*- coding: utf-8 -*-
# Style: 애니메이션 (3D cartoon AI stills + Ken Burns motion) — an inventor's story reads well as a cartoon
from engine import E, RING, ARROW

SERIES = "🍽️ 식재료 비하인드"
SEED = 12
ACCENT = "#ff5252"
TITLE = ["뒷마당 창고에서", "탄생한 라면"]
YT_TITLE = "라면이 뒷마당 창고에서 탄생했다고? ㄷㄷ"
DESCRIPTION = """
3분이면 끝나는 인스턴트 라면, 48살 아저씨가 뒷마당 창고에서 1년 동안 매달려 만든 발명품 🍜
아내의 튀김에서 찾은 비밀, 면을 기름에 튀겨 말리는 방법!
"""
TAGS = ["라면", "라면유래", "인스턴트라면", "안도모모후쿠", "음식유래", "발명", "잡학", "쇼츠", "shorts"]
THUMB_CUE = (3, "0.2")

STYLE = "3D animated cartoon style like a Pixar film, vibrant colors, square composition, no text, no watermark"
PROMPTS = {
    "01.jpg": "a steaming bowl of instant ramen noodles with a boiled egg and green onions, cozy warm kitchen light",
    "02.jpg": "post-war 1950s Japanese street at night, a long line of hungry people in old clothes waiting at a small noodle stall with a lantern, a middle-aged man in glasses watching thoughtfully",
    "03.jpg": "a determined middle-aged Japanese man in glasses experimenting with noodles late at night inside a small cluttered wooden backyard shed, a single hanging light bulb",
    "04.jpg": "a Japanese woman in a 1950s kitchen frying tempura in a pot of hot oil, her husband in glasses behind her having a lightbulb moment with sparkles",
    "05.jpg": "close-up of a dried fried noodle block in a bowl as hot water is poured over it, steam rising, noodles loosening",
    "06.jpg": "a proud middle-aged Japanese man in glasses holding up a package of the first instant noodles in 1958, confetti and celebration",
    "07.jpg": "a Korean high school student happily eating cup ramen at a convenience store window counter at night, city lights outside",
}
IMAGES = {k: None for k in PROMPTS}

SCENES = [
    dict(img="01.jpg", kb="zoomin",
         lines=[dict(tts="3분이면 끝나는 라면, 한 아저씨가 뒷마당 창고에서 만들었음.",
                     chunks=["3분이면 끝나는 라면", "한 아저씨가", "뒷마당 창고에서 만들었음"])],
         els=[E("⏱️ 3분", 60, 60, 80, "tag", (("pop", "0.0", .4),)),
              E("창고 출신?!", 520, 80, 130, "big", (("pop", "0.2", .45),), "--r:-6deg")],
         sfx=[("tick", "0.0"), ("thump", "0.2", .6)]),
    dict(img="02.jpg", kb="panr",
         lines=[dict(tts="전쟁 직후 일본, 라면 한 그릇 먹으려고 긴 줄을 선 사람들을 본, 안도 모모후쿠.",
                     chunks=["전쟁 직후 일본", "라면 한 그릇 먹으려고", "긴 줄을 선 사람들을 본", "안도 모모후쿠"])],
         els=[E("1950년대 일본", 50, 50, 70, "tag", (("pop", "s+.2", .4),)),
              ARROW(140, 480, "0.2", 0, 220),
              E("안도 모모후쿠", 560, 700, 90, "bubble", (("pop", "0.3", .45),), "--r:3deg")],
         sfx=[("pop", "0.2"), ("ding", "0.3")]),
    dict(img="03.jpg", kb="zoomin",
         lines=[dict(tts="집에서 쉽게 먹는 라면을 만들겠다며, 48살에 창고에서 1년 동안 매달림.",
                     chunks=["집에서 쉽게 먹는", "라면을 만들겠다며", "48살에", "창고에서 1년 동안 매달림"])],
         els=[E("48살", 70, 70, 150, "big", (("pop", "0.2", .45),), "--r:-6deg"),
              E("D+365", 700, 80, 110, "stamp", (("stamp", "0.3", .3),))],
         sfx=[("thump", "0.2", .5), ("tick", "0.3")]),
    dict(img="04.jpg", kb="panl",
         lines=[dict(tts="답은 부엌에 있었음. 아내가 튀김 만드는 걸 보고, 면을 기름에 튀겨 말리는 방법을 떠올림.",
                     chunks=["답은 부엌에 있었음", "아내가 튀김 만드는 걸 보고", "면을 기름에 튀겨 말리는", "방법을 떠올림"])],
         els=[E("💡", 780, 60, 190, anims=(("pop", "0.2", .4), ("pulse", "0.2+.4", .6))),
              E("튀김 → 면?!", 90, 80, 110, "bubble", (("pop", "0.2", .45),), "--r:-4deg")],
         sfx=[("ding", "0.2"), ("sparkle", "0.3")]),
    dict(img="05.jpg", kb="zoomin",
         lines=[dict(tts="튀기면 수분이 빠지면서 작은 구멍이 생기고, 뜨거운 물을 부으면 금방 풀어지는 거임.",
                     chunks=["튀기면 수분이 빠지면서", "작은 구멍이 생기고", "뜨거운 물을 부으면", "금방 풀어지는 거임"])],
         els=[RING(360, 380, 360, "0.1"),
              E("구멍 = 물길", 600, 80, 100, "bubble", (("pop", "0.1+.3", .45),), "--r:4deg")],
         sfx=[("pop", "0.1"), ("whoosh", "0.2")]),
    dict(img="06.jpg", kb="zoomout",
         lines=[dict(tts="그렇게 천구백오십팔년, 세계 최초의 인스턴트 라면 탄생.", chunks=["그렇게 1958년", "세계 최초의", "인스턴트 라면 탄생"])],
         els=[E("1958", 600, 70, 180, "big", (("pop", "0.0", .45),), "--r:-6deg"),
              E("세계 최초", 90, 90, 110, "stamp", (("stamp", "0.1", .3),))],
         sfx=[("thump", "0.0", .5), ("sparkle", "0.2")]),
    dict(img="07.jpg", kb="zoomin",
         lines=[dict(tts="한국엔 천구백육십삼년에 들어왔고, 지금은 1인당 라면 소비량 세계 최상위권.",
                     chunks=["한국엔 1963년에 들어왔고", "지금은 1인당 라면 소비량", "세계 최상위권"])],
         els=[E("🇰🇷 1963", 60, 60, 80, "tag", (("pop", "0.0", .4),)),
              E("세계 최상위권", 300, 690, 120, "stamp", (("stamp", "0.2", .3),), "color:#d50000;border-color:#d50000")],
         sfx=[("pop", "0.0"), ("ding", "0.2")]),
]
