#!/usr/bin/env python3
"""완성본 자체 점검(H단계): 받아쓰기, 문장별 프레임 시트, 구간별 음량."""
import json, os, subprocess, sys
ep = os.path.abspath(sys.argv[1]); name = os.path.basename(ep)
mp4 = os.path.join(ep, "renders", name + ".mp4"); work = os.path.join(ep, "work")
tl = json.load(open(os.path.join(work, "timeline.json")))
# 1) 받아쓰기
subprocess.run(["ffmpeg","-y","-loglevel","error","-i",mp4,"-vn","-ac","1","-ar","16000",os.path.join(work,"final.wav")],check=True)
from faster_whisper import WhisperModel
m = WhisperModel("small", device="cpu", compute_type="int8")
segs,_ = m.transcribe(os.path.join(work,"final.wav"), language="ko", word_timestamps=True)
words = [(w.start, w.word) for s in segs for w in s.words]
print("== 받아쓰기"); print(" ".join(f"{a:.1f}:{w.strip()}" for a,w in words))
# 2) 장면마다 중간 프레임 한 장씩 → 가로로 이어 붙인 시트
frames = []
for x in tl["timeline"]:
    t = x["start"] + x["dur"]*0.5; f = os.path.join(work, f"chk{x['i']:02d}.jpg")
    subprocess.run(["ffmpeg","-y","-loglevel","error","-ss",f"{t:.2f}","-i",mp4,"-frames:v","1","-vf","scale=216:-2",f],check=True); frames.append(f)
args = sum([["-i",f] for f in frames],[])
n=len(frames); cols=min(n,6); rows=(n+cols-1)//cols
layout="|".join(f"{(k%cols)*216}_{(k//cols)*384}" for k in range(n))
subprocess.run(["ffmpeg","-y","-loglevel","error",*args,"-filter_complex",f"xstack=inputs={n}:layout={layout}:fill=black",os.path.join(ep,"renders","check.jpg")],check=True)
# 3) 구간별 음량(장면 단위 RMS)
print("== 장면별 음량(dB)")
for x in tl["timeline"]:
    r = subprocess.run(["ffmpeg","-ss",f"{x['start']:.2f}","-t",f"{x['dur']:.2f}","-i",mp4,"-vn","-af","volumedetect","-f","null","-"],capture_output=True,text=True).stderr
    mv = [l.split(":")[1].strip() for l in r.splitlines() if "mean_volume" in l]
    print(f"{x['i']:2d} {x['start']:5.1f}s {'원본소리' if x['orig'] else (x['say'] or '')[:20]:22s} {mv[0] if mv else '?'}")
