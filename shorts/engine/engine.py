# -*- coding: utf-8 -*-
"""Shorts engine: spec (script + scene visuals + SFX) -> TTS -> timing -> audio mix -> HTML motion graphics -> 9:16 mp4.

Usage:  python3 shorts/engine/engine.py shorts/02_ketchup            # full render
        python3 shorts/engine/engine.py shorts/02_ketchup --preview   # contact sheet only

A spec.py in the short's folder defines TITLE, YT_TITLE, DESCRIPTION, TAGS, THUMB_CUE, SCENES.
Each scene: dict(bg=css, lines=[dict(tts=..., chunks=[...])], els=[E(...)...], sfx=[(name, cue, gain)...]).
Cues are strings resolved per scene: "s" = scene start, "L.C" = line L chunk C, optional "+0.3" offset.
"""
import glob, importlib.util, json, os, re, shutil, subprocess, sys, tempfile, urllib.parse, wave
import numpy as np

ENGINE = os.path.dirname(os.path.abspath(__file__))
SR, FPS, W, H = 44100, 30, 1080, 1920
TEMPO = 1.28  # speed-up applied to the TTS voice (pitch preserved)
FFMPEG = __import__("imageio_ffmpeg").get_ffmpeg_exe()
FONTS = os.path.join(ENGINE, "fonts")
FONT_URLS = {"BlackHanSans.ttf": "Black+Han+Sans", "NotoSansKR.ttf": "Noto+Sans+KR:wght@900"}


def ensure_fonts():
    os.makedirs(FONTS, exist_ok=True)
    for fn, fam in FONT_URLS.items():
        p = os.path.join(FONTS, fn)
        if not os.path.exists(p):
            css = subprocess.run(["curl", "-sS", "-A", "Mozilla/4.0", f"https://fonts.googleapis.com/css2?family={fam}"],
                                 capture_output=True, text=True, check=True).stdout
            subprocess.run(["curl", "-sS", "-o", p, re.search(r"https://[^)]+", css).group(0)], check=True)


# ------------------------------------------------------------------ spec helpers (imported by spec.py)
def E(content, x, y, size=160, cls="e", anims=(("pop", "s", .45),), style=""):
    """One on-stage element. Stage is 1080x1080; x/y are its top-left. anims: (keyframes, cue, dur[, ease[, iter]])."""
    return dict(content=content, x=x, y=y, size=size, cls=cls, anims=list(anims), style=style)


def BOX(x, y, w, h, color, radius=20, anims=(), style=""):
    return E("", x, y, 0, "box", anims, f"width:{w}px;height:{h}px;background:{color};border-radius:{radius}px;{style}")


def TCARD(emoji, label, x, y, c, w=300, h=380):
    st = (f"width:{w}px;height:{h}px;background:#fff;border-radius:30px;text-align:center;font-family:BHS;font-size:70px;"
          "color:#222;box-shadow:0 12px 0 rgba(0,0,0,.2);padding-top:36px")
    return E(f'<span style="display:block;font-family:Noto Color Emoji;font-size:{int(w * .55)}px;line-height:1.3">{emoji}</span>{label}',
             x, y, 0, "box", (("pop", c, .45),), st)


def RING(x, y, d, c, color="#00e676"):
    """Highlight circle (benchmark-channel style)."""
    return E("", x, y, 0, "box", (("pop", c, .4),),
             f"width:{d}px;height:{d}px;border:14px solid {color};border-radius:50%;box-shadow:0 0 0 4px rgba(0,0,0,.35)")


def ARROW(x, y, c, rot=0, size=220, color="#ff1f1f"):
    """Red pointer arrow; rot=0 points right, 90 points down."""
    svg = (f'<svg width="{size}" height="{size}" viewBox="0 0 100 100" style="transform:rotate({rot}deg)">'
           f'<path d="M6 40 H58 V20 L96 50 L58 80 V60 H6 Z" fill="{color}" stroke="#fff" stroke-width="5" stroke-linejoin="round"/></svg>')
    return E(svg, x, y, 0, "box", (("pop", c, .4), ("nudge", c + "+.4", .6)), "")


