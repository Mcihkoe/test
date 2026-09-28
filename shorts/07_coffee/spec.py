# -*- coding: utf-8 -*-
# Style: 애니메이션 (3D cartoon AI stills + Ken Burns motion) — it's a legend, so a storybook look fits
from engine import E, RING, ARROW

SERIES = "🍽️ 식재료 비하인드"
SEED = 7
ACCENT = "#ffab40"
TITLE = ["커피를 처음 발견한 건", "사람이 아니었다"]
YT_TITLE = "커피를 처음 발견한 게 염소라고? ㅋㅋ"
DESCRIPTION = """
매일 마시는 커피, 처음 발견한 건 춤추는 염소들이었다는 전설 ☕🐐
에티오피아 염소지기 칼디와 수도원의 '악마의 열매' 이야기!
"""
TAGS = ["커피", "커피유래", "칼디", "커피전설", "음식유래", "식재료", "잡학", "쇼츠", "shorts"]
THUMB_CUE = (2, "0.3")

IMAGES = {
    "01.jpg": "AaDmY-aehzTU-yq8cKaAIA", "02.jpg": "AaDmY-gP5gFWl3eaNOhx1g", "03.jpg": "AaDmY-mMfzvl_43C9DCw9w",
    "04.jpg": "AaDmY_A9SSTSP8eWG9bcUg", "05.jpg": "AaDmY_HYJ4zjrCoDj0Kjcg", "06.jpg": "AaDmY_OIBRvvyY1MwqxcAQ",
    "07.jpg": "AaDmY_UXFsFDD59br5f88Q",
}

SCENES = [
    dict(img="01.jpg", kb="zoomin",
         lines=[dict(tts="매일 마시는 커피, 처음 발견한 게 염소라는 전설이 있음.",
                     chunks=["매일 마시는 커피", "처음 발견한 게", "염소라는 전설이 있음"])],
         els=[E("🐐", 760, 620, 220, anims=(("pop", "0.2", .45), ("wiggle", "0.2+.45", .7))),
              E("염소?!", 90, 80, 150, "big", (("pop", "0.2", .45),), "--r:-8deg")],
         sfx=[("pop", "0.2"), ("ding", "0.2+.2")]),
    dict(img="02.jpg", kb="panr",
         lines=[dict(tts="옛날 에티오피아의 염소지기, 칼디.", chunks=["옛날 에티오피아의", "염소지기 '칼디'"])],
         els=[E("📍 에티오피아", 50, 50, 70, "tag", (("pop", "s+.2", .4),)),
              E("칼디", 700, 120, 110, "bubble", (("pop", "0.1", .45),), "--r:5deg")],
         sfx=[("pop", "0.1")]),
    dict(img="03.jpg", kb="zoomin",
         lines=[dict(tts="어느 날 염소들이 빨간 열매를 먹더니, 밤새 펄쩍펄쩍 춤을 추기 시작함.",
                     chunks=["어느 날 염소들이", "빨간 열매를 먹더니", "밤새 펄쩍펄쩍", "춤을 추기 시작함"])],
         els=[RING(640, 420, 300, "0.1", "#ff1744"),
              ARROW(420, 500, "0.1+.2", 0, 220),
              E("펄쩍!", 90, 80, 160, "comic", (("pop", "0.2", .35),), "--r:-10deg"),
              E("펄쩍!", 640, 110, 130, "comic", (("pop", "0.2+.35", .35),), "--r:8deg")],
         sfx=[("pop", "0.1"), ("thump", "0.2", .5), ("thump", "0.2+.35", .5), ("thump", "0.3", .4)]),
    dict(img="04.jpg", kb="panl",
         lines=[dict(tts="칼디가 열매를 수도원에 가져가자, 수도승은 악마의 열매라며 불에 던져버림.",
                     chunks=["칼디가 열매를", "수도원에 가져가자", "'악마의 열매'라며", "불에 던져버림"])],
         els=[E("악마의 열매!", 230, 60, 120, "bubble", (("pop", "0.2", .45),), "--r:-4deg;color:#c62828"),
              E("🔥", 820, 720, 170, anims=(("pop", "0.3", .4), ("pulse", "0.3+.4", .5)))],
         sfx=[("thump", "0.2", .5), ("whoosh", "0.3")]),
    dict(img="05.jpg", kb="zoomin",
         lines=[dict(tts="그런데 불 속에서, 엄청 고소한 향이 퍼짐.", chunks=["그런데 불 속에서", "엄청 고소한 향이 퍼짐"])],
         els=[E("고소~", 90, 90, 150, "comic", (("pop", "0.1", .45), ("bob", "0.1+.45", 1)), "--r:-6deg"),
              E("✨", 800, 90, 150, anims=(("pop", "0.1+.2", .4), ("pulse", "0.1+.6", .6)))],
         sfx=[("sparkle", "0.1")]),
    dict(img="06.jpg", kb="panr",
         lines=[dict(tts="볶은 열매를 물에 우려 마셨더니, 밤새 기도해도 졸리지 않았다는 거임.",
                     chunks=["볶은 열매를 물에 우려 마셨더니", "밤새 기도해도", "졸리지 않았다는 거임"])],
         els=[E("잠이 안 와!", 300, 60, 120, "bubble", (("pop", "0.2", .45),), "--r:3deg"),
              E("👀", 820, 700, 160, anims=(("pop", "0.2+.2", .4),))],
         sfx=[("ding", "0.2")]),
    dict(img="07.jpg", kb="zoomout",
         lines=[dict(tts="물론 전설이지만, 오늘 커피 마실 때 염소한테 고마워하면 됨.",
                     chunks=["물론 전설이지만", "오늘 커피 마실 때", "염소한테 고마워하면 됨"])],
         els=[E("※ 전설임", 60, 60, 64, "tag", (("pop", "0.0", .4),)),
              E("고마워 🐐", 560, 90, 110, "bubble", (("pop", "0.2", .45),), "--r:5deg")],
         sfx=[("sparkle", "0.2")]),
]
