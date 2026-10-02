# -*- coding: utf-8 -*-
# Style: 실사 (PROMPTS); motion-graphic fallback (MG) when an image is missing
from engine import E, RING, ARROW

SERIES = "🍽️ 식재료 비하인드"
SEED = 17
ACCENT = "#ffb74d"
TITLE = ["땅콩은 꽃이 피면", "땅속으로 숨는다"]
YT_TITLE = "땅콩이 땅속에서 열리는 신기한 방법 ㄷㄷ"
DESCRIPTION = """
땅콩은 견과류가 아니라 콩과 식물 🥜
땅 위에서 꽃이 피고, 줄기가 땅속으로 파고 들어가 열매를 맺는 신기한 식물!
"""
TAGS = ["땅콩", "땅콩재배", "콩과식물", "식물상식", "식재료", "잡학", "쇼츠", "shorts"]
THUMB_CUE = (3, "0.2")

STYLE = "photorealistic, natural light, documentary photo, square composition, no text, no watermark"
PROMPTS = {
    "01.jpg": "a pile of roasted peanuts in shells with a few cracked open on a rustic wooden table",
    "02.jpg": "a farmer pulling up a peanut plant from the soil showing many peanut pods hanging from the roots",
    "03.jpg": "close-up of small bright yellow peanut flowers on a green peanut plant in a field",
    "04.jpg": "macro close-up of a peanut peg, a thin stalk growing downward from the plant and pushing into the soil",
    "05.jpg": "cross-section view of soil showing peanut pods developing underground attached to pegs",
    "06.jpg": "a sunny peanut field in South America with Andes mountains in the background",
}
IMAGES = {k: None for k in PROMPTS}

MG = {
    "01.jpg": ("radial-gradient(circle,#ffe0b2,#8d6e63 80%)", [E("🥜", 330, 240, 420, anims=(("pop", "s", .45), ("wiggle", "s+.5", 1.2)))]),
    "02.jpg": ("linear-gradient(#c5e1a5,#6d4c41 60%)", [E("👨‍🌾", 160, 260, 320, anims=(("pop", "s", .45),)), E("🌱", 600, 250, 200, anims=(("pop", "s+.2", .4),)), E("🥜", 640, 480, 160, anims=(("pop", "0.1", .4), ("bob", "0.1+.4", .8)))]),
    "03.jpg": ("linear-gradient(#b3e5fc 0%,#b3e5fc 55%,#8d6e63 55%)", [E("🌱", 380, 230, 300, anims=(("pop", "s", .45),)), E("🌼", 470, 180, 150, anims=(("pop", "0.0+.3", .4), ("pulse", "0.0+.7", .8)))]),
    "04.jpg": ("linear-gradient(#b3e5fc 0%,#b3e5fc 45%,#8d6e63 45%)", [E("🌱", 380, 160, 260, anims=(("pop", "s", .45),)), E("⬇️", 450, 430, 170, anims=(("pop", "0.1", .4), ("bob", "0.1+.4", .6)))]),
    "05.jpg": ("linear-gradient(#b3e5fc 0%,#b3e5fc 30%,#6d4c41 30%)", [E("🌱", 420, 80, 220, anims=(("pop", "s", .45),)), *[E("🥜", 200 + k * 200, 520 + (k % 2) * 80, 150, anims=(("pop", f"0.1+{k * .12:.2f}", .4),)) for k in range(4)]]),
    "06.jpg": ("linear-gradient(#fff59d,#7cb342)", [E("⛰️", 330, 180, 400, anims=(("pop", "s", .45),)), E("🌎", 780, 520, 180, anims=(("pop", "0.0", .4),))]),
}

SCENES = [
    dict(img="01.jpg", kb="zoomin",
         lines=[dict(tts="땅콩, 견과류처럼 먹지만, 사실 콩과 식물임.", chunks=["땅콩", "견과류처럼 먹지만", "사실 콩과 식물임"])],
         els=[E("견과류 ✕ 콩 ⭕", 220, 70, 120, "big", (("pop", "0.2", .45),), "--r:-5deg")],
         sfx=[("thump", "0.2", .6)]),
    dict(img="02.jpg", kb="panr",
         lines=[dict(tts="근데 진짜 신기한 건, 자라는 방법.", chunks=["근데 진짜 신기한 건", "자라는 방법"])],
         els=[E("???", 760, 80, 160, "comic", (("pop", "0.1", .4),), "--r:8deg")],
         sfx=[("pop", "0.1")]),
    dict(img="03.jpg", kb="zoomin",
         lines=[dict(tts="땅콩은 꽃이 땅 위에서 핌. 노란 꽃이 지고 나면,", chunks=["땅콩은 꽃이 땅 위에서 핌", "노란 꽃이 지고 나면"])],
         els=[RING(380, 300, 330, "0.0"), E("🌼 땅 위", 60, 60, 80, "tag", (("pop", "0.0", .4),))],
         sfx=[("sparkle", "0.0")]),
    dict(img="04.jpg", kb="panu",
         lines=[dict(tts="꽃이 있던 자리에서 줄기가 아래로 쭉 자라서, 땅속으로 파고 들어감.",
                     chunks=["꽃이 있던 자리에서", "줄기가 아래로 쭉 자라서", "땅속으로 파고 들어감"])],
         els=[ARROW(560, 420, "0.1", 90, 230), E("푹!", 720, 640, 150, "comic", (("pop", "0.2", .35),), "--r:-8deg")],
         sfx=[("whoosh", "0.1"), ("thump", "0.2", .6)]),
    dict(img="05.jpg", kb="zoomin",
         lines=[dict(tts="그리고 땅속에서 열매가 자라는 거임. 그래서 이름도 땅콩.",
                     chunks=["그리고 땅속에서", "열매가 자라는 거임", "그래서 이름도 '땅'콩"])],
         els=[E("땅 + 콩", 340, 70, 170, "big", (("pop", "0.2", .45),), "--r:-6deg")],
         sfx=[("pop", "0.1"), ("ding", "0.2")]),
    dict(img="06.jpg", kb="panl",
         lines=[dict(tts="고향은 남아메리카. 수천 년 전부터 키웠다고 함.", chunks=["고향은 남아메리카", "수천 년 전부터", "키웠다고 함"])],
         els=[E("📍 남아메리카", 50, 50, 70, "tag", (("pop", "0.0", .4),))],
         sfx=[("pop", "0.0")]),
]
