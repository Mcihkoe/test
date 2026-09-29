# -*- coding: utf-8 -*-
# Style: 실사 planned (PROMPTS); motion-graphic fallback (MG) until images exist
from engine import E, RING, ARROW

SERIES = "🍽️ 식재료 비하인드"
SEED = 14
ACCENT = "#ffd600"
TITLE = ["옥수수의 조상은", "알갱이가 5개?"]
YT_TITLE = "옥수수 조상은 알갱이가 겨우 5개였다고? ㄷㄷ"
DESCRIPTION = """
지금은 알갱이 수백 개짜리 옥수수, 조상 '테오신트'는 알갱이가 겨우 5~12개였다 🌽
9000년 전 멕시코에서 시작된 인류 최고의 품종개량 이야기!
"""
TAGS = ["옥수수", "테오신트", "옥수수유래", "품종개량", "음식유래", "식재료", "잡학", "쇼츠", "shorts"]
THUMB_CUE = (2, "0.1")

STYLE = "photorealistic, cinematic lighting, documentary photo, square composition, no text, no watermark"
PROMPTS = {
    "01.jpg": "a big golden grilled corn on the cob with butter melting, close-up food photography",
    "02.jpg": "wild teosinte grass plants growing on a Mexican hillside, thin stalks, natural light",
    "03.jpg": "macro close-up comparison of a tiny teosinte ear with a few hard stone-like kernels next to a modern corn cob",
    "04.jpg": "ancient Mesoamerican farmer selecting and planting the largest corn seeds by hand in a field, historical film still",
    "05.jpg": "rows of modern corn cobs with hundreds of shiny yellow kernels piled at a harvest market",
    "06.jpg": "a husked corn cob with its leaves tightly wrapped lying on the ground in a field, close-up",
}
IMAGES = {k: None for k in PROMPTS}

MG = {
    "01.jpg": ("radial-gradient(circle,#fff176,#f57f17 80%)", [E("🌽", 330, 240, 420, anims=(("pop", "s", .45), ("wiggle", "s+.5", 1.2)))]),
    "02.jpg": ("linear-gradient(#c5e1a5,#558b2f)", [E("🌾", 180, 280, 330, anims=(("pop", "s", .45), ("wiggle", "s+.5", 1.4))), E("🌾", 560, 300, 300, anims=(("pop", "s+.15", .45), ("wiggle", "s+.7", 1.4))), E("🇲🇽", 820, 560, 150, anims=(("pop", "0.1", .4),))]),
    "03.jpg": ("linear-gradient(#efebe9,#a1887f)", [*[E("🪨", 180 + k * 150, 380, 120, anims=(("pop", f"0.1+{k * .1:.2f}", .35),)) for k in range(5)]]),
    "04.jpg": ("linear-gradient(#ffe0b2,#8d6e63)", [E("👨‍🌾", 170, 300, 320, anims=(("pop", "s", .45),)), E("🌽", 580, 300, 200, anims=(("pop", "0.1", .4),)), E("👍", 800, 320, 160, anims=(("pop", "0.2", .4),))]),
    "05.jpg": ("radial-gradient(circle,#fff59d,#ff8f00 80%)", [*[E("🌽", 100 + k * 220, 330 + (k % 2) * 60, 200, anims=(("pop", f"s+{k * .1:.2f}", .4),)) for k in range(4)]]),
    "06.jpg": ("linear-gradient(#dcedc8,#689f38)", [E("🌽", 360, 300, 340, anims=(("pop", "s", .45),)), E("🙅", 760, 360, 180, anims=(("pop", "0.1", .4),))]),
}

SCENES = [
    dict(img="01.jpg", kb="zoomin",
         lines=[dict(tts="옥수수의 조상은, 옥수수처럼 안 생겼음.", chunks=["옥수수의 조상은", "옥수수처럼 안 생겼음"])],
         els=[E("조상 = ???", 260, 70, 140, "big", (("pop", "0.1", .45),), "--r:-6deg")],
         sfx=[("thump", "0.1", .6)]),
    dict(img="02.jpg", kb="panr",
         lines=[dict(tts="조상 식물 테오신트는, 멕시코의 잡초 같은 풀.", chunks=["조상 식물 '테오신트'는", "멕시코의 잡초 같은 풀"])],
         els=[E("Teosinte<small>테오신트</small>", 280, 60, 100, "card", (("pop", "0.0", .45),), "--r:-3deg")],
         sfx=[("ding", "0.0")]),
    dict(img="03.jpg", kb="zoomin",
         lines=[dict(tts="알갱이는 겨우 5개에서 12개, 그것도 돌처럼 딱딱한 껍질에 싸여 있었음.",
                     chunks=["알갱이는 겨우 5~12개", "그것도 돌처럼 딱딱한", "껍질에 싸여 있었음"])],
         els=[E("5~12개", 330, 60, 170, "big", (("pop", "0.0", .45),), "--r:-6deg"),
              E("딱딱!", 700, 700, 110, "stamp", (("stamp", "0.1", .3),))],
         sfx=[("thump", "0.0", .5), ("chomp", "0.1"), ("buzz", "0.2")]),
    dict(img="04.jpg", kb="panl",
         lines=[dict(tts="약 9000년 전 멕시코 사람들이, 조금이라도 큰 것만 골라 심기 시작함.",
                     chunks=["약 9000년 전", "멕시코 사람들이", "조금이라도 큰 것만", "골라 심기 시작함"])],
         els=[E("9000년 전", 50, 50, 70, "tag", (("pop", "0.0", .4),)),
              E("큰 것만 ✔", 580, 700, 100, "bubble", (("pop", "0.2", .45),), "--r:3deg")],
         sfx=[("pop", "0.0"), ("ding", "0.2")]),
    dict(img="05.jpg", kb="zoomout",
         lines=[dict(tts="그걸 수천 년 반복하자, 알갱이 수백 개짜리 지금의 옥수수가 됨.",
                     chunks=["그걸 수천 년 반복하자", "알갱이 수백 개짜리", "지금의 옥수수가 됨"])],
         els=[E("5개 → 수백 개", 180, 60, 120, "big", (("pop", "0.1", .45),), "--r:-5deg")],
         sfx=[("sparkle", "0.1")]),
    dict(img="06.jpg", kb="zoomin",
         lines=[dict(tts="그래서 지금 옥수수는 사람 없이는 번식도 잘 못 함. 알갱이가 껍질에 싸여 떨어지질 않거든.",
                     chunks=["그래서 지금 옥수수는", "사람 없이는 번식도 잘 못 함", "알갱이가 껍질에 싸여", "떨어지질 않거든"])],
         els=[E("사람 없으면 ✕", 230, 60, 100, "card", (("pop", "0.1", .45),), "--r:-3deg;color:#c62828"),
              RING(330, 270, 420, "0.2")],
         sfx=[("buzz", "0.1"), ("pop", "0.2")]),
]
