# -*- coding: utf-8 -*-
# Style: 애니메이션 planned (PROMPTS); motion-graphic fallback (MG) until images exist
from engine import E, RING, ARROW

SERIES = "🍽️ 식재료 비하인드"
SEED = 16
ACCENT = "#76ff03"
TITLE = ["아보카도 씨가", "쓸데없이 큰 이유"]
YT_TITLE = "아보카도 씨가 이렇게 큰 이유 ㄷㄷ"
DESCRIPTION = """
아보카도 씨, 왜 이렇게 클까? 🥑
통째로 삼켜서 씨를 퍼뜨려 주던 거대 동물들이 멸종해버렸다는 가설!
"""
TAGS = ["아보카도", "아보카도씨", "거대땅늘보", "멸종", "음식상식", "식재료", "잡학", "쇼츠", "shorts"]
THUMB_CUE = (3, "0.1")

STYLE = "3D animated cartoon style like a Pixar film, vibrant colors, square composition, no text, no watermark"
PROMPTS = {
    "01.jpg": "a ripe avocado cut in half showing an enormous round seed, cartoon kitchen, dramatic spotlight on the seed",
    "02.jpg": "a small cartoon bird looking at a huge avocado seed with a worried face, unable to swallow it, jungle background",
    "03.jpg": "a prehistoric jungle with giant ancient mammals, huge ground sloth and gomphotheres, eating fruits from trees",
    "04.jpg": "a giant ground sloth happily swallowing a whole avocado in one bite, cartoon, prehistoric forest",
    "05.jpg": "a lonely avocado tree in a quiet prehistoric landscape at sunset, fossil bones of a giant sloth nearby",
    "06.jpg": "a smiling farmer caring for rows of avocado trees in a modern orchard, bright sunny day",
}
IMAGES = {k: None for k in PROMPTS}

MG = {
    "01.jpg": ("radial-gradient(circle,#ccff90,#33691e 80%)", [E("🥑", 330, 240, 420, anims=(("pop", "s", .45), ("pulse", "s+.5", .9)))]),
    "02.jpg": ("linear-gradient(#a5d6a7,#1b5e20)", [E("🐦", 170, 330, 260, anims=(("pop", "s", .45), ("wiggle", "s+.5", .8))), E("🟤", 600, 330, 280, anims=(("pop", "s+.2", .45),)), E("😰", 260, 200, 130, anims=(("pop", "0.1", .4),))]),
    "03.jpg": ("linear-gradient(#ffcc80,#6d4c41)", [E("🦥", 120, 300, 330, anims=(("pop", "s", .45),)), E("🦣", 560, 300, 330, anims=(("pop", "s+.15", .45),))]),
    "04.jpg": ("linear-gradient(#dcedc8,#558b2f)", [E("🦥", 180, 300, 360, anims=(("pop", "s", .45), ("bob", "s+.5", .9))), E("🥑", 620, 360, 200, anims=(("grab", "0.1", .8),))]),
    "05.jpg": ("linear-gradient(#ffab91,#4e342e)", [E("🌳", 340, 220, 420, anims=(("pop", "s", .45),)), E("🦴", 120, 620, 160, anims=(("pop", "0.1", .4),)), E("🦴", 820, 620, 140, anims=(("pop", "0.1+.15", .4),))]),
    "06.jpg": ("linear-gradient(#fff9c4,#8bc34a)", [E("👨‍🌾", 170, 300, 320, anims=(("pop", "s", .45),)), E("🌳", 560, 260, 360, anims=(("pop", "s+.2", .45),)), E("🥑", 720, 420, 140, anims=(("pop", "0.1", .4), ("bob", "0.1+.4", .8)))]),
}

SCENES = [
    dict(img="01.jpg", kb="zoomin",
         lines=[dict(tts="아보카도 씨, 이상하게 크지 않음?", chunks=["아보카도 씨", "이상하게 크지 않음?"])],
         els=[RING(360, 330, 360, "0.0", "#ff1744"), E("왜 이렇게 큼?", 230, 60, 130, "big", (("pop", "0.1", .45),), "--r:-5deg")],
         sfx=[("pop", "0.0"), ("thump", "0.1", .6)]),
    dict(img="02.jpg", kb="panr",
         lines=[dict(tts="과일은 보통 동물이 먹고 씨를 퍼뜨리는데, 이 씨를 통째로 삼킬 동물은 지금 거의 없음.",
                     chunks=["과일은 보통 동물이 먹고", "씨를 퍼뜨리는데", "이 씨를 통째로 삼킬 동물은", "지금 거의 없음"])],
         els=[E("꿀꺽 불가 🚫", 520, 700, 100, "bubble", (("pop", "0.3", .45),), "--r:3deg;color:#c62828")],
         sfx=[("buzz", "0.3")]),
    dict(img="03.jpg", kb="panl",
         lines=[dict(tts="그래서 나온 가설이, 옛날 거대 동물들이 먹었다는 것.", chunks=["그래서 나온 가설이", "옛날 거대 동물들이 먹었다는 것"])],
         els=[E("가설", 60, 60, 80, "tag", (("pop", "0.0", .4),), "background:#6a1b9a"),
              E("거대 동물", 470, 700, 110, "stamp", (("stamp", "0.1", .3),))],
         sfx=[("ding", "0.0"), ("thump", "0.1", .6)]),
    dict(img="04.jpg", kb="zoomin",
         lines=[dict(tts="몸길이 몇 미터짜리 거대 땅늘보 같은 동물이, 통째로 삼키고 멀리 퍼뜨렸다는 거.",
                     chunks=["몸길이 몇 미터짜리", "거대 땅늘보 같은 동물이", "통째로 삼키고", "멀리 퍼뜨렸다는 거"])],
         els=[E("꿀꺽!", 620, 80, 160, "comic", (("pop", "0.2", .35),), "--r:8deg"),
              E("거대 땅늘보", 60, 60, 70, "tag", (("pop", "0.1", .4),))],
         sfx=[("chomp", "0.2"), ("thump", "0.2+.2", .5)]),
    dict(img="05.jpg", kb="zoomout",
         lines=[dict(tts="그런데 약 1만 년 전 이 동물들이 멸종하면서, 아보카도는 짝꿍을 잃어버림.",
                     chunks=["그런데 약 1만 년 전", "이 동물들이 멸종하면서", "아보카도는 짝꿍을 잃어버림"])],
         els=[E("멸종", 360, 70, 170, "stamp", (("stamp", "0.1", .3),)),
              E("💔", 820, 680, 150, anims=(("pop", "0.2", .4),))],
         sfx=[("buzz", "0.1"), ("thump", "0.2", .5)]),
    dict(img="06.jpg", kb="panr",
         lines=[dict(tts="그 뒤론 사람이 키워준 덕분에 살아남았다는 해석. 이제 사람이 새 짝꿍인 셈.",
                     chunks=["그 뒤론 사람이 키워준 덕분에", "살아남았다는 해석", "이제 사람이 새 짝꿍인 셈"])],
         els=[E("새 짝꿍 = 사람 🤝", 180, 70, 100, "card", (("pop", "0.2", .45),), "--r:-3deg")],
         sfx=[("sparkle", "0.2")]),
]
