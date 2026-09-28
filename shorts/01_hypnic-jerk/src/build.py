# -*- coding: utf-8 -*-
"""Build a finished 9:16 short: TTS -> timing -> SFX/BGM mix -> HTML motion graphics -> frames -> mp4."""
import glob, json, os, re, shutil, subprocess, sys, wave
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from script import SCENES, TITLE  # noqa: E402

SR = 44100
FPS = 30
W, H = 1080, 1920
OUT = os.path.join(HERE, "out")
FFMPEG = __import__("imageio_ffmpeg").get_ffmpeg_exe()
os.makedirs(OUT, exist_ok=True)


# ---------------------------------------------------------------- TTS + timing
def tts(text, path):
    subprocess.run(["espeak-ng", "-v", "ko", "-s", "200", "-p", "42", "-a", "180", "-w", path, text], check=True)
    with wave.open(path) as w:
        sr = w.getframerate()
        x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    # trim leading/trailing silence
    idx = np.where(np.abs(x) > 0.02)[0]
    x = x[max(idx[0] - 200, 0): idx[-1] + 400]
    # resample to SR
    n = int(len(x) * SR / sr)
    x = np.interp(np.linspace(0, len(x) - 1, n), np.arange(len(x)), x)
    return x


def weight(s):
    return max(len(re.sub(r"[\s'\"!?,.]", "", s)), 1)


t = 0.25
cues, subs, scene_times, voice_clips = {}, [], [], []
for s in SCENES:
    s_start = t
    for li, line in enumerate(s["lines"]):
        clip = tts(line["tts"], os.path.join(OUT, f"{s['id']}_{li}.wav"))
        d = len(clip) / SR
        voice_clips.append((t, clip))
        tot = sum(weight(c) for c in line["chunks"])
        ct = t
        for ci, c in enumerate(line["chunks"]):
            cd = d * weight(c) / tot
            cues[f"{s['id']}.{li}.{ci}"] = round(ct, 3)
            subs.append([round(ct, 3), round(ct + cd, 3), c])
            ct += cd
        t += d + 0.12
    t += 0.18
    scene_times.append((s["id"], round(s_start, 3), round(t, 3)))
TOTAL = round(t + 0.6, 3)
# hold each subtitle until the next one starts
for i in range(len(subs) - 1):
    subs[i][1] = subs[i + 1][0]
subs[-1][1] = TOTAL
scene_times[-1] = (scene_times[-1][0], scene_times[-1][1], TOTAL)
json.dump(dict(cues=cues, subs=subs, scenes=scene_times, total=TOTAL), open(os.path.join(OUT, "timeline.json"), "w"), ensure_ascii=False, indent=1)
print("total", TOTAL)


# ---------------------------------------------------------------- audio
N = int(TOTAL * SR)
mix = np.zeros(N, np.float32)


def put(x, at, gain=1.0):
    i = int(at * SR)
    x = x[: max(N - i, 0)]
    mix[i: i + len(x)] += x * gain


def env(n, a=0.005, r=None):
    e = np.ones(n)
    ai = max(int(a * SR), 1)
    e[:ai] = np.linspace(0, 1, ai)
    return e * (np.exp(-np.linspace(0, r, n)) if r else 1)


rng = np.random.default_rng(7)


def thump():
    n = int(0.45 * SR); tt = np.arange(n) / SR
    f = 110 * np.exp(-tt * 9) + 38
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 7)
    click = rng.standard_normal(n) * np.exp(-tt * 80) * 0.4
    return (body + click) * 0.9


def whoosh():
    n = int(0.4 * SR)
    noise = rng.standard_normal(n)
    k = np.ones(40) / 40
    noise = np.convolve(noise, k, "same") * 3
    return noise * np.sin(np.linspace(0, np.pi, n)) ** 2 * 0.25


def pop():
    n = int(0.09 * SR); tt = np.arange(n) / SR
    f = np.linspace(700, 1400, n)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 40) * 0.35


