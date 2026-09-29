# -*- coding: utf-8 -*-
# Style: 애니메이션 planned (PROMPTS); motion-graphic fallback (MG) until images exist
from engine import E, RING, ARROW, TCARD

SERIES = "🍽️ 식재료 비하인드"
SEED = 15
ACCENT = "#00e676"
TITLE = ["브로콜리·양배추·케일", "사실 다 같은 식물"]
YT_TITLE = "브로콜리랑 양배추가 같은 식물이라고? ㄷㄷ"
DESCRIPTION = """
브로콜리, 양배추, 케일, 콜리플라워, 콜라비, 방울양배추 🥦🥬
전부 '야생 양배추' 한 종에서 나온 형제들! 어디를 키우냐에 따라 달라진 채소 이야기
"""
TAGS = ["브로콜리", "양배추", "케일", "콜리플라워", "채소상식", "식재료", "잡학", "쇼츠", "shorts"]
THUMB_CUE = (0, "0.1")

STYLE = "3D animated cartoon style like a Pixar film, vibrant colors, square composition, no text, no watermark"
PROMPTS = {
    "01.jpg": "cute cartoon vegetable characters standing together like a family photo: broccoli, cabbage, kale, cauliflower, kohlrabi and brussels sprouts",
    "02.jpg": "a scrawny wild cabbage plant with a few leaves and small yellow flowers growing on a windy seaside cliff",
    "03.jpg": "a proud cartoon kale plant with huge ruffled leaves flexing like a bodybuilder in a garden",
    "04.jpg": "a round cartoon cabbage head with leaves tightly wrapped, smiling in a garden",
    "05.jpg": "cartoon broccoli and cauliflower characters showing off their big flower bud heads",
    "06.jpg": "a cartoon kohlrabi with a swollen round stem and a stalk of tiny brussels sprouts growing along a stem",
}
IMAGES = {k: None for k in PROMPTS}

MG = {
    "01.jpg": ("radial-gradient(circle,#b9f6ca,#1b5e20 80%)", [E("🥦", 110, 330, 230, anims=(("pop", "s", .4),)), E("🥬", 330, 330, 230, anims=(("pop", "s+.1", .4),)), E("🥗", 550, 330, 230, anims=(("pop", "s+.2", .4),)), E("🤍", 780, 360, 200, anims=(("pop", "s+.3", .4),))]),
    "02.jpg": ("linear-gradient(#81d4fa,#607d8b)", [E("🌿", 360, 280, 360, anims=(("pop", "s", .45), ("wiggle", "s+.5", 1.2))), E("🌼", 700, 280, 140, anims=(("pop", "0.1", .4),))]),
    "03.jpg": ("linear-gradient(#a5d6a7,#2e7d32)", [E("🥬", 330, 260, 400, anims=(("pop", "s", .45), ("pulse", "s+.5", .8)))]),
    "04.jpg": ("linear-gradient(#e8f5e9,#81c784)", [E("🥬", 330, 260, 400, anims=(("pop", "s", .45),)), E("🔄", 760, 300, 160, anims=(("pop", "s+.2", .4), ("spin", "s+.6", 2)))]),
    "05.jpg": ("linear-gradient(#c8e6c9,#388e3c)", [E("🥦", 170, 300, 340, anims=(("pop", "s", .45), ("bob", "s+.5", 1))), E("🌸", 620, 330, 260, anims=(("pop", "0.1", .45),))]),
    "06.jpg": ("linear-gradient(#f3e5f5,#8e24aa)", [E("🧅", 200, 330, 300, anims=(("pop", "s", .45),)), E("🟢", 620, 300, 110, anims=(("pop", "0.1", .35),)), E("🟢", 700, 400, 110, anims=(("pop", "0.1+.1", .35),)), E("🟢", 620, 500, 110, anims=(("pop", "0.1+.2", .35),))]),
    "07.jpg": ("radial-gradient(circle,#b9f6ca,#1b5e20 80%)", [E("🌿", 420, 330, 240, anims=(("pop", "s", .45),)), *[E(v, 100 + k * 230, 620, 140, anims=(("pop", f"s+{.2 + k * .1:.2f}", .35),)) for k, v in enumerate(("🥦", "🥬", "🥗", "🤍"))]]),
}

