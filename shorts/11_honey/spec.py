# -*- coding: utf-8 -*-
# Style: 실사 (photoreal AI stills + Ken Burns motion)
from engine import E, RING, ARROW

SERIES = "🍽️ 식재료 비하인드"
SEED = 11
ACCENT = "#ffb300"
TITLE = ["수천 년이 지나도", "안 썩는 음식"]
YT_TITLE = "수천 년 된 꿀도 안 썩는 이유 ㄷㄷ"
DESCRIPTION = """
고대 이집트 무덤에서 나온 수천 년 된 꿀단지 🍯
꿀이 안 썩는 과학적인 이유와, 꿀벌 한 마리가 평생 모으는 꿀의 양까지!
※ 돌 전 아기에게는 꿀을 먹이면 안 됩니다.
"""
TAGS = ["꿀", "꿀유통기한", "꿀벌", "이집트", "음식과학", "식재료", "잡학", "쇼츠", "shorts"]
THUMB_CUE = (1, "0.2")

STYLE = "photorealistic, cinematic lighting, documentary photo, square composition, no text, no watermark"
PROMPTS = {
    "01.jpg": "thick golden honey dripping slowly from a wooden honey dipper into a glass jar, glowing backlight",
    "02.jpg": "archaeologists with flashlights discovering an ancient sealed clay jar inside a dim Egyptian tomb with hieroglyphs on the walls, historical film still",
    "03.jpg": "extreme macro of thick glossy honey surface with tiny bubbles, golden amber color",
    "04.jpg": "extreme macro close-up of a honeybee on a honeycomb filled with honey, sharp detail",
    "05.jpg": "a single honeybee next to a tiny drop of honey on a silver teaspoon, macro photography, scale comparison",
    "06.jpg": "a jar of honey on a kitchen table next to a baby bottle and a small red warning sign, soft light",
}
IMAGES = {k: None for k in PROMPTS}

MG = {
    "01.jpg": ("radial-gradient(circle,#ffd54f,#e65100 80%)", [E("🍯", 350, 250, 400, anims=(("pop", "s", .45), ("pulse", "s+.5", 1)))]),
    "02.jpg": ("linear-gradient(#5d4037,#1b0f0a)", [E("🏺", 360, 300, 360, anims=(("pop", "s", .45),)), E("🔦", 60, 420, 200, anims=(("flyR", "0.0", .5),))]),
    "03.jpg": ("radial-gradient(circle,#ffe082,#ff8f00 80%)", [E("🍯", 380, 250, 320, anims=(("pop", "s", .45),))]),
    "04.jpg": ("repeating-linear-gradient(60deg,#ffca28 0 40px,#ffb300 40px 80px)", [E("🐝", 380, 260, 340, anims=(("pop", "s", .45), ("bob", "s+.5", .8)))]),
    "05.jpg": ("linear-gradient(#fffde7,#ffe082)", [E("🐝", 330, 320, 230, anims=(("pop", "s", .45), ("bob", "s+.5", .8))), E("🥄", 620, 330, 300, anims=(("pop", "0.1", .45),))]),
    "06.jpg": ("linear-gradient(#e3f2fd,#90caf9)", [E("🍯", 300, 320, 280, anims=(("pop", "s", .45),)), E("🍼", 640, 320, 280, anims=(("pop", "0.0+.2", .45),)), E("🚫", 620, 300, 320, anims=(("stamp", "0.1", .3),))]),
}

SCENES = [
    dict(img="01.jpg", kb="zoomin",
         lines=[dict(tts="유통기한이 사실상 없는 음식, 바로 꿀임.", chunks=["유통기한이 사실상 없는 음식", "바로 꿀임"])],
         els=[E("유통기한 ∞", 170, 70, 140, "big", (("pop", "0.1", .45),), "--r:-6deg")],
         sfx=[("sparkle", "0.1")]),
    dict(img="02.jpg", kb="zoomin",
         lines=[dict(tts="이집트 고대 무덤에서, 수천 년 된 꿀단지가 발견된 적도 있음.",
                     chunks=["이집트 고대 무덤에서", "수천 년 된 꿀단지가", "발견된 적도 있음"])],
         els=[E("📍 이집트", 50, 50, 70, "tag", (("pop", "s+.2", .4),)),
              RING(390, 420, 320, "0.1"), E("수천 년!", 420, 90, 130, "big", (("pop", "0.2", .45),), "--r:6deg")],
         sfx=[("pop", "0.1"), ("thump", "0.2", .5)]),
    dict(img="03.jpg", kb="zoomout",
         lines=[dict(tts="꿀이 안 썩는 이유는, 수분이 적고 산성이라 세균이 살 수가 없기 때문.",
                     chunks=["꿀이 안 썩는 이유는", "수분이 적고 산성이라", "세균이 살 수가 없기 때문"])],
         els=[E("💧 수분 적음", 60, 70, 90, "bubble", (("pop", "0.1", .4),), "--r:-4deg"),
              E("🍋 산성", 640, 70, 90, "bubble", (("pop", "0.1+.3", .4),), "--r:4deg"),
              E("🦠✕", 420, 620, 170, "big", (("stamp", "0.2", .3),))],
         sfx=[("pop", "0.1"), ("pop", "0.1+.3"), ("buzz", "0.2")]),
    dict(img="04.jpg", kb="panr",
         lines=[dict(tts="게다가 꿀벌이 넣는 효소가, 세균을 막는 성분까지 만들어냄.",
                     chunks=["게다가 꿀벌이 넣는 효소가", "세균을 막는 성분까지", "만들어냄"])],
         els=[E("🐝 천연 방부제", 250, 60, 100, "card", (("pop", "0.1", .45),), "--r:-3deg")],
         sfx=[("ding", "0.1")]),
    dict(img="05.jpg", kb="zoomin",
         lines=[dict(tts="근데 꿀벌 한 마리가 평생 모으는 꿀은, 겨우 티스푼 십이분의 일.",
                     chunks=["근데 꿀벌 한 마리가", "평생 모으는 꿀은", "겨우 티스푼 1/12"])],
         els=[E("평생 = 1/12 티스푼", 170, 60, 100, "card", (("pop", "0.2", .45),), "--r:-3deg;color:#c62828"),
              ARROW(160, 520, "0.2+.3", 20, 220)],
         sfx=[("thump", "0.2", .5)]),
    dict(img="06.jpg", kb="zoomin",
         lines=[dict(tts="단, 돌 전 아기에겐 절대 주면 안 됨. 보툴리누스균 위험 때문.",
                     chunks=["단, 돌 전 아기에겐", "절대 주면 안 됨", "보툴리누스균 위험 때문"])],
         els=[E("⚠️", 60, 50, 190, anims=(("pop", "0.0", .4), ("pulse", "0.0+.4", .6))),
              E("돌 전 아기 금지", 280, 690, 110, "stamp", (("stamp", "0.1", .3),))],
         sfx=[("alarm", "0.0"), ("thump", "0.1", .6)]),
]
