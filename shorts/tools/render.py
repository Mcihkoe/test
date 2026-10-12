#!/usr/bin/env python3
"""쇼츠 화면 틀 렌더러 (G단계).

spec.json 하나로 1080x1920 세로 영상을 만든다.
- 위: 큰 제목 두 줄(흰색 + 빨강 또는 하늘색) 고정
- 가운데: 장면 클립(장면마다 천천히 확대)
- 아래: 말하는 구절 자막, [대괄호] 안 단어는 강조색
- 맨 아래: 작은 회색 원본 출처
- 빨간 원(circles), 화면 흔들림(shakes)

사용법: python3 render.py spec.json out.mp4
spec.json 예시는 shorts/tools/example_spec.json 참고.
소리는 미리 섞은 wav 한 개(spec["audio"])를 그대로 얹는다.
"""
import json
import os
import subprocess
import sys
import tempfile

W, H, FPS = 1080, 1920, 30
VIDEO_Y, VIDEO_H = 400, 1180  # 가운데 영상 영역
FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fonts")
FONT = "Black Han Sans"
COLORS = {"red": "&H003030FF&", "sky": "&H00FFD43A&", "yellow": "&H0000E1FF&", "white": "&H00FFFFFF&"}


def ass_time(t):
    h, rem = divmod(max(t, 0), 3600)
    m, s = divmod(rem, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"


def ass_text(text, accent):
    # [강조] → 강조색, 나머지는 흰색
    return text.replace("[", "{\\c" + COLORS[accent] + "}").replace("]", "{\\c" + COLORS["white"] + "}")


def circle_drawing(r):
    k = 0.5523 * r  # 베지어 원 근사
    return (f"m {r} 0 b {r} {k} {k} {r} 0 {r} b {-k} {r} {-r} {k} {-r} 0 "
            f"b {-r} {-k} {-k} {-r} 0 {-r} b {k} {-r} {r} {-k} {r} 0")


def build_ass(spec, total, path):
    accent = spec.get("accent", "red")
    lines = [
        "[Script Info]", "ScriptType: v4.00+", f"PlayResX: {W}", f"PlayResY: {H}", "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, "
        "Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, "
        "Alignment, MarginL, MarginR, MarginV, Encoding",
        f"Style: Title,{FONT},96,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,6,0,8,40,40,0,1",
        f"Style: Sub,{FONT},78,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,0,0,0,0,100,100,0,0,1,7,2,2,60,60,0,1",
        f"Style: Credit,{FONT},34,&H00A0A0A0,&H00A0A0A0,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,2,40,40,40,1",
        f"Style: Circle,{FONT},20,&H00000000,&H00000000,{COLORS['red'][:-1]},&H00000000,0,0,0,0,100,100,0,0,1,12,0,7,0,0,0,1",
        "", "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    ]
    t1, t2 = spec["title"]
    end = ass_time(total)
    # 긴 제목은 화면 폭(양옆 40px 여백)에 맞게 글자 크기를 줄임
    fs = min(96, int(1000 / (max(len(t1), len(t2)) * 0.95)))
    lines.append(f"Dialogue: 2,0:00:00.00,{end},Title,,0,0,90,,{{\\fs{fs}}}{t1}")
    lines.append(f"Dialogue: 2,0:00:00.00,{end},Title,,0,0,{90 + int(fs * 1.15)},,{{\\fs{fs}\\c{COLORS[accent]}}}{t2}")
    for s in spec.get("subs", []):
        lines.append(f"Dialogue: 3,{ass_time(s['start'])},{ass_time(s['end'])},Sub,,0,0,{spec.get('sub_margin', 330)},,"
                     f"{{\\fad(60,0)}}{ass_text(s['text'], accent)}")
    if spec.get("credit"):
        lines.append(f"Dialogue: 2,0:00:00.00,{end},Credit,,0,0,0,,원본 영상: {spec['credit']} / YouTube")
    for c in spec.get("circles", []):
        x, y, r = c["x"], VIDEO_Y + c["y"], c["r"]
        lines.append(f"Dialogue: 4,{ass_time(c['start'])},{ass_time(c['end'])},Circle,,0,0,0,,"
                     f"{{\\pos({x},{y})\\1a&HFF&\\bord12\\p1\\t(0,150,\\fscx115\\fscy115)\\t(150,300,\\fscx100\\fscy100)}}"
                     f"{circle_drawing(r)}")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def prep_clip(scene, out):
    # 장면 클립: 가운데 영역(1080xVIDEO_H)을 꽉 채우게 자르고, 장면 동안 4% 천천히 확대
    d = scene["dur"]
    z = scene.get("zoom", 0.04)
    crop = f"crop={scene['crop']}," if scene.get("crop") else ""
    speed = scene.get("speed", 1.0)
    vf = (f"{crop}setpts=PTS/{speed},fps={FPS},"
          f"scale={W}:{VIDEO_H}:force_original_aspect_ratio=increase,crop={W}:{VIDEO_H},"
          f"scale=w='trunc({W}*(1+{z}*t/{d})/2)*2':h='trunc({VIDEO_H}*(1+{z}*t/{d})/2)*2':eval=frame,"
          f"crop={W}:{VIDEO_H},setsar=1")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(scene["src_start"]),
                    "-t", str(d * speed), "-i", scene["src"], "-an", "-vf", vf,
                    "-t", str(d), "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", out], check=True)


def main(spec_path, out_path):
    spec = json.load(open(spec_path, encoding="utf-8"))
    base = os.path.dirname(os.path.abspath(spec_path))
    for s in spec["scenes"]:
        s["src"] = os.path.join(base, s["src"])
    total = sum(s["dur"] for s in spec["scenes"])
    tmp = tempfile.mkdtemp(prefix="render_")
    clips = []
    for i, s in enumerate(spec["scenes"]):
        c = os.path.join(tmp, f"c{i}.mp4")
        prep_clip(s, c)
        clips.append(c)
    with open(os.path.join(tmp, "list.txt"), "w") as f:
        f.writelines(f"file '{c}'\n" for c in clips)
    joined = os.path.join(tmp, "joined.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
                    "-i", os.path.join(tmp, "list.txt"), "-c", "copy", joined], check=True)
    ass = os.path.join(tmp, "subs.ass")
    build_ass(spec, total, ass)

    # 흔들림: 프레임 전체를 살짝 키운 뒤 흔들리는 위치로 잘라 냄
    shake = "+".join(f"between(t,{s['start']},{s['start']+s.get('dur',0.4)})" for s in spec.get("shakes", [])) or "0"
    amp = 18
    fc = (f"color=black:s={W}x{H}:r={FPS}:d={total}[bg];"
          f"[0:v]setpts=PTS-STARTPTS[v];[bg][v]overlay=0:{VIDEO_Y}:shortest=1,"
          f"subtitles='{ass}':fontsdir='{FONT_DIR}',"
          f"scale={W+2*amp}:{H+2*amp},"
          f"crop={W}:{H}:x='{amp}+({shake})*{amp}*sin(t*90)':y='{amp}+({shake})*{amp}*cos(t*77)'[out]")
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", joined]
    if spec.get("audio"):
        cmd += ["-i", os.path.join(base, spec["audio"])]
    cmd += ["-filter_complex", fc, "-map", "[out]"]
    if spec.get("audio"):
        cmd += ["-map", "1:a", "-c:a", "aac", "-b:a", "192k"]
    cmd += ["-t", str(total), "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(FPS), out_path]
    subprocess.run(cmd, check=True)
    print(f"rendered {out_path} ({total:.2f}s)")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