# ------------------------------------------------------------------ TTS
def tts(text, cache_dir):
    key = re.sub(r"[^\w]", "", text)[:40] + f"_{abs(hash(text)) % 10**8}"
    mp3 = os.path.join(cache_dir, key + ".mp3")
    if not os.path.exists(mp3):
        q = urllib.parse.quote(text)
        subprocess.run(["curl", "-sS", "--retry", "4", "-o", mp3,
                        f"https://translate.googleapis.com/translate_tts?ie=UTF-8&client=gtx&tl=ko&q={q}"], check=True)
    wav = mp3[:-4] + ".wav"
    subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-i", mp3, "-af", f"atempo={TEMPO}", "-ar", str(SR), "-ac", "1", wav],
                   check=True)
    with wave.open(wav) as w:
        x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    idx = np.where(np.abs(x) > 0.015)[0]
    return x[max(idx[0] - 300, 0): idx[-1] + 600]


def weight(s):
    return max(len(re.sub(r"[\s'\"!?,.~]", "", s)), 1)


# ------------------------------------------------------------------ SFX / BGM synthesis
rng = np.random.default_rng(7)


def _sweep(f, n):
    return np.sin(2 * np.pi * np.cumsum(f) / SR)


def sfx(name):
    if name == "thump":
        n = int(.45 * SR); t = np.arange(n) / SR
        return (_sweep(110 * np.exp(-t * 9) + 38, n) * np.exp(-t * 7) + rng.standard_normal(n) * np.exp(-t * 80) * .4) * .9
    if name == "whoosh":
        n = int(.4 * SR)
        x = np.convolve(rng.standard_normal(n), np.ones(40) / 40, "same") * 3
        return x * np.sin(np.linspace(0, np.pi, n)) ** 2 * .25
    if name == "pop":
        n = int(.09 * SR); t = np.arange(n) / SR
        return _sweep(np.linspace(700, 1400, n), n) * np.exp(-t * 40) * .35
    if name == "ding":
        n = int(.8 * SR); t = np.arange(n) / SR
        return (np.sin(2 * np.pi * 1318 * t) + .5 * np.sin(2 * np.pi * 1976 * t)) * np.exp(-t * 5) * .22
    if name == "buzz":  # wrong-answer buzzer
        n = int(.45 * SR); t = np.arange(n) / SR
        return np.sign(np.sin(2 * np.pi * 140 * t)) * np.minimum(1, (.45 - t) * 20) * .12
    if name == "zap":
        n = int(.5 * SR); t = np.arange(n) / SR
        f = 180 + 120 * rng.standard_normal(n).cumsum() / np.sqrt(np.arange(1, n + 1))
        return (2 * ((np.cumsum(f) / SR) % 1) - 1) * (.5 + .5 * (rng.random(n) > .3)) * np.exp(-t * 5) * .3
    if name == "alarm":
        out = []
        for i in range(6):
            n = int(.2 * SR); t = np.arange(n) / SR
            out.append(np.sign(np.sin(2 * np.pi * (880 if i % 2 == 0 else 660) * t)) * np.exp(-t * 6) * .08)
        return np.concatenate(out)
    if name == "tick":
        out = np.zeros(int(1.2 * SR))
        for i in range(4):
            n = int(.03 * SR); t = np.arange(n) / SR; s = int(i * .3 * SR)
            out[s:s + n] += np.sin(2 * np.pi * 2000 * t) * np.exp(-t * 200) * .3
        return out
    if name == "chomp":
        n = int(.18 * SR); t = np.arange(n) / SR
        return np.convolve(rng.standard_normal(n), np.ones(8) / 8, "same") * np.exp(-t * 25) * .8
    if name == "sparkle":
        out = np.zeros(int(.9 * SR))
        for i, f in enumerate((1568, 2093, 2637, 3136)):
            n = int(.4 * SR); t = np.arange(n) / SR; s = int(i * .09 * SR)
            out[s:s + n] += np.sin(2 * np.pi * f * t) * np.exp(-t * 9) * .1
        return out
    raise KeyError(name)


