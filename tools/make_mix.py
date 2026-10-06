#!/usr/bin/env python3
"""Build a long playlist mix from many synthesized tracks.

Usage: python3 tools/make_mix.py --minutes 60 --out output/mix [--title "NY Afternoon Jazz"]
Writes OUT.mp3 (crossfaded, loudness-normalized) and OUT_tracklist.txt (YouTube chapters).
"""
import argparse
import random
import subprocess
import tempfile
from pathlib import Path

XFADE = 4  # seconds
HERE = Path(__file__).parent


def dur(path):
    out = subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)]
    )
    return float(out)


def ts(sec):
    sec = int(sec)
    h, m, s = sec // 3600, sec % 3600 // 60, sec % 60
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--minutes", type=float, default=60)
    ap.add_argument("--out", default="output/mix")
    ap.add_argument("--title", default="NY Afternoon Jazz")
    ap.add_argument("--seed", type=int, default=100)
    a = ap.parse_args()
    rnd = random.Random(a.seed)
    target = a.minutes * 60
    tmp = Path(tempfile.mkdtemp())
    tracks, total = [], 0.0
    i = 0
    while total < target:
        i += 1
        bpm = rnd.choice([84, 88, 92, 96, 100])
        tr = rnd.choice([-2, -1, 0, 1, 2, 3])
        wav = tmp / f"t{i:02d}.wav"
        subprocess.run(
            ["python3", str(HERE / "gen_jazz_bgm.py"), str(wav), "--bpm", str(bpm),
             "--seed", str(a.seed + i), "--transpose", str(tr)],
            check=True, stdout=subprocess.DEVNULL,
        )
        d = dur(wav)
        tracks.append((wav, d, bpm, tr))
        total += d - (XFADE if i > 1 else 0)
        print(f"track {i}: {d:.0f}s bpm={bpm} transpose={tr:+d} total={total/60:.1f}min", flush=True)

    # crossfade chain
    cmd = ["ffmpeg", "-y", "-loglevel", "error"]
    for wav, *_ in tracks:
        cmd += ["-i", str(wav)]
    filt, last = [], "[0:a]"
    for k in range(1, len(tracks)):
        lab = f"[x{k}]"
        filt.append(f"{last}[{k}:a]acrossfade=d={XFADE}:c1=tri:c2=tri{lab}")
        last = lab
    filt.append(f"{last}loudnorm=I=-16:TP=-1.5:LRA=11[out]")
    out_mp3 = Path(a.out + ".mp3")
    out_mp3.parent.mkdir(parents=True, exist_ok=True)
    cmd += ["-filter_complex", ";".join(filt), "-map", "[out]", "-c:a", "libmp3lame", "-b:a", "192k", str(out_mp3)]
    subprocess.run(cmd, check=True)

    # tracklist with chapter timestamps (first chapter must be 0:00 for YouTube)
    lines, t = [], 0.0
    for n, (_, d, bpm, tr) in enumerate(tracks, 1):
        lines.append(f"{ts(t)} {a.title} #{n:02d}")
        t += d - XFADE
    Path(a.out + "_tracklist.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {out_mp3} ({dur(out_mp3)/60:.1f} min), {len(tracks)} tracks")


if __name__ == "__main__":
    main()
