# -*- coding: utf-8 -*-
# Style: 실사 (photoreal AI stills + Ken Burns motion)
from engine import E, RING, ARROW

SERIES = "🍽️ 식재료 비하인드"
SEED = 6
ACCENT = "#ff1744"
TITLE = ["한국인의 매운맛", "원래 수입품이었다"]
YT_TITLE = "고추가 원래 한국에 없었다고? ㄷㄷ"
DESCRIPTION = """
김치, 떡볶이, 찌개... 한국인의 매운맛을 책임지는 고추는 원래 한국에 없던 채소 🌶️
아메리카에서 출발해 조선까지 오게 된 과정과, 빨간 김치 이전의 김치 이야기!
"""
TAGS = ["고추", "고추유래", "김치", "백김치", "음식유래", "식재료", "역사", "잡학", "쇼츠", "shorts"]
THUMB_CUE = (0, "0.2")

IMAGES = {  # Canva media ids (None = not generated yet)
    "01.jpg": 'MAHWdeXXP3E',
    "02.jpg": 'MAHWde1BsLo',
    "03.jpg": 'MAHWdf8EwAE',
    "04.jpg": 'MAHWdTKuU1g',
    "05.jpg": 'MAHWdZHTiOI',
    "06.jpg": 'MAHWdQuxuvo',
    "07.jpg": 'MAHWdbWYfQw',
}

SCENES = [
    dict(img="01.jpg", kb="zoomin",
         lines=[dict(tts="한국인 하면 매운맛인데, 고추는 원래 한국에 없던 채소임.",
                     chunks=["한국인 하면 매운맛", "근데 고추는 원래", "한국에 없던 채소임"])],
         els=[E("수입품?!", 560, 70, 140, "big", (("pop", "0.2", .45),), "--r:-8deg")],
         sfx=[("thump", "0.2", .6)]),
    dict(img="02.jpg", kb="panl",
         lines=[dict(tts="고추의 고향은 아메리카 대륙. 수천 년 전부터 재배되던 작물.",
                     chunks=["고추의 고향은", "아메리카 대륙", "수천 년 전부터 재배되던 작물"])],
         els=[E("📍 아메리카 대륙", 250, 60, 80, "tag", (("pop", "0.1", .4),), "background:#c62828")],
         sfx=[("ding", "0.1")]),
    dict(img="03.jpg", kb="panr",
         lines=[dict(tts="콜럼버스가 유럽으로 가져간 뒤, 포르투갈 상인들의 뱃길을 타고 아시아까지 퍼짐.",
                     chunks=["콜럼버스가 유럽으로 가져간 뒤", "포르투갈 상인들의", "뱃길을 타고", "아시아까지 퍼짐"])],
         els=[E("아메리카 → 유럽 → 아시아", 130, 60, 70, "tag", (("pop", "0.1", .4),)),
              ARROW(420, 600, "0.2", 0, 240)],
         sfx=[("whoosh", "0.2")]),
    dict(img="04.jpg", kb="zoomin",
         lines=[dict(tts="조선에선 천육백년대 초 기록에 처음 등장하는데, 일본에서 건너온 독이 있는 풀이라고 적혀 있음.",
                     chunks=["조선에선 1600년대 초", "기록에 처음 등장하는데", "'일본에서 건너온", "독이 있는 풀'이라고 적혀 있음"])],
         els=[E("1614년 《지봉유설》", 50, 50, 64, "tag", (("pop", "0.1", .4),)),
              RING(760, 620, 280, "0.2", "#ff1744"),
              E("독초?!", 640, 150, 140, "stamp", (("stamp", "0.3", .3),))],
         sfx=[("ding", "0.1"), ("buzz", "0.3")]),
    dict(img="05.jpg", kb="zoomout",
         lines=[dict(tts="그럼 그 전 김치는? 고춧가루 없는 하얀 김치였음.",
                     chunks=["그럼 그 전 김치는?", "고춧가루 없는", "하얀 김치였음"])],
         els=[E("원조 김치 = 하얀색", 180, 60, 90, "card", (("pop", "0.2", .45),), "--r:-3deg")],
         sfx=[("sparkle", "0.2")]),
    dict(img="06.jpg", kb="panl",
         lines=[dict(tts="빨간 김치가 흔해진 건 천칠백년대 이후. 생각보다 얼마 안 됐음.",
                     chunks=["빨간 김치가 흔해진 건", "1700년대 이후", "생각보다 얼마 안 됐음"])],
         els=[E("1700년대~", 330, 60, 130, "big", (("pop", "0.1", .45),), "--r:-5deg")],
         sfx=[("pop", "0.1")]),
    dict(img="07.jpg", kb="zoomin",
         lines=[dict(tts="그런데 지금은, 1인당 고추 소비량 세계 최상위권으로 꼽히는 나라가 됨.",
                     chunks=["그런데 지금은", "1인당 고추 소비량", "세계 최상위권으로 꼽히는", "나라가 됨"])],
         els=[E("🌶️", 60, 60, 170, anims=(("pop", "0.1", .4), ("wiggle", "0.1+.4", .8))),
              E("세계 최상위권", 250, 700, 120, "stamp", (("stamp", "0.2", .3),), "color:#d50000;border-color:#d50000")],
         sfx=[("ding", "0.2")]),
]