SCENES = [
    dict(img="01.jpg", kb="zoomin",
         lines=[dict(tts="브로콜리, 양배추, 케일, 콜리플라워. 이거 다 같은 식물임.",
                     chunks=["브로콜리, 양배추", "케일, 콜리플라워", "이거 다 같은 식물임"])],
         els=[E("= 같은 식물", 280, 80, 140, "big", (("pop", "0.2", .45),), "--r:-6deg;color:#00c853")],
         sfx=[("pop", "s"), ("thump", "0.2", .6)]),
    dict(img="02.jpg", kb="panr",
         lines=[dict(tts="전부 야생 양배추 한 종, 브라시카 올레라케아에서 나왔음.",
                     chunks=["전부 '야생 양배추' 한 종", "브라시카 올레라케아에서 나왔음"])],
         els=[E("Brassica oleracea<small>야생 양배추</small>", 190, 60, 80, "card", (("pop", "0.0", .45),), "--r:-3deg")],
         sfx=[("ding", "0.0")]),
    dict(img="03.jpg", kb="zoomin",
         lines=[dict(tts="사람들이 잎이 큰 것만 골라 키우면, 케일.", chunks=["잎이 큰 것만 골라 키우면", "케일"])],
         els=[E("잎 → 케일", 300, 70, 140, "big", (("pop", "0.1", .45),), "--r:-5deg;color:#2e7d32")],
         sfx=[("pop", "0.1")]),
    dict(img="04.jpg", kb="zoomout",
         lines=[dict(tts="잎이 둥글게 뭉친 걸 고르면, 양배추.", chunks=["잎이 둥글게 뭉친 걸 고르면", "양배추"])],
         els=[E("뭉친 잎 → 양배추", 150, 70, 100, "big", (("pop", "0.1", .45),), "--r:-5deg;color:#2e7d32")],
         sfx=[("pop", "0.1")]),
    dict(img="05.jpg", kb="zoomin",
         lines=[dict(tts="꽃봉오리가 큰 걸 고르면, 브로콜리와 콜리플라워.", chunks=["꽃봉오리가 큰 걸 고르면", "브로콜리와 콜리플라워"])],
         els=[E("꽃봉오리 → 브로콜리", 100, 70, 90, "big", (("pop", "0.1", .45),), "--r:-5deg;color:#2e7d32")],
         sfx=[("pop", "0.1")]),
    dict(img="06.jpg", kb="panl",
         lines=[dict(tts="줄기가 부푼 건 콜라비, 곁눈이 큰 건 방울양배추.", chunks=["줄기가 부푼 건 콜라비", "곁눈이 큰 건 방울양배추"])],
         els=[E("줄기 → 콜라비", 60, 70, 90, "bubble", (("pop", "0.0", .45),), "--r:-4deg"),
              E("곁눈 → 방울양배추", 220, 720, 90, "bubble", (("pop", "0.1", .45),), "--r:3deg")],
         sfx=[("pop", "0.0"), ("pop", "0.1")]),
    dict(img="07.jpg", kb="zoomin",
         lines=[dict(tts="결국 같은 식물에서, 어디를 키우느냐만 바꾼 셈.", chunks=["결국 같은 식물에서", "어디를 키우느냐만 바꾼 셈"])],
         els=[E("한 뿌리 6형제", 250, 70, 120, "stamp", (("stamp", "0.1", .3),), "color:#1b5e20;border-color:#1b5e20")],
         sfx=[("sparkle", "0.1")]),
]
PROMPTS["07.jpg"] = "a cartoon family tree illustration with a wild cabbage plant at the root branching into broccoli, cabbage, kale, cauliflower, kohlrabi and brussels sprouts"
IMAGES["07.jpg"] = None