def zap():
    n = int(0.5 * SR); tt = np.arange(n) / SR
    f = 180 + 120 * rng.standard_normal(n).cumsum() / np.sqrt(np.arange(1, n + 1))
    saw = 2 * ((np.cumsum(f) / SR) % 1) - 1
    return saw * (0.5 + 0.5 * (rng.random(n) > 0.3)) * np.exp(-tt * 5) * 0.3


def beep(freq, dur=0.14):
    n = int(dur * SR); tt = np.arange(n) / SR
    return np.sign(np.sin(2 * np.pi * freq * tt)) * env(n, 0.003) * np.exp(-tt * 6) * 0.08


# BGM: soft mysterious pad + pluck arpeggio (Am - F - C - G), low in the mix
bpm = 104; beat = 60 / bpm
chords = [[220, 261.6, 329.6], [174.6, 220, 261.6], [130.8, 196, 261.6], [196, 246.9, 293.7]]
tt = np.arange(N) / SR
pad = np.zeros(N)
bar = beat * 4
for bi in range(int(TOTAL / bar) + 1):
    ch = chords[bi % 4]
    a, b = int(bi * bar * SR), min(int((bi + 1) * bar * SR), N)
    seg = tt[a:b] - bi * bar
    for f in ch:
        pad[a:b] += np.sin(2 * np.pi * f * seg) * 0.05 + np.sin(2 * np.pi * f * 2.003 * seg) * 0.015
    # pluck arpeggio on 8ths
    for k in range(8):
        f = ch[k % 3] * 2
        s0 = a + int(k * beat / 2 * SR)
        n = int(0.3 * SR)
        if s0 >= N:
            break
        ts = np.arange(min(n, N - s0)) / SR
        pad[s0: s0 + len(ts)] += np.sin(2 * np.pi * f * ts) * np.exp(-ts * 12) * 0.05
pad *= 0.55 * np.clip(tt / 1.0, 0, 1) * np.clip((TOTAL - tt) / 1.2, 0, 1)
mix += pad.astype(np.float32)

for sid, s0, s1 in scene_times[1:]:
    put(whoosh(), s0 - 0.12)
put(thump(), cues["bed.0.2"], 1.0)
put(thump(), cues["ending.0.1"], 0.8)
for i in range(4):
    put(pop(), cues["stats.0.3"] + i * 0.12)
put(pop(), cues["brain.0.1"])
for i in range(6):
    put(beep(880 if i % 2 == 0 else 660), cues["alarm.0.1"] + i * 0.22 - 0.3)
put(zap(), cues["zap.0.1"])
put(thump(), cues["zap.0.2"], 0.7)
put(whoosh() * 1.5, cues["monkey.1.0"] + 0.3)
put(thump(), cues["monkey.1.1"], 0.6)
for k in ("triggers.0.0", "triggers.0.1", "triggers.0.2"):
    put(pop(), cues[k])
put(pop(), cues["ending.0.3"])

bed = mix.copy()
for at, clip in voice_clips:
    put(clip, at, 0.95)
peak = max(np.abs(mix).max(), 1e-6) / 0.89
for name, track in (("audio.wav", mix / peak), ("audio_novoice.wav", bed / peak)):
    with wave.open(os.path.join(OUT, name), "w") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((track * 32767).astype(np.int16).tobytes())


# ---------------------------------------------------------------- HTML
def c(k):
    return cues[k]


def A(name, at, dur, ease="cubic-bezier(.2,1.4,.4,1)", it="1", fill="both"):
    return f"{name} {dur}s {ease} {at:.3f}s {it} normal {fill}"


def anim(*parts):
    return "animation:" + ",".join(parts) + ";"


ST = {sid: (s0, s1) for sid, s0, s1 in scene_times}
fonts = os.path.join(HERE, "fonts")