def bgm(total, seed):
    r = np.random.default_rng(seed)
    progs = [[[220, 261.6, 329.6], [174.6, 220, 261.6], [130.8, 196, 261.6], [196, 246.9, 293.7]],
             [[261.6, 329.6, 392], [220, 261.6, 329.6], [174.6, 220, 261.6], [196, 246.9, 293.7]],
             [[196, 246.9, 293.7], [164.8, 196, 246.9], [130.8, 164.8, 196], [146.8, 185, 220]]]
    chords = progs[seed % len(progs)]
    beat = 60 / (108 + seed % 3 * 6)
    N = int(total * SR); tt = np.arange(N) / SR; out = np.zeros(N)
    bar = beat * 4
    for bi in range(int(total / bar) + 1):
        ch = chords[bi % 4]
        a, b = int(bi * bar * SR), min(int((bi + 1) * bar * SR), N)
        seg = tt[a:b] - bi * bar
        for f in ch:
            out[a:b] += np.sin(2 * np.pi * f * seg) * .045
        for k in range(8):
            s0 = a + int(k * beat / 2 * SR)
            if s0 >= N:
                break
            f = ch[(k * (1 + seed % 2)) % 3] * 2
            ts = np.arange(min(int(.28 * SR), N - s0)) / SR
            out[s0:s0 + len(ts)] += np.sin(2 * np.pi * f * ts) * np.exp(-ts * 12) * .05
        for k in range(4):  # soft kick on each beat
            s0 = a + int(k * beat * SR)
            if s0 >= N:
                break
            ts = np.arange(min(int(.15 * SR), N - s0)) / SR
            out[s0:s0 + len(ts)] += _sweep(90 * np.exp(-ts * 30) + 45, len(ts)) * np.exp(-ts * 25) * .09
    return out * np.clip(tt / 1.0, 0, 1) * np.clip((total - tt) / 1.2, 0, 1) * .6


# ------------------------------------------------------------------ CSS
CSS = """
@font-face{font-family:BHS;src:url('file://%(fonts)s/BlackHanSans.ttf')}
@font-face{font-family:NSK;src:url('file://%(fonts)s/NotoSansKR.ttf');font-weight:900}
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1920px;background:#000;overflow:hidden;font-family:NSK,'Noto Color Emoji',sans-serif}
.title{position:absolute;left:0;top:70px;width:100%;text-align:center;font-family:BHS,'Noto Color Emoji';font-size:112px;line-height:1.16;letter-spacing:-1px}
.title .l1{color:#fff}.title .l2{color:%(accent)s}
.stage{position:absolute;left:0;top:420px;width:1080px;height:1080px;overflow:hidden}
.scene{position:absolute;inset:0;opacity:0}.scin,.bg{position:absolute;inset:0}
.x{position:absolute;line-height:1;white-space:nowrap}
.e{font-family:'Noto Color Emoji'}
.sub{position:absolute;left:50%;top:1330px;transform:translateX(-50%);background:#000;color:#fff;font-weight:900;font-size:62px;padding:10px 34px 16px;border-radius:14px;white-space:nowrap;letter-spacing:-1px}
.sub.em{color:#ffe600;font-size:80px}
.progress{position:absolute;left:0;top:1500px;height:10px;background:%(accent)s}
.series{position:absolute;left:0;top:1560px;width:100%;text-align:center;color:#888;font-weight:900;font-size:40px;letter-spacing:2px}
.comic{font-family:BHS;color:#ffe600;-webkit-text-stroke:10px #000;paint-order:stroke fill}
.big{font-family:BHS;-webkit-text-stroke:12px #fff;paint-order:stroke fill;color:#ff2020}
.card{background:#fff;color:#111;border-radius:28px;text-align:center;font-family:BHS;padding:18px 40px 22px;box-shadow:0 12px 0 rgba(0,0,0,.25)}
.card small{display:block;font-family:NSK;font-weight:900;font-size:.4em;color:#666}
.stamp{font-family:BHS;color:#ff1744;border:14px solid #ff1744;border-radius:24px;padding:0 40px;background:rgba(255,255,255,.92)}
.tag{background:#000;color:#fff;font-weight:900;padding:10px 28px;border-radius:16px}
.bubble{background:#fff;color:#111;font-family:BHS;padding:14px 40px;border-radius:40px;box-shadow:0 10px 0 rgba(0,0,0,.2)}
.label{font-family:BHS;color:#fff;-webkit-text-stroke:10px #000;paint-order:stroke fill}
@keyframes pop{0%{transform:scale(0) rotate(var(--r,0deg));opacity:0}100%{transform:scale(1) rotate(var(--r,0deg));opacity:1}}
@keyframes out{0%{opacity:1;transform:scale(1) rotate(var(--r,0deg))}100%{opacity:0;transform:scale(0) rotate(var(--r,0deg))}}
@keyframes show{0%{opacity:0}100%{opacity:1}}
@keyframes hide{0%{opacity:1}100%{opacity:0}}
@keyframes stamp{0%{transform:scale(3) rotate(-10deg);opacity:0}100%{transform:scale(1) rotate(-10deg);opacity:1}}
@keyframes sceneIn{0%{transform:scale(1.15);opacity:0}100%{transform:scale(1);opacity:1}}
@keyframes pulse{0%,100%{transform:scale(1) rotate(var(--r,0deg))}50%{transform:scale(1.08) rotate(var(--r,0deg))}}
@keyframes bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-24px)}}
@keyframes wiggle{0%,100%{transform:rotate(-8deg)}50%{transform:rotate(8deg)}}
@keyframes shake{0%,100%{transform:translate(0,0)}10%{transform:translate(-30px,20px)}25%{transform:translate(28px,-24px)}40%{transform:translate(-20px,-10px)}60%{transform:translate(16px,14px)}80%{transform:translate(-8px,6px)}}
@keyframes flyR{0%{transform:translateX(-700px)}100%{transform:translateX(0)}}
@keyframes flyL{0%{transform:translateX(700px)}100%{transform:translateX(0)}}
@keyframes dropIn{0%{transform:translateY(-900px)}100%{transform:translateY(0)}}
@keyframes sail{0%{transform:translateX(0)}100%{transform:translateX(560px)}}
@keyframes sneak{0%{transform:translateX(0)}100%{transform:translateX(420px)}}
@keyframes grab{0%{transform:translate(0,0);opacity:1}100%{transform:translate(300px,160px) scale(.3);opacity:0}}
@keyframes spin{0%{transform:rotate(0)}100%{transform:rotate(360deg)}}
@keyframes zfloat{0%{transform:translate(0,0) scale(.5);opacity:0}30%{opacity:1}100%{transform:translate(60px,-220px) scale(1.2);opacity:0}}
@keyframes flash{0%{opacity:.9}100%{opacity:0}}
@keyframes blink{0%{opacity:.55}50%{opacity:0}}
@keyframes grow{0%{transform:scaleX(0)}100%{transform:scaleX(1)}}
@keyframes dim{0%{filter:none}100%{filter:brightness(.25) saturate(.4)}}
@keyframes recolor{0%{filter:none}100%{filter:hue-rotate(var(--h,0deg)) saturate(1.3)}}
@keyframes nudge{0%,100%{translate:0 0}50%{translate:14px 10px}}
@keyframes kbzoomin{0%{transform:scale(1)}100%{transform:scale(1.14)}}
@keyframes kbzoomout{0%{transform:scale(1.16)}100%{transform:scale(1.02)}}
@keyframes kbpanl{0%{transform:scale(1.14) translateX(3.5%)}100%{transform:scale(1.14) translateX(-3.5%)}}
@keyframes kbpanr{0%{transform:scale(1.14) translateX(-3.5%)}100%{transform:scale(1.14) translateX(3.5%)}}
@keyframes kbpanu{0%{transform:scale(1.14) translateY(3.5%)}100%{transform:scale(1.14) translateY(-3.5%)}}
.kb{position:absolute;inset:0;background-size:cover;background-position:center}
.vig{position:absolute;inset:0;background:radial-gradient(circle,transparent 60%,rgba(0,0,0,.35))}
@keyframes spread{0%{transform:scale(.2);opacity:0}100%{transform:scale(1);opacity:1}}
"""

