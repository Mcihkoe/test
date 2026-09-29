# -*- coding: utf-8 -*-
# Style: 실사 planned (PROMPTS); motion-graphic fallback (MG) until images exist
from engine import E, RING, ARROW

SERIES = "🍽️ 식재료 비하인드"
SEED = 13
ACCENT = "#ff1744"
TITLE = ["옛날 수박은", "빨간색이 아니었다"]
YT_TITLE = "옛날 수박 속은 하얬다고? ㄷㄷ"
DESCRIPTION = """
여름 필수템 수박, 옛날엔 속이 거의 하얗고 빨간 부분은 조금뿐이었다 🍉
이집트 무덤 속 수박 씨부터 17세기 그림 속 수박, 씨 없는 수박의 비밀까지!
"""
TAGS = ["수박", "수박유래", "씨없는수박", "음식유래", "식재료", "잡학", "쇼츠", "shorts"]
THUMB_CUE = (3, "0.2")

STYLE = "photorealistic, cinematic lighting, documentary photo, square composition, no text, no watermark"
PROMPTS = {
    "01.jpg": "a juicy bright red watermelon slice on a summer picnic table, water droplets, bright sunlight",
    "02.jpg": "an ancient Egyptian tomb interior with painted walls and a small clay bowl of dark watermelon seeds on a stone ledge, torchlight",
    "03.jpg": "a small round wild striped melon lying in dry African desert sand under harsh sun",
    "04.jpg": "a 17th-century Italian still-life oil painting of a cut watermelon with pale swirly flesh and only small pockets of red",
    "05.jpg": "a modern watermelon field with farmers harvesting large striped watermelons, one cut open showing deep red flesh",
    "06.jpg": "a seedless watermelon cut in half on a white plate showing deep red flesh with only tiny white soft seeds",
}
IMAGES = {k: None for k in PROMPTS}

MG = {
    "01.jpg": ("radial-gradient(circle,#ff8a80,#b71c1c 78%)", [E("🍉", 330, 240, 420, anims=(("pop", "s", .45), ("wiggle", "s+.5", 1.2)))]),
    "02.jpg": ("linear-gradient(#8d6e63,#3e2723)", [E("🏺", 140, 300, 320, anims=(("pop", "s", .45),)), E("🫘", 560, 380, 180, anims=(("pop", "0.1", .4),)), E("🔦", 760, 400, 180, anims=(("flyL", "0.1", .5),))]),
    "03.jpg": ("linear-gradient(#ffe0b2,#e6a45a)", [E("☀️", 780, 60, 180, anims=(("pop", "s", .4), ("pulse", "s+.4", 1))), E("🍈", 360, 300, 360, anims=(("pop", "s+.2", .45),)), E("💧", 180, 380, 160, anims=(("pop", "0.1", .4), ("bob", "0.1+.4", .8)))]),
    "04.jpg": ("linear-gradient(#d7ccc8,#6d4c41)", [E("🖼️", 330, 250, 420, anims=(("pop", "s", .45),)), E("🌀", 470, 390, 150, anims=(("pop", "0.1", .4), ("spin", "0.1+.4", 3)))]),
    "05.jpg": ("linear-gradient(#aed581,#33691e)", [*[E("🍉", 90 + k * 230, 360 + (k % 2) * 60, 190, anims=(("pop", f"s+{k * .1:.2f}", .4),)) for k in range(4)], E("👨‍🌾", 420, 580, 170, anims=(("pop", "0.1", .4),))]),
    "06.jpg": ("radial-gradient(circle,#ffcdd2,#c62828 80%)", [E("🍉", 330, 260, 400, anims=(("pop", "s", .45), ("pulse", "s+.5", .9)))]),
}

SCENES = [
    dict(img="01.jpg", kb="zoomin",
         lines=[dict(tts="여름엔 수박이지. 근데 옛날 수박은, 속이 거의 하얬음.",
                     chunks=["여름엔 수박이지", "근데 옛날 수박은", "속이 거의 하얬음"])],
         els=[E("하얀 수박?!", 260, 70, 140, "big", (("pop", "0.2", .45),), "--r:-6deg")],
         sfx=[("thump", "0.2", .6)]),
    dict(img="02.jpg", kb="zoomin",
         lines=[dict(tts="수박의 고향은 아프리카. 이집트 무덤에선 수천 년 전 수박 씨가 발견되기도 함.",
                     chunks=["수박의 고향은 아프리카", "이집트 무덤에선", "수천 년 전 수박 씨가", "발견되기도 함"])],
         els=[E("📍 아프리카", 50, 50, 70, "tag", (("pop", "0.0", .4),)),
              E("수천 년 전 씨앗", 280, 700, 100, "card", (("pop", "0.2", .45),), "--r:-3deg")],
         sfx=[("pop", "0.0"), ("ding", "0.2")]),
    dict(img="03.jpg", kb="panr",
         lines=[dict(tts="옛날엔 과육보다, 물과 씨를 얻으려고 키웠다는 해석이 많음.",
                     chunks=["옛날엔 과육보다", "물과 씨를 얻으려고", "키웠다는 해석이 많음"])],
         els=[E("💧 물통 + 🫘 간식", 170, 70, 100, "bubble", (("pop", "0.1", .45),), "--r:-3deg")],
         sfx=[("pop", "0.1")]),
    dict(img="04.jpg", kb="zoomin",
         lines=[dict(tts="십칠세기 이탈리아 그림을 보면, 수박 속이 소용돌이 모양에 빨간 부분은 조금뿐.",
                     chunks=["17세기 이탈리아 그림을 보면", "수박 속이 소용돌이 모양에", "빨간 부분은 조금뿐"])],
         els=[E("🇮🇹 17세기 그림", 50, 50, 70, "tag", (("pop", "0.0", .4),)),
              RING(380, 330, 320, "0.1"), E("빨강 조금", 480, 700, 110, "stamp", (("stamp", "0.2", .3),))],
         sfx=[("pop", "0.1"), ("buzz", "0.2")]),
    dict(img="05.jpg", kb="panl",
         lines=[dict(tts="사람들이 달고 빨간 것만 골라 심기를 수백 년, 지금의 새빨간 수박이 된 거임.",
                     chunks=["달고 빨간 것만 골라 심기를", "수백 년", "지금의 새빨간 수박이 된 거임"])],
         els=[E("수백 년 품종개량", 220, 60, 90, "card", (("pop", "0.1", .45),), "--r:-3deg")],
         sfx=[("sparkle", "0.2")]),
    dict(img="06.jpg", kb="zoomout",
         lines=[dict(tts="참고로 씨 없는 수박은 유전자 조작이 아니라, 염색체 수를 맞춰 교배해서 만든 거임.",
                     chunks=["참고로 씨 없는 수박은", "유전자 조작이 아니라", "염색체 수를 맞춰", "교배해서 만든 거임"])],
         els=[E("GMO ✕", 90, 70, 140, "big", (("pop", "0.1", .45),), "--r:-6deg"),
              E("🧬 염색체 교배", 380, 700, 90, "bubble", (("pop", "0.2", .45),), "--r:3deg")],
         sfx=[("buzz", "0.1"), ("ding", "0.2")]),
]