scene_html = {}
s0 = ST["bed"][0]
scene_html["bed"] = f"""
<div class="bg" style="background:radial-gradient(circle at 50% 30%,#2b3a7a,#0b1030 70%)"></div>
<div class="e" style="left:820px;top:90px;font-size:150px;{anim(A('pop',s0,.5))}">🌙</div>
<div class="cam" style="{anim(A('slowzoom',s0,ST['bed'][1]-s0,'linear'))}">
 <div class="shakewrap" style="{anim(A('shake',c('bed.0.2'),.5,'linear'))}">
  <div class="bedframe"></div><div class="mattress"></div><div class="pillow"></div><div class="blanket"></div>
  <div class="e" style="left:250px;top:470px;font-size:190px;{anim(A('hideAt',c('bed.0.2'),.01,'steps(1)'))}">😴</div>
  <div class="e" style="left:250px;top:450px;font-size:190px;{anim(A('showAt',c('bed.0.2'),.01,'steps(1)'))}">😳</div>
  <div class="zzz" style="left:420px;top:420px;{anim(A('zfloat',s0,1.4,'ease-out','2'))}">Z</div>
  <div class="zzz" style="left:480px;top:380px;font-size:80px;{anim(A('zfloat',s0+.5,1.4,'ease-out','2'))}">z</div>
 </div>
</div>
<div class="flash" style="{anim(A('flash',c('bed.0.2'),.35,'ease-out',fill='forwards'))}"></div>
<div class="comic" style="left:560px;top:250px;{anim(A('popHold',c('bed.0.2'),.5))}">툭!</div>
<div class="e" style="left:700px;top:560px;font-size:160px;{anim(A('pop',c('bed.1.0'),.5))}">❓</div>
"""

