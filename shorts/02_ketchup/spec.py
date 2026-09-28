# -*- coding: utf-8 -*-
from engine import E, BOX

SERIES = "🍽️ 식재료 비하인드"
SEED = 2
TITLE = ["케첩의 원래 정체", "알고 보니 생선?!"]
YT_TITLE = "케첩이 원래 생선 소스였다고? ㄷㄷ"
DESCRIPTION = """
감자튀김 필수템 케첩, 원래는 토마토가 아니라 생선 소스였다는 사실 🐟
중국 남부의 생선 발효 소스 → 영국의 버섯·호두 케첩 → 토마토 케첩이 되기까지!
"""
TAGS = ["케첩", "케첩유래", "음식유래", "식재료", "음식상식", "잡학", "쇼츠", "shorts"]
THUMB_CUE = (0, "0.3")  # scene index, cue -> cover frame


def bottle(x, y, s=1.0, anims=(("pop", "s", .45),)):
    return [BOX(x, y + 70 * s, 190 * s, 400 * s, "#e53935", 60 * s, anims),
            BOX(x + 45 * s, y, 100 * s, 90 * s, "#fafafa", 16 * s, anims),
            BOX(x + 20 * s, y + 200 * s, 150 * s, 110 * s, "#fff3e0", 14 * s, anims),
            E("🍅", x + 50 * s, y + 215 * s, 85 * s, anims=anims)]


def tcard(emoji, label, x, y, c):
    st = "width:300px;height:380px;background:#fff;border-radius:30px;text-align:center;font-family:BHS;font-size:74px;color:#222;box-shadow:0 12px 0 rgba(0,0,0,.2);padding-top:40px"
    return E(f'<span style="display:block;font-family:Noto Color Emoji;font-size:170px;line-height:1.3">{emoji}</span>{label}',
             x, y, 0, "box", (("pop", c, .45),), st)


