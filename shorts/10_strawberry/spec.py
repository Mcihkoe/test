# -*- coding: utf-8 -*-
# Style: 실사 (photoreal AI stills + Ken Burns motion)
from engine import E, RING, ARROW

SERIES = "🍽️ 식재료 비하인드"
SEED = 10
ACCENT = "#ff1744"
TITLE = ["딸기에 박힌 점들", "씨가 아니었다"]
YT_TITLE = "딸기 겉에 박힌 게 씨가 아니라고? ㄷㄷ"
DESCRIPTION = """
딸기 겉의 작은 점들, 사실 씨가 아니라 하나하나가 진짜 열매 🍓
식물학적으로 딸기는 베리가 아니고, 오히려 바나나가 베리라는 사실까지!
"""
TAGS = ["딸기", "딸기씨", "식물학", "베리", "음식상식", "식재료", "잡학", "쇼츠", "shorts"]
THUMB_CUE = (0, "0.2")

STYLE = "photorealistic, macro food photography, studio lighting, square composition, no text, no watermark"
PROMPTS = {
    "01.jpg": "extreme close-up of a single ripe red strawberry showing the tiny yellow seed-like dots on its surface, water droplets",
    "02.jpg": "extreme macro of the tiny yellow achenes embedded in the red skin of a strawberry, shallow depth of field",
    "03.jpg": "a strawberry sliced in half lengthwise on a white plate showing its pale inner flesh and red edges",
    "04.jpg": "a ripe banana and a strawberry placed side by side on a wooden table, playful comparison composition",
    "05.jpg": "18th-century French botanical garden in Brittany, rows of wild strawberry plants with small white flowers, a botanist in period clothing examining them, historical film still",
    "06.jpg": "a woven basket overflowing with fresh ripe strawberries, bright summer light",
}
IMAGES = {k: None for k in PROMPTS}

MG = {
    "01.jpg": ("radial-gradient(circle,#ff8a80,#b71c1c 78%)", [E("🍓", 320, 230, 440, anims=(("pop", "s", .45),))]),
    "02.jpg": ("radial-gradient(circle,#ffcdd2,#c62828 80%)", [E("🍓", 250, 260, 400, anims=(("pop", "s", .45),)), E("🔍", 640, 380, 260, anims=(("pop", "0.0+.3", .4), ("wiggle", "0.0+.7", 1)))]),
    "03.jpg": ("linear-gradient(#fce4ec,#f48fb1)", [E("🍓", 340, 280, 400, anims=(("pop", "s", .45), ("pulse", "s+.5", .9)))]),
    "04.jpg": ("linear-gradient(#fff3e0,#ffcc80)", [E("🍓", 170, 320, 320, anims=(("pop", "0.1", .45),)), E("🍌", 600, 320, 320, anims=(("pop", "0.2", .45), ("wiggle", "0.3", .8)))]),
    "05.jpg": ("linear-gradient(#c5e1a5,#33691e)", [E("🌎", 430, 220, 220, anims=(("pop", "s", .45),)), E("🍓", 130, 430, 220, anims=(("flyR", "0.2", .5),)), E("🍓", 730, 430, 220, anims=(("flyL", "0.2", .5),)), E("❤️", 480, 470, 140, anims=(("pop", "0.3", .4), ("pulse", "0.3+.4", .6)))]),
    "06.jpg": ("radial-gradient(circle,#ff8a80,#880e4f 80%)", [E("🧺", 350, 300, 360, anims=(("pop", "s", .45),)), *[E("🍓", 120 + k * 220, 700 - (k % 2) * 60, 120, anims=(("pop", f"s+{.1 + k * .08:.2f}", .4),)) for k in range(4)]]),
}

SCENES = [
    dict(img="01.jpg", kb="zoomin",
         lines=[dict(tts="딸기 겉에 박힌 이 점들, 씨가 아님.", chunks=["딸기 겉에 박힌", "이 점들", "씨가 아님"])],
         els=[RING(380, 330, 300, "0.1"), ARROW(110, 400, "0.1+.2", 0, 230),
              E("씨 ✕", 640, 80, 150, "big", (("pop", "0.2", .45),), "--r:-6deg")],
         sfx=[("pop", "0.1"), ("buzz", "0.2")]),
    dict(img="02.jpg", kb="zoomin",
         lines=[dict(tts="하나하나가 사실은 진짜 열매이고, 그 안에 아주 작은 씨가 들어 있음.",
                     chunks=["하나하나가 사실은", "진짜 열매이고", "그 안에 아주 작은", "씨가 들어 있음"])],
         els=[E("점 1개 = 열매 1개", 190, 60, 100, "card", (("pop", "0.1", .45),), "--r:-3deg")],
         sfx=[("ding", "0.1")]),
    dict(img="03.jpg", kb="zoomout",
         lines=[dict(tts="우리가 먹는 빨간 부분은, 꽃턱이 부풀어 오른 거임.", chunks=["우리가 먹는 빨간 부분은", "'꽃턱'이 부풀어 오른 거임"])],
         els=[E("꽃턱", 700, 90, 130, "bubble", (("pop", "0.1", .45),), "--r:5deg;color:#c62828"),
              ARROW(560, 300, "0.1+.2", 135, 200)],
         sfx=[("pop", "0.1")]),
    dict(img="04.jpg", kb="panr",
         lines=[dict(tts="그래서 식물학적으론 딸기는 베리가 아니고, 오히려 바나나가 베리임.",
                     chunks=["그래서 식물학적으론", "딸기는 베리가 아니고", "오히려 바나나가", "베리임"])],
         els=[E("🍓 베리 ✕", 80, 70, 90, "bubble", (("pop", "0.1", .45),), "--r:-4deg;color:#c62828"),
              E("🍌 베리 ⭕", 600, 70, 90, "bubble", (("pop", "0.2", .45),), "--r:4deg;color:#2e7d32")],
         sfx=[("buzz", "0.1"), ("ding", "0.3")]),
    dict(img="05.jpg", kb="panl",
         lines=[dict(tts="지금의 큰 딸기는, 십팔세기 프랑스에서 아메리카 딸기 두 종이 우연히 섞여 탄생함.",
                     chunks=["지금의 큰 딸기는", "18세기 프랑스에서", "아메리카 딸기 두 종이", "우연히 섞여 탄생함"])],
         els=[E("🇫🇷 18세기", 50, 50, 70, "tag", (("pop", "0.1", .4),)),
              E("북미 🍓 × 남미 🍓", 200, 690, 90, "card", (("pop", "0.2", .45),), "--r:-3deg")],
         sfx=[("pop", "0.1"), ("sparkle", "0.3")]),
    dict(img="06.jpg", kb="zoomin",
         lines=[dict(tts="딸기 한 입에, 열매 약 이백 개를 먹는 셈.", chunks=["딸기 한 입에", "열매 약 200개를", "먹는 셈"])],
         els=[E("×200", 600, 80, 190, "big", (("pop", "0.1", .45),), "--r:-8deg")],
         sfx=[("thump", "0.1", .6)]),
]