EASE = {"pop": "cubic-bezier(.2,1.4,.4,1)", "stamp": "ease-out", "flyR": "cubic-bezier(.2,.9,.3,1)",
        "flyL": "cubic-bezier(.2,.9,.3,1)", "dropIn": "cubic-bezier(.5,0,.5,1.3)", "flash": "ease-out",
        "show": "steps(1)", "hide": "steps(1)", "grab": "ease-in", "spin": "linear", "blink": "steps(1)",
        "sail": "ease-in-out", "sneak": "ease-in-out", "zfloat": "ease-out", "grow": "ease-out"}
LOOPS = {"pulse", "bob", "wiggle", "spin", "blink", "nudge"}


def load_spec(d):
    sp = importlib.util.spec_from_file_location("spec", os.path.join(d, "spec.py"))
    m = importlib.util.module_from_spec(sp)
    sys.path.insert(0, ENGINE)
    sp.loader.exec_module(m)
    return m


def build(short_dir, preview=False):
    ensure_fonts()
    short_dir = os.path.abspath(short_dir)
    spec = load_spec(short_dir)
    work = os.path.join(tempfile.gettempdir(), "shorts_work", os.path.basename(short_dir))
    os.makedirs(work, exist_ok=True)
    cache = os.path.join(tempfile.gettempdir(), "shorts_tts")
    os.makedirs(cache, exist_ok=True)

    # ---- timing
    t = 0.2
    subs, voice, scenes = [], [], []
    for sc in spec.SCENES:
        s0, cues = t, {}
        for li, line in enumerate(sc["lines"]):
            clip = tts(line["tts"], cache)
            d = len(clip) / SR
            voice.append((t, clip))
            tot = sum(weight(c) for c in line["chunks"])
            ct = t
            for ci, ch in enumerate(line["chunks"]):
                cues[f"{li}.{ci}"] = ct
                subs.append([ct, ct + d * weight(ch) / tot, ch])
                ct += d * weight(ch) / tot
            t += d + 0.1
        t += 0.12
        scenes.append(dict(sc=sc, s=s0, e=t, cues=cues))
    total = t + 0.7
    scenes[-1]["e"] = total
    for i in range(len(subs) - 1):
        subs[i][1] = subs[i + 1][0]
    subs[-1][1] = total

    def cue(scn, c):
        base, *offs = c.split("+")
        v = scn["s"] if base == "s" else scn["cues"][base]
        return v + sum(float(o) for o in offs)

    # ---- audio
    N = int(total * SR)
    mix = bgm(total, getattr(spec, "SEED", 1)).astype(np.float32)

    def put(buf, x, at, g=1.0):
        i = max(int(at * SR), 0)
        x = x[: max(N - i, 0)]
        buf[i:i + len(x)] += x * g

    for scn in scenes[1:]:
        put(mix, sfx("whoosh"), scn["s"] - .12)
    for scn in scenes:
        for name, c, *g in scn["sc"].get("sfx", []):
            put(mix, sfx(name), cue(scn, c), g[0] if g else 1.0)
    bed = mix.copy()
    for at, clip in voice:
        put(mix, clip, at, 1.0)
    peak = max(np.abs(mix).max(), 1e-6) / .89
    for name, tr in (("audio.wav", mix / peak), ("audio_novoice.wav", bed / peak)):
        with wave.open(os.path.join(work, name), "w") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
            w.writeframes((np.clip(tr, -1, 1) * 32767).astype(np.int16).tobytes())

    # ---- html
    def el_html(scn, el):
        parts = []
        for a in el["anims"]:
            name, c, dur = a[0], a[1], a[2]
            ease = a[3] if len(a) > 3 else EASE.get(name, "cubic-bezier(.2,1.4,.4,1)")
            it = a[4] if len(a) > 4 else ("infinite" if name in LOOPS else "1")
            fill = "none" if name == "flash" else "both"
            if name == "flash":
                fill = "forwards"
            parts.append(f"{name} {dur}s {ease} {cue(scn, c):.3f}s {it} normal {fill}")
        an = f"animation:{','.join(parts)};" if parts else ""
        fs = f"font-size:{el['size']}px;" if el["size"] else ""
        cls = el["cls"]
        klass = "x" + ("" if cls == "box" else f" {cls}")
        return f'<div class="{klass}" style="left:{el["x"]}px;top:{el["y"]}px;{fs}{an}{el["style"]}">{el["content"]}</div>'

    scenes_html = ""
    for scn in scenes:
        sc = scn["sc"]
        inner = f'<div class="bg" style="background:{sc.get("bg", "#222")}"></div>'
        if sc.get("img"):
            ip = os.path.join(short_dir, "images", sc["img"])
            if os.path.exists(ip):
                inner += (f'<div class="kb" style="background-image:url(\'file://{ip}\');animation:kb{sc.get("kb", "zoomin")} '
                          f'{scn["e"] - scn["s"] + .4:.2f}s linear {scn["s"]:.3f}s 1 normal both"></div><div class="vig"></div>')
            else:
                inner += f'<div class="x tag" style="left:40px;top:40px;font-size:40px">missing image: {sc["img"]}</div>'
        inner += "".join(el_html(scn, e) for e in sc.get("els", []))
        scenes_html += (f'<div class="scene" data-s="{scn["s"]:.3f}" data-e="{scn["e"]:.3f}"><div class="scin" style="animation:sceneIn .35s '
                        f'cubic-bezier(.2,.9,.3,1) {scn["s"]:.3f}s 1 normal both">{inner}</div></div>')
    accent = getattr(spec, "ACCENT", "#ff2020")
    html = f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS.replace('%(fonts)s', FONTS).replace('%(accent)s', accent)}</style></head><body>