SCENES = [
    dict(bg="radial-gradient(circle at 50% 40%,#ff8a65,#b71c1c 75%)",
         lines=[dict(tts="감자튀김에 찍어먹는 이 케첩, 원래는 토마토가 아니었음.",
                     chunks=["감자튀김에 찍어먹는", "이 케첩", "원래는 토마토가", "아니었음"])],
         els=[E("🍟", 90, 330, 330, anims=(("pop", "s", .45), ("bob", "s+.5", 1.2))),
              *bottle(600, 260, anims=(("pop", "0.1", .45),)),
              E("🍅", 390, 40, 200, anims=(("pop", "0.2", .45),)),
              E("✕", 395, -10, 300, "big", (("stamp", "0.3", .3),))],
         sfx=[("pop", "0.1"), ("pop", "0.2"), ("buzz", "0.3")]),
    dict(bg="linear-gradient(#0d47a1,#002171)",
         lines=[dict(tts="케첩의 조상은, 중국 남부와 동남아에서 먹던 생선 발효 소스, 케찹.",
                     chunks=["케첩의 조상은", "중국 남부와 동남아에서", "먹던 생선 발효 소스", "'케찹'"])],
         els=[E("🐟", 110, 230, 330, anims=(("pop", "s", .45), ("bob", "s+.5", 1.4))),
              E("🏺", 620, 300, 300, anims=(("pop", "0.2", .45),)),
              E("🫧", 700, 170, 110, anims=(("pop", "0.2+.3", .4), ("bob", "0.2+.7", 1))),
              E('鮭汁<small>케찹 · kê-tsiap</small>', 250, 620, 120, "card", (("pop", "0.3", .45),), "--r:-4deg")],
         sfx=[("pop", "0.2"), ("ding", "0.3")]),
    dict(bg="linear-gradient(#81d4fa 0%,#4fc3f7 55%,#0277bd 56%,#01579b 100%)",
         lines=[dict(tts="17세기 영국 선원들이 이 맛에 반해, 본국으로 가져갔는데,",
                     chunks=["17세기 영국 선원들이", "이 맛에 반해", "본국으로 가져갔는데"])],
         els=[E("😋", 90, 90, 170, anims=(("pop", "0.1", .45),)),
              E("🇬🇧", 800, 110, 170, anims=(("pop", "0.2", .45),)),
              E("⛵", 40, 300, 290, anims=(("pop", "s", .4), ("sail", "0.0", 2.6)))],
         sfx=[("pop", "0.1"), ("pop", "0.2")]),
    dict(bg="#ffe0b2",
         lines=[dict(tts="영국엔 그 재료가 없어서, 버섯, 호두, 굴로 흉내 내기 시작함.",
                     chunks=["영국엔 그 재료가 없어서", "버섯", "호두", "굴로 흉내 내기 시작함"])],
         els=[E("영국판 짝퉁 케첩", 170, 60, 88, "card", (("pop", "s", .45),)),
              tcard("🍄", "버섯", 50, 300, "0.1"), tcard("🌰", "호두", 390, 300, "0.2"), tcard("🦪", "굴", 730, 300, "0.3")],
         sfx=[("pop", "0.1"), ("pop", "0.2"), ("pop", "0.3")]),
    dict(bg="radial-gradient(circle,#c5e1a5,#558b2f 80%)",
         lines=[dict(tts="토마토가 들어간 건 천팔백년대 초.", chunks=["토마토가 들어간 건", "1800년대 초"]),
                dict(tts="심지어 천팔백삼십년대 미국에선, 토마토가 만병통치약 알약으로 팔리기도 했음.",
                     chunks=["심지어 1830년대 미국에선", "토마토가 만병통치약", "알약으로 팔리기도 했음"])],
         els=[E("🍅", 120, 170, 300, anims=(("dropIn", "s", .6), ("pulse", "s+.6", .9))),
              E("1800년대 초", 560, 120, 64, "tag", (("pop", "0.1", .4),)),
              E("💊", 560, 330, 240, anims=(("pop", "1.1", .45), ("wiggle", "1.1+.45", .5))),
              E("만병통치약?!", 420, 620, 110, "bubble", (("pop", "1.1+.2", .45),), "--r:-5deg;color:#c62828")],
         sfx=[("thump", "s+.5", .6), ("pop", "1.1"), ("sparkle", "1.2")]),
    dict(bg="linear-gradient(#fff176,#fbc02d)",
         lines=[dict(tts="그리고 천팔백칠십육년, 한 회사가 달달한 토마토 케첩을 대량으로 팔면서, 지금의 맛이 완성됨.",
                     chunks=["그리고 1876년", "한 회사가", "달달한 토마토 케첩을", "대량으로 팔면서", "지금의 맛이 완성됨"])],
         els=[E("🏭", 80, 90, 280, anims=(("pop", "s", .45),)),
              E("1876", 470, 150, 170, "big", (("pop", "0.0", .45),), "--r:-6deg"),
              *[b for i in range(4) for b in bottle(40 + i * 260, 450, .72, anims=(("flyL", f"0.3+{i * .12:.2f}", .5),))],
              E("😋", 830, 40, 180, anims=(("pop", "0.4", .45),))],
         sfx=[("pop", "0.0"), ("whoosh", "0.3"), ("sparkle", "0.4")]),
    dict(bg="radial-gradient(circle at 50% 40%,#ff8a65,#b71c1c 75%)",
         lines=[dict(tts="결국 케첩의 시작은, 생선 소스였던 거임.", chunks=["결국 케첩의 시작은", "생선 소스였던 거임"])],
         els=[*bottle(120, 230),
              E("=", 440, 330, 200, "comic", (("pop", "0.1", .4),)),
              E("🐟", 600, 330, 300, anims=(("pop", "0.1+.15", .45), ("bob", "0.1+.6", 1.1))),
              E("원조는 나야", 520, 120, 90, "bubble", (("pop", "0.1+.4", .45),), "--r:4deg")],
         sfx=[("pop", "0.1"), ("ding", "0.1+.4")]),
]
