#!/usr/bin/env python3
"""쇼츠 한 편 제작 (F·G·H단계): TTS → 장면 길이 맞추기 → 소리 섞기 → 화면 틀 렌더 → 자체 점검.

사용법: python3 make.py <편 폴더>   (폴더 안의 spec.json을 읽고 renders/에 결과를 쓴다)

spec.json
{
  "title": ["윗줄", "아랫줄"], "accent": "sky|red|yellow", "credit": "채널명",
  "src": "../raw/ref/xxx.mp4",          # 기본 원본
  "crop": "w:h:x:y",                    # 원본에서 먼저 잘라 낼 영역(선택)
  "cover": [[y0, y1], ...],             # 원본 자막 띠를 흐리게(원본 픽셀, 선택)
  "bars": [[y0, y1], ...],              # 원본 자막 띠를 검은 띠로 덮기(원본 픽셀, 선택)
  "sub_margin": 330,                    # 자막 높이(화면 아래에서 px)
  "bgm": "../bgm/x.mp3", "bgm_vol": 0.12,
  "voice": "M1",
  "scenes": [
    {"say": "TTS로 읽을 문장", "sub": "자막 [강조]", "at": 36.0, "vol": 0.15,
     "circle": {"x": 540, "y": 500, "r": 150}, "focus": 0.5, "speed": 1.0},
    {"orig": 4.0, "at": 35.0, "vol": 1.0, "shake": 0.2, "sub": "(선택)"}
  ]
}
연속된 say 장면은 한 번에 합성해서(문장 사이가 자연스럽게) 문장 시작 시각으로 장면을 나눈다.
"""
import difflib
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render  # noqa: E402

W, H, FPS, VH = render.W, render.H, render.FPS, render.VIDEO_H
SR = 44100
PAD = 0.25  # 블록 마지막 문장 뒤 여유


def run(cmd):
    subprocess.run(cmd, check=True)


def ff(*args):
    run(["ffmpeg", "-y", "-loglevel", "error", *args])


def dur(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                         capture_output=True, text=True, check=True).stdout
    return float(out.strip())


_tts = None
_whisper = None


def tts(text, out, voice):
    global _tts
    from supertonic import TTS
    if _tts is None:
        _tts = TTS(auto_download=True)
    style = _tts.get_voice_style(voice_name=voice)
    audio, _ = _tts.synthesize(text, voice_style=style, lang="ko", speed=1.2, total_steps=14)
    raw = out + ".raw.wav"
    _tts.save_audio(audio, raw)
    # 1.2배 합성 후 재생 속도만 올림(체감 1.4배) + 앞뒤 무음 제거
    ff("-i", raw, "-af", "atempo=1.1667,silenceremove=start_periods=1:start_threshold=-45dB,areverse,"
       "silenceremove=start_periods=1:start_threshold=-45dB,areverse", "-ar", str(SR), "-ac", "2", out)
    os.remove(raw)


def whisper_words(path):
    global _whisper
    from faster_whisper import WhisperModel
    if _whisper is None:
        _whisper = WhisperModel("small", device="cpu", compute_type="int8")
    segs, _ = _whisper.transcribe(path, language="ko", word_timestamps=True)
    return [(w.word, w.start, w.end) for s in segs for w in s.words]


def norm(s):
    return re.sub(r"[^0-9A-Za-z가-힣]", "", s)


def sentence_starts(sentences, words):
    """문장별 시작 시각: TTS 원문 글자와 받아쓰기 글자를 맞춰서 문장 첫 글자의 시각을 찾는다."""
    ref, bounds = "", []
    for s in sentences:
        bounds.append(len(ref))
        ref += norm(s)
    hyp, times = "", []
    for w, a, b in words:
        n = norm(w)
        for i, _ in enumerate(n):
            times.append(a + (b - a) * i / max(len(n), 1))
        hyp += n
    sm = difflib.SequenceMatcher(None, ref, hyp, autojunk=False)
    mapping = {}
    for blk in sm.get_matching_blocks():
        for k in range(blk.size):
            mapping[blk.a + k] = blk.b + k
    starts = []
    for i, bnd in enumerate(bounds):
        j = next((mapping[k] for k in range(bnd, len(ref)) if k in mapping), None)
        starts.append(0.0 if i == 0 else (times[j] if j is not None else None))
    # 못 찾은 곳은 글자 수 비율로 메움
    total = words[-1][2] if words else 1.0
    for i, s in enumerate(starts):
        if s is None:
            starts[i] = total * bounds[i] / max(len(ref), 1)
    for i in range(1, len(starts)):  # 단조 증가 보장
        starts[i] = max(starts[i], starts[i - 1] + 0.3)
    return starts


