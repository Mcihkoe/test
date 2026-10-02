# -*- coding: utf-8 -*-
# Style: 실사 (PROMPTS); motion-graphic fallback (MG) when an image is missing
from engine import E, RING, ARROW

SERIES = "🍽️ 식재료 비하인드"
SEED = 20
ACCENT = "#ffca28"
TITLE = ["흰 달걀 vs 갈색 달걀", "뭐가 더 좋을까?"]
YT_TITLE = "흰 달걀이랑 갈색 달걀, 영양 차이 있을까? ㄷㄷ"
DESCRIPTION = """
흰 달걀과 갈색 달걀, 영양은 똑같다 🥚
껍데기 색은 닭 품종이, 노른자 색은 사료가 정한다는 사실!
"""
TAGS = ["달걀", "계란", "갈색달걀", "흰달걀", "노른자", "음식상식", "식재료", "잡학", "쇼츠", "shorts"]
THUMB_CUE = (0, "0.1")

STYLE = "photorealistic, natural light, food photography, square composition, no text, no watermark"
PROMPTS = {
    "01.jpg": "a white egg and a brown egg side by side on a wooden table, dramatic comparison lighting",
    "02.jpg": "a white leghorn hen and a brown hen standing side by side in a sunny farmyard",
    "03.jpg": "close-up of a white leghorn hen's face showing its white earlobe, farm background",
    "04.jpg": "a Korean grocery store shelf full of cartons of brown eggs",
    "05.jpg": "two fried eggs side by side, one with a pale yellow yolk and one with a deep orange yolk",
    "06.jpg": "a fresh egg cracked into a glass bowl showing a tall round yolk and thick egg white",
}
IMAGES = {k: None for k in PROMPTS}

MG = {
    "01.jpg": ("radial-gradient(circle,#fff8e1,#ffb300 80%)", [E("🥚", 200, 300, 300, anims=(("pop", "s", .45),)), E("🥚", 600, 300, 300, anims=(("pop", "s+.15", .45),), style="filter:sepia(1) saturate(2.5) brightness(.75);")]),
    "02.jpg": ("linear-gradient(#c5e1a5,#8d6e63)", [E("🐔", 180, 300, 320, anims=(("pop", "s", .45), ("bob", "s+.5", .9))), E("🐓", 600, 300, 320, anims=(("pop", "s+.15", .45), ("bob", "s+.7", .9)))]),
    "03.jpg": ("linear-gradient(#e8f5e9,#a5d6a7)", [E("🐔", 330, 260, 400, anims=(("pop", "s", .45),))]),
    "04.jpg": ("linear-gradient(#ffecb3,#a1887f)", [*[E("🥚", 120 + k * 180, 330 + (k % 2) * 70, 160, anims=(("pop", f"s+{k * .07:.2f}", .35),), style="filter:sepia(1) saturate(2.5) brightness(.75);") for k in range(5)], E("🇰🇷", 820, 600, 150, anims=(("pop", "0.1", .4),))]),
    "05.jpg": ("radial-gradient(circle,#fffde7,#ff8f00 80%)", [E("🍳", 160, 320, 320, anims=(("pop", "s", .45),), style="filter:saturate(.4) brightness(1.1);"), E("🍳", 600, 320, 320, anims=(("pop", "s+.15", .45),), style="filter:saturate(1.8) hue-rotate(-12deg);"), E("🌽", 440, 600, 160, anims=(("pop", "0.1", .4),))]),
    "06.jpg": ("radial-gradient(circle,#fffde7,#ffb300 80%)", [E("🥚", 330, 260, 400, anims=(("pop", "s", .45), ("pulse", "s+.5", .9))), E("✨", 760, 180, 150, anims=(("pop", "0.1", .4), ("pulse", "0.1+.4", .6)))]),
}

SCENES = [
    dict(img="01.jpg", kb="zoomin",
         lines=[dict(tts="흰 달걀이랑 갈색 달걀, 어느 쪽이 더 영양가 높을까?",
                     chunks=["흰 달걀이랑 갈색 달걀", "어느 쪽이 더 영양가 높을까?"])],
         els=[E("VS", 450, 80, 180, "big", (("pop", "0.0", .45),), "--r:-6deg")],
         sfx=[("thump", "0.0", .6), ("pop", "0.1")]),
    dict(img="02.jpg", kb="panr",
         lines=[dict(tts="정답은 똑같음. 껍데기 색은 닭 품종이 정하는 거.", chunks=["정답은 똑같음", "껍데기 색은", "닭 품종이 정하는 거"])],
         els=[E("영양 = 똑같음", 230, 70, 130, "big", (("pop", "0.0", .45),), "--r:-5deg;color:#2e7d32")],
         sfx=[("ding", "0.0")]),
    dict(img="03.jpg", kb="zoomin",
         lines=[dict(tts="재밌는 건, 닭 귓불 색으로 알 색을 대충 짐작할 수 있다는 거. 귓불이 하야면 흰 알을 낳는 경우가 많음.",
                     chunks=["재밌는 건", "닭 귓불 색으로", "알 색을 대충 짐작할 수 있음", "귓불이 하야면 흰 알"])],
         els=[RING(420, 380, 260, "0.1"), ARROW(150, 440, "0.1+.2", 0, 220),
              E("귓불 하양 → 흰 알", 170, 720, 90, "card", (("pop", "0.3", .45),), "--r:-3deg")],
         sfx=[("pop", "0.1"), ("ding", "0.3")]),
    dict(img="04.jpg", kb="panl",
         lines=[dict(tts="한국에 갈색 달걀이 많은 건, 갈색 알을 낳는 품종을 주로 키워서.",
                     chunks=["한국에 갈색 달걀이 많은 건", "갈색 알을 낳는 품종을", "주로 키워서"])],
         els=[E("🇰🇷 갈색이 대세", 220, 70, 100, "card", (("pop", "0.0", .45),), "--r:-3deg")],
         sfx=[("pop", "0.0")]),
    dict(img="05.jpg", kb="zoomin",
         lines=[dict(tts="노른자 색도 영양이 아니라, 닭이 먹은 사료 색 때문.", chunks=["노른자 색도", "영양이 아니라", "닭이 먹은 사료 색 때문"])],
         els=[E("진한 노른자 ≠ 영양", 110, 70, 92, "big", (("pop", "0.1", .45),), "--r:-4deg")],
         sfx=[("buzz", "0.1"), ("pop", "0.2")]),
    dict(img="06.jpg", kb="zoomout",
         lines=[dict(tts="결국 달걀은, 색보다 신선도가 중요.", chunks=["결국 달걀은", "색보다 신선도가 중요"])],
         els=[E("신선도 ✔", 350, 70, 150, "stamp", (("stamp", "0.1", .3),), "color:#2e7d32;border-color:#2e7d32")],
         sfx=[("sparkle", "0.1")]),
]
