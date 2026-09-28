# -*- coding: utf-8 -*-
# Style: 실사 (photoreal AI stills + Ken Burns motion)
from engine import E, RING, ARROW

SERIES = "🍽️ 식재료 비하인드"
SEED = 5
ACCENT = "#ffd600"
TITLE = ["지금 먹는 바나나는", "사실 2대째다"]
YT_TITLE = "우리가 먹는 바나나가 2대째인 이유 ㄷㄷ"
DESCRIPTION = """
1950년대까지 전 세계가 먹던 바나나는 지금 바나나가 아니었다? 🍌
'그로 미셸'이 사라지고 '캐번디시'가 된 이유, 그리고 지금 바나나가 또 위험한 이유까지!
"""
TAGS = ["바나나", "그로미셸", "캐번디시", "파나마병", "음식유래", "식재료", "잡학", "쇼츠", "shorts"]
THUMB_CUE = (3, "0.3")

IMAGES = {  # Canva media ids (None = not generated yet)
    "01.jpg": 'MAHWdIKtb1s',
    "02.jpg": 'MAHWdNVpYh0',
    "03.jpg": 'MAHWdOqlKCc',
    "04.jpg": 'MAHWdB9RohM',
    "05.jpg": 'MAHWdaO6fKo',
    "06.jpg": 'MAHWdXm01BM',
    "07.jpg": 'MAHWdD1kDLw',
    "08.jpg": 'MAHWdQDLp60',
}

SCENES = [
    dict(img="01.jpg", kb="zoomin",
         lines=[dict(tts="지금 우리가 먹는 이 바나나, 사실 2대째 바나나임.",
                     chunks=["지금 우리가 먹는", "이 바나나", "사실 2대째 바나나임"])],
         els=[E("2대째", 600, 90, 150, "big", (("pop", "0.2", .45),), "--r:-8deg")],
         sfx=[("thump", "0.2", .6)]),
    dict(img="02.jpg", kb="panl",
         lines=[dict(tts="천구백오십년대까지 전 세계가 먹던 바나나는, 그로 미셸이라는 품종.",
                     chunks=["1950년대까지", "전 세계가 먹던 바나나는", "'그로 미셸'이라는 품종"])],
         els=[E("1950년대", 40, 40, 64, "tag", (("pop", "s", .4),)),
              E("Gros Michel<small>그로 미셸</small>", 300, 700, 100, "card", (("pop", "0.2", .45),), "--r:-3deg")],
         sfx=[("ding", "0.2")]),
    dict(img="03.jpg", kb="zoomout",
         lines=[dict(tts="지금 것보다 더 크고, 더 달고, 향도 진했다고 함.",
                     chunks=["지금 것보다 더 크고", "더 달고", "향도 진했다고 함"])],
         els=[E("더 큼", 60, 60, 90, "bubble", (("pop", "0.0", .4),), "--r:-5deg"),
              E("더 달콤", 700, 110, 90, "bubble", (("pop", "0.1", .4),), "--r:5deg"),
              E("향 진함", 380, 720, 90, "bubble", (("pop", "0.2", .4),), "--r:-3deg")],
         sfx=[("pop", "0.0"), ("pop", "0.1"), ("pop", "0.2")]),
    dict(img="04.jpg", kb="zoomin",
         lines=[dict(tts="그런데 파나마병이라는 곰팡이 병이 돌면서, 농장이 줄줄이 초토화됨.",
                     chunks=["그런데 '파나마병'이라는", "곰팡이 병이 돌면서", "농장이 줄줄이", "초토화됨"])],
         els=[RING(330, 260, 420, "0.1", "#ff1744"),
              ARROW(90, 330, "0.1+.2", 0, 230),
              E("초토화", 300, 60, 170, "stamp", (("stamp", "0.3", .3),))],
         sfx=[("buzz", "0.3")]),
    dict(img="05.jpg", kb="panr",
         lines=[dict(tts="바나나는 씨 없이 줄기를 잘라 심는 복제품이라, 한 그루가 걸리면 전부 약했던 거임.",
                     chunks=["바나나는 씨 없이", "줄기를 잘라 심는", "복제품이라", "한 그루가 걸리면", "전부 약했던 거임"])],
         els=[E("전부 복제품", 250, 60, 110, "card", (("pop", "0.2", .45),), "--r:-3deg;color:#c62828"),
              ARROW(740, 330, "0.3", 150, 220)],
         sfx=[("ding", "0.2"), ("buzz", "0.4")]),
    dict(img="06.jpg", kb="zoomout",
         lines=[dict(tts="그래서 병에 강한 캐번디시로 갈아탄 게, 지금의 바나나.",
                     chunks=["그래서 병에 강한", "'캐번디시'로 갈아탄 게", "지금의 바나나"])],
         els=[E("Cavendish<small>캐번디시</small>", 290, 60, 100, "card", (("pop", "0.1", .45),), "--r:3deg"),
              E("✅", 820, 700, 170, anims=(("pop", "0.2", .4),))],
         sfx=[("whoosh", "0.1"), ("sparkle", "0.2")]),
    dict(img="07.jpg", kb="zoomin",
         lines=[dict(tts="바나나맛 사탕이 진짜 바나나랑 맛이 다른 이유가, 옛날 그로 미셸 맛이라서라는 말도 있음.",
                     chunks=["바나나맛 사탕이", "진짜 바나나랑 맛이 다른 이유가", "옛날 그로 미셸 맛이라서", "라는 말도 있음"])],
         els=[RING(80, 330, 380, "0.1"),
              E("그로 미셸 맛?", 470, 80, 100, "bubble", (("pop", "0.2", .45),), "--r:4deg")],
         sfx=[("pop", "0.1"), ("ding", "0.2")]),
    dict(img="08.jpg", kb="zoomin",
         lines=[dict(tts="근데 지금 캐번디시도, 신종 파나마병에 위협받는 중임.",
                     chunks=["근데 지금 캐번디시도", "신종 파나마병에", "위협받는 중임"])],
         els=[E("⚠️", 60, 50, 190, anims=(("pop", "0.1", .4), ("pulse", "0.1+.4", .6))),
              E("2대째도 위험", 290, 700, 120, "stamp", (("stamp", "0.2", .3),))],
         sfx=[("alarm", "0.1"), ("thump", "0.2", .6)]),
]
