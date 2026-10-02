# -*- coding: utf-8 -*-
# Style: 애니메이션 (PROMPTS); motion-graphic fallback (MG) when an image is missing
from engine import E, RING, ARROW

SERIES = "🍽️ 식재료 비하인드"
SEED = 19
ACCENT = "#ce93d8"
TITLE = ["고구마는 뿌리", "감자는 줄기?"]
YT_TITLE = "고구마랑 감자, 먹는 부위가 완전 다르다고? ㄷㄷ"
DESCRIPTION = """
고구마는 뿌리, 감자는 땅속 줄기 🍠🥔
그리고 굶주린 백성을 살리려 고구마를 조선에 들여온 통신사 조엄 이야기까지!
"""
TAGS = ["고구마", "감자", "조엄", "고구마유래", "음식유래", "식재료", "역사", "잡학", "쇼츠", "shorts"]
THUMB_CUE = (1, "0.1")

STYLE = "3D animated cartoon style like a Pixar film, vibrant colors, square composition, no text, no watermark"
PROMPTS = {
    "01.jpg": "a cute cartoon sweet potato and a cute cartoon potato standing side by side looking at each other suspiciously",
    "02.jpg": "a cross-section of soil showing a sweet potato growing from plant roots and a potato growing from an underground stem",
    "03.jpg": "close-up of a cartoon potato with small sprouts growing out of its eyes, kitchen counter",
    "04.jpg": "a Joseon dynasty Korean envoy in traditional official robes and gat hat on a wooden ship deck holding sweet potatoes, 18th century",
    "05.jpg": "hungry Joseon villagers in hanbok happily receiving baked sweet potatoes from an official in a snowy village",
    "06.jpg": "steaming roasted sweet potatoes split open showing golden orange flesh in a winter street cart",
}
IMAGES = {k: None for k in PROMPTS}

MG = {
    "01.jpg": ("radial-gradient(circle,#f3e5f5,#6a1b9a 80%)", [E("🍠", 160, 300, 320, anims=(("pop", "s", .45), ("wiggle", "s+.5", 1))), E("🥔", 600, 300, 320, anims=(("pop", "s+.15", .45), ("wiggle", "s+.6", 1)))]),
    "02.jpg": ("linear-gradient(#b3e5fc 0%,#b3e5fc 30%,#6d4c41 30%)", [E("🌱", 200, 100, 180, anims=(("pop", "s", .4),)), E("🍠", 160, 420, 260, anims=(("pop", "0.0+.3", .45),)), E("🌱", 640, 100, 180, anims=(("pop", "s", .4),)), E("🥔", 600, 420, 260, anims=(("pop", "0.1+.3", .45),))]),
    "03.jpg": ("linear-gradient(#fff8e1,#d7ccc8)", [E("🥔", 330, 280, 400, anims=(("pop", "s", .45),)), E("🌱", 560, 230, 150, anims=(("pop", "0.1", .4), ("bob", "0.1+.4", .8)))]),
    "04.jpg": ("linear-gradient(#81d4fa,#0277bd)", [E("⛵", 120, 280, 320, anims=(("pop", "s", .45), ("bob", "s+.5", 1.2))), E("🍠", 600, 320, 280, anims=(("pop", "0.2", .45),))]),
    "05.jpg": ("linear-gradient(#eceff1,#90a4ae)", [*[E("🧑", 100 + k * 220, 400, 180, anims=(("pop", f"s+{k * .1:.2f}", .4),)) for k in range(4)], E("🍠", 430, 200, 200, anims=(("pop", "0.1", .4), ("pulse", "0.1+.4", .7)))]),
    "06.jpg": ("radial-gradient(circle,#ffcc80,#bf360c 80%)", [E("🍠", 330, 260, 400, anims=(("pop", "s", .45), ("pulse", "s+.5", .9))), E("♨️", 760, 160, 160, anims=(("pop", "s+.3", .4), ("bob", "s+.7", .8)))]),
}

SCENES = [
    dict(img="01.jpg", kb="zoomin",
         lines=[dict(tts="고구마랑 감자, 비슷해 보이지만 먹는 부위가 완전 다름.",
                     chunks=["고구마랑 감자", "비슷해 보이지만", "먹는 부위가 완전 다름"])],
         els=[E("VS", 440, 80, 180, "big", (("pop", "0.0", .45),), "--r:-6deg")],
         sfx=[("thump", "0.0", .6), ("ding", "0.2")]),
    dict(img="02.jpg", kb="zoomin",
         lines=[dict(tts="고구마는 뿌리가 부푼 거고, 감자는 땅속 줄기가 부푼 거임.",
                     chunks=["고구마는 뿌리가 부푼 거고", "감자는 땅속 줄기가 부푼 거임"])],
         els=[E("뿌리", 150, 720, 110, "bubble", (("pop", "0.0", .45),), "--r:-4deg;color:#6a1b9a"),
              E("줄기", 620, 720, 110, "bubble", (("pop", "0.1", .45),), "--r:4deg;color:#6d4c41")],
         sfx=[("pop", "0.0"), ("pop", "0.1")]),
    dict(img="03.jpg", kb="zoomin",
         lines=[dict(tts="그래서 감자엔 눈이 있어서 거기서 싹이 남. 줄기의 마디거든.",
                     chunks=["그래서 감자엔 '눈'이 있어서", "거기서 싹이 남", "줄기의 마디거든"])],
         els=[RING(480, 200, 280, "0.1"), E("눈 = 줄기 마디", 160, 720, 100, "card", (("pop", "0.2", .45),), "--r:-3deg")],
         sfx=[("pop", "0.1"), ("ding", "0.2")]),
    dict(img="04.jpg", kb="panr",
         lines=[dict(tts="고구마가 조선에 들어온 건 천칠백육십년대. 일본에 간 통신사 조엄이, 대마도에서 들여왔음.",
                     chunks=["고구마가 조선에 들어온 건", "1760년대", "일본에 간 통신사 조엄이", "대마도에서 들여왔음"])],
         els=[E("1760년대", 50, 50, 70, "tag", (("pop", "0.1", .4),)),
              E("통신사 조엄", 480, 700, 100, "bubble", (("pop", "0.2", .45),), "--r:3deg")],
         sfx=[("pop", "0.1"), ("ding", "0.2")]),
    dict(img="05.jpg", kb="zoomin",
         lines=[dict(tts="흉년에 굶는 백성들을 살리려고 가져왔다는 이야기.", chunks=["흉년에 굶는 백성들을", "살리려고 가져왔다는 이야기"])],
         els=[E("❤️ 구황작물", 300, 70, 110, "card", (("pop", "0.1", .45),), "--r:-3deg")],
         sfx=[("sparkle", "0.1")]),
    dict(img="06.jpg", kb="zoomout",
         lines=[dict(tts="이름도 대마도 말 고코이모에서 왔다는 설이 유력함.", chunks=["이름도 대마도 말", "'고코이모'에서 왔다는", "설이 유력함"])],
         els=[E("고코이모 → 고구마", 170, 70, 100, "big", (("pop", "0.1", .45),), "--r:-4deg;color:#8e24aa")],
         sfx=[("pop", "0.1"), ("ding", "0.2")]),
]
