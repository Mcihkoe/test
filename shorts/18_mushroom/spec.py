# -*- coding: utf-8 -*-
# Style: 실사 (PROMPTS); motion-graphic fallback (MG) when an image is missing
from engine import E, RING, ARROW

SERIES = "🍽️ 식재료 비하인드"
SEED = 18
ACCENT = "#b388ff"
TITLE = ["버섯은 식물보다", "동물에 더 가깝다"]
YT_TITLE = "버섯이 식물보다 동물에 가깝다고? ㄷㄷ"
DESCRIPTION = """
채소 코너에 있지만 식물이 아닌 버섯 🍄
곤충 껍데기와 같은 성분 키틴, 그리고 세계에서 가장 큰 생물이 버섯이라는 사실까지!
"""
TAGS = ["버섯", "균류", "키틴", "뽕나무버섯", "생물상식", "식재료", "잡학", "쇼츠", "shorts"]
THUMB_CUE = (1, "0.1")

STYLE = "photorealistic, natural light, documentary photo, square composition, no text, no watermark"
PROMPTS = {
    "01.jpg": "a supermarket vegetable aisle with mushrooms in baskets next to lettuce and carrots",
    "02.jpg": "a wild mushroom growing on the forest floor next to a small curious deer, soft morning light",
    "03.jpg": "macro close-up of a shiny beetle shell next to a sliced mushroom, scientific comparison",
    "04.jpg": "white fungal mycelium threads spreading through decaying wood and leaves on the forest floor, macro",
    "05.jpg": "a vast dense coniferous forest in Oregon with clusters of honey mushrooms at the base of trees",
    "06.jpg": "sliced mushrooms sizzling in a pan with butter and garlic, close-up",
}
IMAGES = {k: None for k in PROMPTS}

MG = {
    "01.jpg": ("linear-gradient(#e8f5e9,#a5d6a7)", [E("🥬", 120, 330, 230, anims=(("pop", "s", .4),)), E("🍄", 400, 300, 300, anims=(("pop", "s+.15", .45), ("wiggle", "s+.6", 1))), E("🥕", 760, 330, 230, anims=(("pop", "s+.3", .4),))]),
    "02.jpg": ("linear-gradient(#d1c4e9,#4527a0)", [E("🍄", 200, 320, 300, anims=(("pop", "s", .45),)), E("🦌", 600, 300, 320, anims=(("pop", "0.0+.3", .45),)), E("🤝", 460, 560, 140, anims=(("pop", "0.1", .4),))]),
    "03.jpg": ("radial-gradient(circle,#fff3e0,#795548 80%)", [E("🍄", 180, 330, 300, anims=(("pop", "s", .45),)), E("🪲", 620, 330, 300, anims=(("pop", "0.1", .45), ("wiggle", "0.1+.5", 1)))]),
    "04.jpg": ("linear-gradient(#5d4037,#1b0f0a)", [E("🪵", 330, 360, 360, anims=(("pop", "s", .45),)), E("🕸️", 420, 200, 200, anims=(("spread", "0.1", .6),))]),
    "05.jpg": ("linear-gradient(#1b5e20,#0b2e0f)", [*[E("🌲", 40 + k * 210, 260 + (k % 2) * 60, 220, anims=(("pop", f"s+{k * .08:.2f}", .4),)) for k in range(5)], E("🍄", 430, 560, 180, anims=(("pop", "0.1", .4), ("pulse", "0.1+.4", .7)))]),
    "06.jpg": ("radial-gradient(circle,#ffe0b2,#bf360c 80%)", [E("🍳", 330, 260, 400, anims=(("pop", "s", .45),)), E("🍄", 470, 380, 140, anims=(("pop", "s+.3", .4),))]),
}

SCENES = [
    dict(img="01.jpg", kb="panr",
         lines=[dict(tts="버섯은 채소 코너에 있지만, 식물이 아님.", chunks=["버섯은 채소 코너에 있지만", "식물이 아님"])],
         els=[E("식물 ✕", 330, 70, 160, "big", (("pop", "0.1", .45),), "--r:-6deg")],
         sfx=[("buzz", "0.1")]),
    dict(img="02.jpg", kb="zoomin",
         lines=[dict(tts="오히려 식물보다, 동물에 더 가까운 생물.", chunks=["오히려 식물보다", "동물에 더 가까운 생물"])],
         els=[E("🍄 ≈ 🐾", 330, 70, 150, "big", (("pop", "0.1", .45),), "--r:-5deg;color:#7c4dff")],
         sfx=[("thump", "0.1", .6)]),
    dict(img="03.jpg", kb="zoomin",
         lines=[dict(tts="버섯 세포벽은 키틴이라는 성분인데, 이건 곤충 껍데기랑 같은 재료.",
                     chunks=["버섯 세포벽은", "'키틴'이라는 성분인데", "곤충 껍데기랑 같은 재료"])],
         els=[E("Chitin<small>키틴</small>", 330, 60, 110, "card", (("pop", "0.1", .45),), "--r:-3deg"),
              E("= 🪲 껍데기", 470, 720, 90, "bubble", (("pop", "0.2", .45),), "--r:3deg")],
         sfx=[("ding", "0.1"), ("pop", "0.2")]),
    dict(img="04.jpg", kb="panl",
         lines=[dict(tts="광합성도 못 해서, 우리처럼 다른 걸 분해해서 영양분을 얻음.",
                     chunks=["광합성도 못 해서", "우리처럼 다른 걸 분해해서", "영양분을 얻음"])],
         els=[E("광합성 ✕", 60, 70, 110, "stamp", (("stamp", "0.0", .3),))],
         sfx=[("buzz", "0.0"), ("chomp", "0.1")]),
    dict(img="05.jpg", kb="zoomout",
         lines=[dict(tts="참고로 세계에서 가장 큰 생물도 버섯 종류. 미국 오리건 숲 땅속에, 축구장 천 개 넘는 크기로 퍼져 있음.",
                     chunks=["세계에서 가장 큰 생물도", "버섯 종류", "미국 오리건 숲 땅속에", "축구장 1000개 넘는 크기"])],
         els=[E("🌍 세계 최대 생물", 180, 60, 90, "card", (("pop", "0.1", .45),), "--r:-3deg"),
              E("⚽×1000", 430, 700, 120, "big", (("pop", "0.3", .45),), "--r:-5deg")],
         sfx=[("sparkle", "0.1"), ("thump", "0.3", .6)]),
    dict(img="06.jpg", kb="zoomin",
         lines=[dict(tts="다음에 버섯 먹을 땐, 식물보다 우리 쪽 친척이라고 생각하면 됨.",
                     chunks=["다음에 버섯 먹을 땐", "식물보다 우리 쪽 친척이라고", "생각하면 됨"])],
         els=[E("먼 친척 🤝", 330, 70, 120, "bubble", (("pop", "0.1", .45),), "--r:-3deg")],
         sfx=[("pop", "0.1")]),
]
