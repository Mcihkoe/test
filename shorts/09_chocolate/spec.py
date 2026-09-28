# -*- coding: utf-8 -*-
# Style: 실사 (photoreal AI stills + Ken Burns motion)
from engine import E, RING, ARROW

SERIES = "🍽️ 식재료 비하인드"
SEED = 9
ACCENT = "#ff9e40"
TITLE = ["달콤한 초콜릿의", "매운 과거"]
YT_TITLE = "초콜릿이 원래 쓰고 매운 음료였다고? ㄷㄷ"
DESCRIPTION = """
달콤한 초콜릿, 원래는 고추를 넣은 쓰고 매운 음료였다 🍫🌶️
카카오 콩이 돈으로 쓰이던 아즈텍부터 초콜릿 바가 탄생하기까지!
"""
TAGS = ["초콜릿", "초콜릿유래", "카카오", "아즈텍", "음식유래", "식재료", "잡학", "쇼츠", "shorts"]
THUMB_CUE = (1, "0.2")

STYLE = "photorealistic, cinematic lighting, documentary photo, square composition, no text, no watermark"
PROMPTS = {
    "01.jpg": "close-up of a hand snapping a glossy dark chocolate bar, crumbs, warm moody light",
    "02.jpg": "ancient Aztec noble in feathered headdress pouring a frothy dark cacao drink from a height between two clay cups, red chili peppers on the table, torchlight, historical film still",
    "03.jpg": "ancient Mesoamerican market scene, a woven basket full of cacao beans being traded for a live turkey, historical film still",
    "04.jpg": "17th-century Spanish aristocrats in lace collars sipping hot chocolate from porcelain cups in an ornate palace room, sugar bowl on the table, oil-painting-like lighting",
    "05.jpg": "19th-century chocolate factory, workers in aprons pouring liquid chocolate into rectangular bar molds, vintage industrial interior",
    "06.jpg": "silky milk chocolate being poured and swirling with fresh milk, luxurious food photography",
    "07.jpg": "happy person biting into a chocolate bar with eyes closed, cozy cafe background, bokeh",
}
IMAGES = {k: None for k in PROMPTS}  # Canva media ids once generated

# Motion-graphic fallback per image (used until the AI image exists)
MG = {
    "01.jpg": ("radial-gradient(circle,#8d5524,#2b1408 75%)", [E("🍫", 330, 240, 400, anims=(("pop", "s", .45), ("wiggle", "s+.5", 1.2)))]),
    "02.jpg": ("radial-gradient(circle,#ff9800,#4e1f00 80%)", [E("🏺", 130, 280, 330, anims=(("pop", "s", .45),)), E("🫘", 520, 360, 200, anims=(("pop", "0.1", .4),)), E("🌶️", 740, 340, 220, anims=(("pop", "0.2", .4), ("wiggle", "0.2+.4", .8)))]),
    "03.jpg": ("linear-gradient(#a5d6a7,#33691e)", [E("🦃", 150, 300, 330, anims=(("pop", "0.1", .45), ("bob", "0.1+.5", 1))), E("🫘", 620, 360, 260, anims=(("pop", "0.2", .45),))]),
    "04.jpg": ("radial-gradient(circle,#e57373,#4a0000 80%)", [E("👑", 430, 220, 220, anims=(("dropIn", "s", .5),)), E("☕", 380, 400, 320, anims=(("pop", "s+.2", .45),)), E("🍬", 740, 520, 180, anims=(("pop", "0.1", .4),))]),
    "05.jpg": ("linear-gradient(#90a4ae,#37474f)", [E("🏭", 110, 280, 330, anims=(("pop", "s", .45),)), E("🍫", 600, 360, 280, anims=(("flyL", "0.1", .5),))]),
    "06.jpg": ("linear-gradient(#fff8e1,#d7ccc8)", [E("🥛", 180, 300, 320, anims=(("pop", "s", .45),)), E("🍫", 580, 300, 320, anims=(("pop", "0.0+.3", .45), ("bob", "0.0+.8", 1.2)))]),
    "07.jpg": ("radial-gradient(circle,#f8bbd0,#ad1457 80%)", [E("😋", 360, 260, 360, anims=(("pop", "s", .45), ("pulse", "s+.5", .8))), E("🍫", 120, 520, 180, anims=(("pop", "0.1", .4),)), E("🍫", 780, 520, 180, anims=(("pop", "0.2", .4),))]),
}