s0 = ST["stats"][0]
people = ""
for i in range(10):
    x = 75 + (i % 5) * 190; y = 420 + (i // 5) * 225
    hi = f"{anim(A('pop',s0+.1+i*.05,.4), A('redden',c('stats.0.3')+min(i,6)*.07,.3,'ease-out'))}" if i < 7 else anim(A('pop', s0 + .1 + i * .05, .4))
    people += f'<div class="person" style="left:{x}px;top:{y}px;{hi}">🧍</div>'
scene_html["stats"] = f"""
<div class="bg" style="background:#4fc3f7"></div>
<div class="card" style="left:190px;top:30px;width:700px;{anim(A('pop',s0,.5))}">입면 경련<small>Hypnic Jerk</small></div>
{people}
<div class="big" style="left:0;width:1080px;top:235px;color:#ff2d2d;{anim(A('popHold',c('stats.0.3'),.5))}">10명 중 7명</div>
"""

s0 = ST["brain"][0]
scene_html["brain"] = f"""
<div class="bg" style="background:radial-gradient(circle,#6a2c91,#1c0930 75%)"></div>
<div class="e" style="left:290px;top:260px;font-size:480px;{anim(A('pop',s0,.5), A('pulse',s0+.5,.8,'ease-in-out','infinite'))}">🧠</div>
<div class="e" style="left:120px;top:180px;font-size:150px;{anim(A('pop',s0+.2,.4))}">❓</div>
<div class="e" style="left:800px;top:240px;font-size:120px;{anim(A('pop',s0+.35,.4))}">❓</div>
<div class="stamp" style="left:300px;top:700px;{anim(A('stamp',c('brain.0.1'),.35,'ease-out'))}">착각</div>
"""

s0 = ST["relax"][0]
scene_html["relax"] = f"""
<div class="bg" style="background:linear-gradient(#26a69a,#00695c)"></div>
<div class="e" style="left:330px;top:250px;font-size:400px;transform-origin:50% 100%;{anim(A('pop',s0,.5), A('droop',c('relax.0.2'),.9,'ease-in'))}">💪</div>
<div class="gauge" style="left:140px;top:120px;{anim(A('pop',s0+.1,.4))}">
  <div class="glabel">근육 긴장도</div><div class="gbar"><div class="gfill" style="{anim(A('drain',c('relax.0.1'),1.4,'ease-in'))}"></div></div>
</div>
<div class="e" style="left:760px;top:720px;font-size:130px;{anim(A('pop',c('relax.0.2')+.4,.4))}">😪</div>
"""

s0 = ST["alarm"][0]
scene_html["alarm"] = f"""
<div class="bg" style="background:#1a0000"></div>
<div class="bg" style="background:#d50000;{anim(A('blink',s0,.44,'steps(1)','infinite'))}"></div>
<div class="e" style="left:40px;top:40px;font-size:150px;{anim(A('pop',s0,.4))}">🚨</div>
<div class="e" style="left:890px;top:40px;font-size:150px;{anim(A('pop',s0+.1,.4))}">🚨</div>
<div class="e" style="left:70px;top:260px;font-size:230px;{anim(A('pop',s0+.1,.4))}">🧠</div>
<div class="bubble" style="left:330px;top:230px;{anim(A('popHold',c('alarm.0.1'),.4))}">추락 중!!!</div>
<div class="speed" style="left:470px;top:520px"></div><div class="speed" style="left:560px;top:480px"></div><div class="speed" style="left:650px;top:540px"></div>
<div class="e" style="left:430px;top:560px;font-size:260px;{anim(A('tumble',s0,1.1,'linear','infinite'))}">🧍</div>
"""

s0 = ST["zap"][0]
bolts = "".join(
    f'<div class="e" style="left:{470+dx}px;top:360px;font-size:120px;{anim(A("travel",c("zap.0.1")+k*.18,.7,"ease-in","2"))}">⚡</div>'
    for k, dx in enumerate((-90, 0, 90)))
scene_html["zap"] = f"""
<div class="bg" style="background:linear-gradient(#ffd54f,#ff8f00)"></div>
<div class="e" style="left:390px;top:40px;font-size:280px;{anim(A('pop',s0,.5))}">🧠</div>
<div class="tag" style="left:330px;top:330px;{anim(A('pop',c('zap.0.1'),.4))}">긴급 신호 발송</div>
{bolts}
<div class="shakewrap" style="{anim(A('shake',c('zap.0.2'),.5,'linear'))}">
  <div class="e" style="left:330px;top:690px;font-size:330px;{anim(A('pop',s0+.2,.5), A('jump',c('zap.0.2'),.45,'ease-out'))}">🛌</div>
</div>
<div class="comic" style="left:600px;top:560px;{anim(A('popHold',c('zap.0.2'),.45))}">움찔!</div>
"""

s0 = ST["monkey"][0]
scene_html["monkey"] = f"""
<div class="bg" style="background:linear-gradient(#81c784,#1b5e20)"></div>
<div class="e" style="left:80px;top:40px;font-size:880px;opacity:.95">🌳</div>
<div class="branch"></div>
<div class="e" style="left:560px;top:270px;font-size:220px;{anim(A('pop',s0,.5), A('fall',c('monkey.1.0')+.3,.8,'ease-in'))}">🐒</div>
<div class="zzz" style="left:760px;top:250px;{anim(A('zfloat',s0+.3,1.4,'ease-out','3'))}">Z</div>
<div class="tag" style="left:90px;top:40px;{anim(A('pop',c('monkey.0.2'),.4))}">가설: 원숭이 조상의 흔적</div>
<div class="xmark" style="{anim(A('stamp',c('monkey.1.1'),.35,'ease-out'))}">✕</div>
"""

s0 = ST["triggers"][0]
cards = ""
for k, (emo, label) in enumerate((("☕", "커피"), ("😫", "스트레스"), ("🥱", "피로"))):
    cards += f'<div class="tcard" style="left:{50+k*335}px;top:260px;{anim(A("pop",c(f"triggers.0.{k}"),.45))}"><span>{emo}</span>{label}</div>'
scene_html["triggers"] = f"""
<div class="bg" style="background:#ffe0b2"></div>
<div class="card" style="left:190px;top:80px;width:700px;font-size:78px;{anim(A('pop',s0,.4))}">이런 날 더 자주!</div>
{cards}
<div class="big" style="left:0;width:1080px;top:700px;color:#d50000;{anim(A('popHold',c('triggers.0.3'),.5))}">⬆ 발생 빈도 UP</div>
"""

s0 = ST["ending"][0]
scene_html["ending"] = f"""
<div class="bg" style="background:radial-gradient(circle at 50% 30%,#2b3a7a,#0b1030 70%)"></div>
<div class="shakewrap" style="{anim(A('shake',c('ending.0.1'),.45,'linear'))}">
  <div class="bedframe"></div><div class="mattress"></div><div class="pillow"></div><div class="blanket"></div>
  <div class="e" style="left:250px;top:470px;font-size:190px">😴</div>
</div>
<div class="e" style="left:600px;top:130px;font-size:260px;{anim(A('pop',c('ending.0.2'),.5), A('pulse',c('ending.0.2')+.5,.8,'ease-in-out','infinite'))}">🧠</div>
<div class="e" style="left:540px;top:330px;font-size:150px;{anim(A('pop',c('ending.0.2')+.2,.5))}">🛡️</div>
<div class="e" style="left:130px;top:150px;font-size:200px;{anim(A('popHold',c('ending.0.3'),.5), A('pulse',c('ending.0.3')+.5,.6,'ease-in-out','infinite'))}">❤️</div>
<div class="comic" style="left:560px;top:620px;font-size:150px;{anim(A('popHold',c('ending.0.1'),.45))}">툭!</div>
"""

scenes_div = "".join(
    f'<div class="scene" data-s="{s0}" data-e="{s1}"><div class="scin" style="{anim(A("sceneIn",s0,.35,"cubic-bezier(.2,.9,.3,1)"))}">{scene_html[sid]}</div></div>'
    for sid, s0, s1 in scene_times)

html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:BHS;src:url('file://{fonts}/BlackHanSans.ttf')}}
@font-face{{font-family:NSK;src:url('file://{fonts}/NotoSansKR.ttf');font-weight:900}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:{W}px;height:{H}px;background:#000;overflow:hidden;font-family:NSK,'Noto Color Emoji',sans-serif}}
.title{{position:absolute;left:0;top:70px;width:100%;text-align:center;font-family:BHS,'Noto Color Emoji';font-size:112px;line-height:1.16;letter-spacing:-1px}}
.title .l1{{color:#fff}} .title .l2{{color:#ff2020}}
.stage{{position:absolute;left:0;top:420px;width:1080px;height:1080px;overflow:hidden}}
.scene{{position:absolute;inset:0;opacity:0}}
.scin,.cam,.shakewrap{{position:absolute;inset:0}}
.bg{{position:absolute;inset:0}}
.e{{position:absolute;font-family:'Noto Color Emoji';line-height:1}}
.sub{{position:absolute;left:50%;top:1330px;transform:translateX(-50%);background:#000;color:#fff;font-weight:900;font-size:62px;padding:10px 34px 16px;border-radius:14px;white-space:nowrap;letter-spacing:-1px}}
.sub.em{{color:#ffe600;font-size:84px}}
.progress{{position:absolute;left:0;top:1500px;height:10px;background:#ff2020}}
.bedframe{{position:absolute;left:130px;top:640px;width:820px;height:230px;background:#6d4c41;border-radius:20px}}
.mattress{{position:absolute;left:150px;top:590px;width:780px;height:90px;background:#eceff1;border-radius:24px}}
.pillow{{position:absolute;left:190px;top:545px;width:260px;height:95px;background:#fff;border-radius:50px}}
.blanket{{position:absolute;left:430px;top:560px;width:520px;height:150px;background:#3f51b5;border-radius:30px 30px 20px 20px}}
.zzz{{position:absolute;font-family:BHS;font-size:110px;color:#bbdefb}}
.flash{{position:absolute;inset:0;background:#fff;opacity:0}}
.comic{{position:absolute;font-family:BHS;font-size:190px;color:#ffe600;-webkit-text-stroke:10px #000;paint-order:stroke fill;transform:rotate(-8deg)}}
.card{{position:absolute;background:#fff;color:#111;border-radius:28px;text-align:center;font-family:BHS;font-size:110px;padding:18px 0 22px;box-shadow:0 12px 0 rgba(0,0,0,.25)}}
.card small{{display:block;font-family:NSK;font-weight:900;font-size:40px;color:#666;margin-top:-6px}}
.person{{position:absolute;width:170px;height:220px;font-family:'Noto Color Emoji';font-size:170px;text-align:center;line-height:220px;border-radius:30px}}
.big{{position:absolute;text-align:center;font-family:BHS;font-size:150px;-webkit-text-stroke:12px #fff;paint-order:stroke fill}}
.stamp{{position:absolute;font-family:BHS;font-size:200px;color:#ff1744;border:14px solid #ff1744;border-radius:24px;padding:0 40px;transform:rotate(-10deg);background:rgba(255,255,255,.9)}}
.gauge{{position:absolute;width:800px}}
.glabel{{font-family:BHS;font-size:70px;color:#fff;margin-bottom:10px}}
.gbar{{height:70px;background:rgba(0,0,0,.35);border-radius:35px;overflow:hidden;border:6px solid #fff}}
.gfill{{height:100%;width:100%;background:#ff5252}}
.bubble{{position:absolute;background:#fff;color:#d50000;font-family:BHS;font-size:120px;padding:10px 40px;border-radius:40px}}
.speed{{position:absolute;width:14px;height:200px;background:rgba(255,255,255,.6);border-radius:7px;{anim(A('speed',0,.4,'linear','infinite'))}}}
.tag{{position:absolute;background:#000;color:#fff;font-weight:900;font-size:54px;padding:10px 28px;border-radius:16px}}
.branch{{position:absolute;left:470px;top:470px;width:520px;height:40px;background:#5d4037;border-radius:20px;transform:rotate(-6deg)}}
.xmark{{position:absolute;left:340px;top:420px;font-family:BHS;font-size:400px;color:#ff1744;-webkit-text-stroke:14px #fff;paint-order:stroke fill;line-height:1}}
.tcard{{position:absolute;width:300px;height:400px;background:#fff;border-radius:30px;text-align:center;font-family:BHS;font-size:74px;color:#222;box-shadow:0 12px 0 rgba(0,0,0,.2);padding-top:40px}}
.tcard span{{display:block;font-family:'Noto Color Emoji';font-size:180px;line-height:1.3}}
@keyframes pop{{0%{{transform:scale(0);opacity:0}}100%{{transform:scale(1);opacity:1}}}}
@keyframes popHold{{0%{{transform:scale(0) rotate(-8deg);opacity:0}}100%{{transform:scale(1) rotate(-8deg);opacity:1}}}}
@keyframes sceneIn{{0%{{transform:scale(1.15);opacity:0}}100%{{transform:scale(1);opacity:1}}}}
@keyframes slowzoom{{0%{{transform:scale(1)}}100%{{transform:scale(1.1)}}}}
@keyframes shake{{0%,100%{{transform:translate(0,0)}}10%{{transform:translate(-30px,20px)}}25%{{transform:translate(28px,-24px)}}40%{{transform:translate(-20px,-10px)}}60%{{transform:translate(16px,14px)}}80%{{transform:translate(-8px,6px)}}}}
@keyframes flash{{0%{{opacity:.9}}100%{{opacity:0}}}}
@keyframes hideAt{{0%{{opacity:1}}100%{{opacity:0}}}}
@keyframes showAt{{0%{{opacity:0}}100%{{opacity:1}}}}
@keyframes zfloat{{0%{{transform:translate(0,0) scale(.5);opacity:0}}30%{{opacity:1}}100%{{transform:translate(60px,-220px) scale(1.2);opacity:0}}}}
@keyframes redden{{0%{{background:transparent}}100%{{background:#ff2d2d;box-shadow:0 0 0 8px #fff}}}}
@keyframes pulse{{0%,100%{{transform:scale(1)}}50%{{transform:scale(1.07)}}}}
@keyframes stamp{{0%{{transform:scale(3) rotate(-10deg);opacity:0}}100%{{transform:scale(1) rotate(-10deg);opacity:1}}}}
@keyframes droop{{0%{{transform:scaleY(1) rotate(0)}}100%{{transform:scaleY(.55) rotate(25deg);filter:saturate(.3)}}}}
@keyframes drain{{0%{{width:100%}}100%{{width:6%}}}}
@keyframes blink{{0%{{opacity:.55}}50%{{opacity:0}}}}
@keyframes tumble{{0%{{transform:translateY(-120px) rotate(0)}}100%{{transform:translateY(120px) rotate(360deg)}}}}
@keyframes speed{{0%{{transform:translateY(-300px);opacity:0}}50%{{opacity:1}}100%{{transform:translateY(500px);opacity:0}}}}
@keyframes travel{{0%{{transform:translateY(0) scale(.6);opacity:0}}20%{{opacity:1}}100%{{transform:translateY(420px) scale(1.1);opacity:0}}}}
@keyframes jump{{0%{{transform:translateY(0)}}35%{{transform:translateY(-110px) rotate(-6deg)}}100%{{transform:translateY(0)}}}}
@keyframes fall{{0%{{transform:translateY(0) rotate(0)}}100%{{transform:translateY(900px) rotate(200deg)}}}}
</style></head><body>
<div class="title"><div class="l1">{TITLE[0]}</div><div class="l2">{TITLE[1]}</div></div>
<div class="stage">{scenes_div}</div>
<div class="sub" id="sub"></div>
<div class="progress" id="prog"></div>
<script>
const SUBS={json.dumps(subs, ensure_ascii=False)}, TOTAL={TOTAL};
const scenes=[...document.querySelectorAll('.scene')];
const sub=document.getElementById('sub'), prog=document.getElementById('prog');
function render(t){{
  for(const s of scenes) s.style.opacity=(t>=+s.dataset.s-0.001&&t<+s.dataset.e)?1:0;
  for(const a of document.getAnimations()){{a.pause();a.currentTime=t*1000;}}
  const cur=SUBS.find(x=>t>=x[0]&&t<x[1]);
  sub.style.display=cur?'block':'none';
  if(cur){{sub.textContent=cur[2];sub.className='sub'+(/!$/.test(cur[2])&&cur[2].length<5?' em':'');}}
  prog.style.width=(t/TOTAL*100)+'%';
}}
</script></body></html>"""
open(os.path.join(OUT, "short.html"), "w").write(html)

# ---------------------------------------------------------------- render frames
if "--no-render" in sys.argv:
    sys.exit()
from playwright.sync_api import sync_playwright  # noqa: E402

fdir = os.path.join(OUT, "frames")
shutil.rmtree(fdir, ignore_errors=True); os.makedirs(fdir)
exe = glob.glob("/opt/pw-browsers/chromium-1194/chrome-linux*/chrome")[0]
nframes = int(TOTAL * FPS)
only = [float(x) for x in os.environ.get("PREVIEW_T", "").split(",") if x]
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=exe)
    pg = b.new_page(viewport={"width": W, "height": H})
    pg.goto("file://" + os.path.join(OUT, "short.html"))
    pg.evaluate("document.fonts.ready")
    pg.wait_for_timeout(500)
    if only:
        for tt_ in only:
            pg.evaluate(f"render({tt_})")
            pg.screenshot(path=os.path.join(OUT, f"preview_{tt_:05.2f}.jpg"), type="jpeg", quality=85)
        sys.exit()
    for i in range(nframes):
        pg.evaluate(f"render({i / FPS})")
        pg.screenshot(path=os.path.join(fdir, f"f{i:05d}.jpg"), type="jpeg", quality=90)
        if i % 150 == 0:
            print("frame", i, "/", nframes, flush=True)
    b.close()

subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(fdir, "f%05d.jpg"),
                "-i", os.path.join(OUT, "audio.wav"), "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-ar", "44100", "-shortest",
                "-movflags", "+faststart", os.path.join(OUT, "short.mp4")], check=True)
print("done", os.path.join(OUT, "short.mp4"))