def prep_clip(src, sc, d, crop, cover, bars, out):
    """장면 클립(영상+원본 소리). 1080xVH를 꽉 채우고 천천히 확대."""
    speed = sc.get("speed", 1.0)
    focus = sc.get("focus", 0.5)
    z = sc.get("zoom", 0.04)
    pre = []
    c = sc.get("crop", crop)
    if c:
        pre.append(f"crop={c}")
    for y0, y1 in sc.get("bars", bars) or []:
        pre.append(f"drawbox=x=0:y={y0}:w=iw:h={y1 - y0}:color=black:t=fill")
    for y0, y1 in sc.get("cover", cover) or []:
        pre.append(f"split[a{y0}][b{y0}];[b{y0}]crop=iw:{y1 - y0}:0:{y0},gblur=sigma=25[c{y0}];"
                   f"[a{y0}][c{y0}]overlay=0:{y0}")
    vf = ",".join(pre + [
        f"setpts=PTS/{speed}", f"fps={FPS}",
        f"scale={W}:{VH}:force_original_aspect_ratio=increase",
        f"crop={W}:{VH}:(iw-{W})/2:(ih-{VH})*{focus}",
        f"scale=w='trunc({W}*(1+{z}*t/{d})/2)*2':h='trunc({VH}*(1+{z}*t/{d})/2)*2':eval=frame",
        f"crop={W}:{VH}", "setsar=1",
    ])
    af = f"atempo={speed}," if speed != 1.0 else ""
    af += f"volume={sc.get('vol', 0.15)},aresample={SR},aformat=channel_layouts=stereo"
    ff("-ss", str(sc["at"]), "-t", str(d * speed + 0.1), "-i", src,
       "-filter_complex", f"[0:v]{vf}[v];[0:a]{af}[a]", "-map", "[v]", "-map", "[a]",
       "-t", str(d), "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", "-c:a", "pcm_s16le", out)


def chunk_sub(text, start, end, maxlen=11):
    """자막을 2~3단어씩 나눠서 글자 수 비율로 시간 배분. [강조]는 덩어리 안에서 유지."""
    words, chunks, cur = text.split(), [], []
    for w in words:
        if cur and len(norm(" ".join(cur + [w]))) > maxlen:
            chunks.append(" ".join(cur))
            cur = []
        cur.append(w)
    if cur:
        chunks.append(" ".join(cur))
    # 덩어리마다 대괄호 짝 맞추기
    fixed, open_ = [], False
    for ch in chunks:
        s = ("[" if open_ else "") + ch
        open_ = s.count("[") > s.count("]")
        fixed.append(s + ("]" if open_ else ""))
    lens = [max(len(norm(c)), 1) for c in fixed]
    tot, t, out = sum(lens), start, []
    for c, n in zip(fixed, lens):
        e = t + (end - start) * n / tot
        out.append({"start": round(t, 2), "end": round(e, 2), "text": c})
        t = e
    return out