SCENES = [
    dict(img="01.jpg", kb="zoomin",
         lines=[dict(tts="달콤한 초콜릿, 원래는 쓰고 매운 음료였음.", chunks=["달콤한 초콜릿", "원래는", "쓰고 매운 음료였음"])],
         els=[E("쓰고 매움?!", 200, 70, 140, "big", (("pop", "0.2", .45),), "--r:-7deg")],
         sfx=[("thump", "0.2", .6)]),
    dict(img="02.jpg", kb="panr",
         lines=[dict(tts="고대 아즈텍 사람들은 카카오를 갈아서, 고추를 넣고 거품 내서 마셨음.",
                     chunks=["고대 아즈텍 사람들은", "카카오를 갈아서", "고추를 넣고", "거품 내서 마셨음"])],
         els=[E("📍 아즈텍", 50, 50, 70, "tag", (("pop", "s+.2", .4),)),
              E("🌶️ + 🍫", 470, 90, 120, "bubble", (("pop", "0.2", .45),), "--r:4deg")],
         sfx=[("pop", "0.2")]),
    dict(img="03.jpg", kb="zoomin",
         lines=[dict(tts="심지어 카카오 콩은 돈이었음. 칠면조 한 마리가 콩 백 알 정도였다는 기록도 있음.",
                     chunks=["심지어 카카오 콩은 돈이었음", "칠면조 한 마리가", "콩 100알 정도였다는", "기록도 있음"])],
         els=[E("💰 카카오 = 돈", 250, 60, 100, "card", (("pop", "0.0", .45),), "--r:-3deg"),
              E("🦃 = 🫘×100", 330, 700, 90, "bubble", (("pop", "0.2", .45),), "--r:3deg")],
         sfx=[("ding", "0.0"), ("pop", "0.2")]),
    dict(img="04.jpg", kb="panl",
         lines=[dict(tts="스페인 사람들이 유럽으로 가져가서 설탕을 넣자, 귀족들이 푹 빠짐.",
                     chunks=["스페인 사람들이 유럽으로 가져가서", "설탕을 넣자", "귀족들이 푹 빠짐"])],
         els=[E("+ 설탕", 70, 80, 130, "big", (("pop", "0.1", .45),), "--r:-6deg;color:#fff;-webkit-text-stroke:12px #000"),
              E("😍", 840, 90, 160, anims=(("pop", "0.2", .4), ("pulse", "0.2+.4", .6)))],
         sfx=[("sparkle", "0.1"), ("pop", "0.2")]),
    dict(img="05.jpg", kb="zoomin",
         lines=[dict(tts="먹는 초콜릿 바가 처음 나온 건, 천팔백사십칠년 영국.", chunks=["먹는 초콜릿 바가", "처음 나온 건", "1847년 영국"])],
         els=[E("1847", 580, 70, 170, "big", (("pop", "0.2", .45),), "--r:-6deg"),
              E("🇬🇧", 60, 60, 160, anims=(("pop", "0.2+.2", .4),))],
         sfx=[("thump", "0.2", .5)]),
    dict(img="06.jpg", kb="zoomout",
         lines=[dict(tts="우유를 넣은 밀크 초콜릿은 그보다 더 뒤, 천팔백칠십년대 스위스.",
                     chunks=["우유를 넣은 밀크 초콜릿은", "그보다 더 뒤", "1870년대 스위스"])],
         els=[E("🥛 밀크 초콜릿", 60, 60, 70, "tag", (("pop", "0.0", .4),)),
              E("🇨🇭 1870년대", 330, 700, 100, "card", (("pop", "0.2", .45),), "--r:3deg")],
         sfx=[("pop", "0.0"), ("ding", "0.2")]),
    dict(img="07.jpg", kb="zoomin",
         lines=[dict(tts="그러니까 초콜릿이 달콤해진 건, 겨우 몇백 년밖에 안 됐음.",
                     chunks=["그러니까 초콜릿이 달콤해진 건", "겨우 몇백 년밖에", "안 됐음"])],
         els=[E("달콤한 역사 = 몇백 년", 170, 60, 90, "card", (("pop", "0.1", .45),), "--r:-3deg")],
         sfx=[("sparkle", "0.1")]),
]