<div class="title"><div class="l1">{spec.TITLE[0]}</div><div class="l2">{spec.TITLE[1]}</div></div>
<div class="stage">{scenes_html}</div><div class="sub" id="sub"></div><div class="progress" id="prog"></div>
<div class="series">{getattr(spec, 'SERIES', '')}</div>
<script>
const SUBS={json.dumps([[round(a, 3), round(b, 3), c] for a, b, c in subs], ensure_ascii=False)},TOTAL={total:.3f};
const scenes=[...document.querySelectorAll('.scene')],sub=document.getElementById('sub'),prog=document.getElementById('prog');
function render(t){{
 for(const s of scenes) s.style.opacity=(t>=+s.dataset.s-0.001&&t<+s.dataset.e)?1:0;
 for(const a of document.getAnimations()){{a.pause();a.currentTime=t*1000;}}
 const c=SUBS.find(x=>t>=x[0]&&t<x[1]); sub.style.display=c?'block':'none';
 if(c){{sub.textContent=c[2];sub.className='sub'+(/!$/.test(c[2])&&c[2].length<6?' em':'');}}
 prog.style.width=(t/TOTAL*100)+'%';
}}
</script></body></html>"""
    open(os.path.join(work, "short.html"), "w").write(html)

    # ---- frames
    from playwright.sync_api import sync_playwright
    exe = glob.glob("/opt/pw-browsers/chromium-*/chrome-linux*/chrome")
    fdir = os.path.join(work, "frames")
    shutil.rmtree(fdir, ignore_errors=True); os.makedirs(fdir)
    thumb_t = cue(scenes[spec.THUMB_CUE[0]], spec.THUMB_CUE[1]) + .45
    times = [scn["e"] - .25 for scn in scenes] if preview else [i / FPS for i in range(int(total * FPS))]
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=exe[0]) if exe else p.chromium.launch()
        pg = b.new_page(viewport={"width": W, "height": H})
        pg.goto("file://" + os.path.join(work, "short.html"))
        pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(500)
        for i, tt in enumerate(times):
            pg.evaluate(f"render({tt})")
            pg.screenshot(path=os.path.join(fdir, f"f{i:05d}.jpg"), type="jpeg", quality=90)
        pg.evaluate(f"render({thumb_t})")
        pg.screenshot(path=os.path.join(short_dir, "thumbnail.jpg"), type="jpeg", quality=92)
        b.close()
    if preview:
        from PIL import Image
        ims = [Image.open(f).resize((270, 480)) for f in sorted(glob.glob(os.path.join(fdir, "*.jpg")))]
        cols = min(len(ims), 5)
        g = Image.new("RGB", (270 * cols, 480 * ((len(ims) + cols - 1) // cols)))
        for i, im in enumerate(ims):
            g.paste(im, ((i % cols) * 270, (i // cols) * 480))
        g.save(os.path.join(work, "contact.jpg"), quality=85)
        print("preview", os.path.join(work, "contact.jpg"), "total", round(total, 2))
        return

    def enc(audio, out):
        subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(fdir, "f%05d.jpg"),
                        "-i", os.path.join(work, audio), "-c:v", "libx264", "-preset", "medium", "-crf", "20",
                        "-pix_fmt", "yuv420p", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "160k", "-ar", "44100", "-shortest",
                        "-movflags", "+faststart", os.path.join(short_dir, out)], check=True)
    enc("audio.wav", "short.mp4")
    enc("audio_novoice.wav", "short_no-narration.mp4")

    def ts(x):
        return f"{int(x // 3600):02d}:{int(x % 3600 // 60):02d}:{int(x % 60):02d},{int(round((x % 1) * 1000)) % 1000:03d}"
    with open(os.path.join(short_dir, "subtitles.srt"), "w") as f:
        for i, (a, b, c) in enumerate(subs, 1):
            f.write(f"{i}\n{ts(a)} --> {ts(b)}\n{c}\n\n")
    with open(os.path.join(short_dir, "upload.txt"), "w") as f:
        f.write(f"[제목]\n{spec.YT_TITLE}\n\n[설명]\n{spec.DESCRIPTION.strip()}\n\n{' '.join('#' + x for x in spec.TAGS)}\n\n"
                f"[태그]\n{', '.join(spec.TAGS)}\n\n[길이] {total:.1f}초 · 1080x1920 · 30fps\n")
    print("done", short_dir, round(total, 2))


if __name__ == "__main__":
    build(sys.argv[1], preview="--preview" in sys.argv)