def main(ep_dir):
    ep_dir = os.path.abspath(ep_dir)
    spec = json.load(open(os.path.join(ep_dir, "spec.json"), encoding="utf-8"))
    work = os.path.join(ep_dir, "work")
    rdir = os.path.join(ep_dir, "renders")
    os.makedirs(work, exist_ok=True)
    os.makedirs(rdir, exist_ok=True)
    src_default = os.path.join(ep_dir, spec["src"])
    voice = spec.get("voice", "M1")
    scenes = spec["scenes"]

    # 1) say 블록별 TTS 합성 → 문장 시작 시각 → 장면 길이
    timeline, vo_parts, subs, t = [], [], [], 0.0
    i = 0
    blk_no = 0
    while i < len(scenes):
        if "orig" in scenes[i]:
            sc = scenes[i]
            timeline.append((sc, t, sc["orig"]))
            if sc.get("sub"):
                subs.append({"start": t, "end": t + sc["orig"], "text": sc["sub"]})
            t += sc["orig"]
            i += 1
            continue
        j = i
        while j < len(scenes) and "say" in scenes[j]:
            j += 1
        block = scenes[i:j]
        wav = os.path.join(work, f"vo{blk_no}.wav")
        tts(" ".join(s["say"] for s in block), wav, voice)
        words = whisper_words(wav)
        starts = sentence_starts([s["say"] for s in block], words)
        bdur = dur(wav)
        ends = starts[1:] + [bdur + PAD]
        for sc, a, b in zip(block, starts, ends):
            timeline.append((sc, t + a, b - a))
            subs += chunk_sub(sc.get("sub", sc["say"]), t + a, t + min(b, bdur + 0.1))
        vo_parts.append((wav, t))
        t += bdur + PAD
        i = j
        blk_no += 1
    total = round(t, 3)

    # 2) 장면 클립(영상+원본 소리)
    clips = []
    for k, (sc, a, d) in enumerate(timeline):
        c = os.path.join(work, f"c{k:02d}.mov")
        src = os.path.join(ep_dir, sc["src"]) if sc.get("src") else src_default
        prep_clip(src, sc, d, spec.get("crop"), spec.get("cover"), spec.get("bars"), c)
        clips.append(c)
    lst = os.path.join(work, "list.txt")
    open(lst, "w").writelines(f"file '{c}'\n" for c in clips)
    joined = os.path.join(work, "joined.mov")
    ff("-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", joined)

    # 3) 소리 섞기: 장면 원본 소리 + 나레이션 + 배경음악(원본 소리 구간은 거의 끔)
    inputs = ["-i", joined]
    fc, labels = [], ["[0:a]"]
    for n, (wav, off) in enumerate(vo_parts, start=1):
        inputs += ["-i", wav]
        ms = int(off * 1000)
        fc.append(f"[{n}:a]adelay={ms}|{ms},volume=1.0[vo{n}]")
        labels.append(f"[vo{n}]")
    if spec.get("bgm"):
        b = len(vo_parts) + 1
        inputs += ["-stream_loop", "-1", "-i", os.path.join(ep_dir, spec["bgm"])]
        quiet = "+".join(f"between(t,{a:.2f},{a + d:.2f})" for sc, a, d in timeline if "orig" in sc) or "0"
        bv = spec.get("bgm_vol", 0.12)
        fc.append(f"[{b}:a]aresample={SR},aformat=channel_layouts=stereo,"
                  f"volume='if({quiet},0.02,{bv})':eval=frame,atrim=0:{total}[bg]")
        labels.append("[bg]")
    fc.append(f"{''.join(labels)}amix=inputs={len(labels)}:duration=first:normalize=0,"
              f"alimiter=limit=0.95,atrim=0:{total}[a]")
    mix = os.path.join(work, "mix.wav")
    ff(*inputs, "-filter_complex", ";".join(fc), "-map", "[a]", "-ar", str(SR), mix)

    # 4) 화면 틀(제목·자막·빨간 원·흔들림) 렌더
    circles = [dict(sc["circle"], start=a, end=a + min(d, sc["circle"].get("for", 1.5)))
               for sc, a, d in timeline if sc.get("circle")]
    shakes = [{"start": a + sc["shake"], "dur": 0.4} for sc, a, d in timeline if "shake" in sc]
    rspec = {"title": spec["title"], "accent": spec.get("accent", "red"), "credit": spec.get("credit"),
             "subs": subs, "circles": circles, "shakes": shakes, "sub_margin": spec.get("sub_margin", 330)}
    ass = os.path.join(work, "subs.ass")
    render.build_ass(rspec, total, ass)
    shake = "+".join(f"between(t,{s['start']:.2f},{s['start'] + s['dur']:.2f})" for s in shakes) or "0"
    amp = 18
    out = os.path.join(rdir, os.path.basename(ep_dir) + ".mp4")
    vfc = (f"color=black:s={W}x{H}:r={FPS}:d={total}[bg];[0:v]setpts=PTS-STARTPTS[v];"
           f"[bg][v]overlay=0:{render.VIDEO_Y}:shortest=1,subtitles='{ass}':fontsdir='{render.FONT_DIR}',"
           f"scale={W + 2 * amp}:{H + 2 * amp},crop={W}:{H}:x='{amp}+({shake})*{amp}*sin(t*90)':"
           f"y='{amp}+({shake})*{amp}*cos(t*77)'[out]")
    ff("-i", joined, "-i", mix, "-filter_complex", vfc, "-map", "[out]", "-map", "1:a",
       "-t", str(total), "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(FPS),
       "-c:a", "aac", "-b:a", "192k", out)

    json.dump({"total": total, "timeline": [{"i": k, "start": round(a, 2), "dur": round(d, 2),
               "say": sc.get("say"), "orig": sc.get("orig"), "at": sc["at"]} for k, (sc, a, d) in enumerate(timeline)],
               "subs": subs}, open(os.path.join(work, "timeline.json"), "w"), ensure_ascii=False, indent=1)
    print(f"rendered {out} ({total:.2f}s)")
    return out


if __name__ == "__main__":
    main(sys.argv[1])
