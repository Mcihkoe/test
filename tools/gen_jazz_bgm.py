#!/usr/bin/env python3
"""Synthesize a short, jazzy instrumental BGM loop (no external AI needed).

Usage: python3 tools/gen_jazz_bgm.py OUT.wav [--bpm 92] [--seed 7] [--transpose 0]
Layers: electric-piano comping, walking bass, brush drums, vibraphone melody.
"""
import argparse
import wave

import numpy as np
from scipy.signal import butter, fftconvolve, lfilter

SR = 44100
TRANSPOSE = 0

# name: (bass root, comp voicing, chord tones for melody, scale pitch classes)
CHORDS = {
    "Dm9": (38, [53, 57, 60, 64], [62, 65, 69, 72], [2, 4, 5, 7, 9, 11, 0]),
    "G13": (43, [53, 59, 62, 64], [59, 62, 65, 67], [7, 9, 11, 0, 2, 4, 5]),
    "Cmaj9": (36, [52, 55, 59, 62], [60, 64, 67, 71], [0, 2, 4, 5, 7, 9, 11]),
    "A7alt": (45, [53, 55, 61, 64], [57, 61, 64, 67], [9, 10, 1, 2, 4, 5, 7]),
    "Fmaj9": (41, [57, 60, 64, 67], [65, 69, 72, 76], [5, 7, 9, 10, 0, 2, 4]),
    "Fm6": (41, [56, 60, 62, 65], [65, 68, 72, 74], [5, 7, 8, 10, 0, 2, 3]),
    "Em7": (40, [55, 59, 62, 67], [64, 67, 71, 74], [4, 6, 7, 9, 11, 1, 2]),
    "A7": (45, [55, 61, 64, 66], [57, 61, 64, 67], [9, 11, 1, 2, 4, 6, 7]),
}
FORM = (
    ["Dm9", "G13", "Cmaj9", "A7alt"]
    + ["Fmaj9", "Fm6", "Em7", "A7"]
    + ["Dm9", "G13", "Cmaj9", "Cmaj9"]
)
CHORUSES = 4


def hz(m):
    return 440.0 * 2 ** ((m + TRANSPOSE - 69) / 12)


def add(buf, start, sig):
    i = int(start * SR)
    if i >= len(buf):
        return
    n = min(len(sig), len(buf) - i)
    buf[i : i + n] += sig[:n]


def tone_epiano(m, dur, vel):
    t = np.arange(int(dur * SR)) / SR
    f = hz(m)
    idx = 1.6 * np.exp(-5 * t)
    s = np.sin(2 * np.pi * f * t + idx * np.sin(2 * np.pi * f * t))
    s += 0.25 * np.sin(2 * np.pi * f * 4 * t) * np.exp(-12 * t)
    env = np.exp(-2.2 * t) * np.minimum(1, t / 0.005)
    env *= np.minimum(1, (dur - t) / 0.08)
    return s * env * vel * (1 + 0.08 * np.sin(2 * np.pi * 4.8 * t))


def tone_bass(m, dur, vel):
    t = np.arange(int(dur * SR)) / SR
    f = hz(m)
    s = np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-6 * t)
    s += 0.25 * np.sin(2 * np.pi * 3 * f * t) * np.exp(-9 * t)
    env = np.exp(-3.2 * t) * np.minimum(1, t / 0.004)
    env *= np.minimum(1, (dur - t) / 0.05)
    return s * env * vel


def tone_vibes(m, dur, vel):
    t = np.arange(int(dur * SR)) / SR
    f = hz(m)
    s = np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * 4 * f * t) * np.exp(-8 * t)
    env = np.exp(-1.6 * t) * np.minimum(1, t / 0.003)
    env *= np.minimum(1, (dur - t) / 0.1)
    return s * env * vel * (1 + 0.15 * np.sin(2 * np.pi * 5.5 * t))


_hp = butter(2, 6000 / (SR / 2), btype="high")
_bp = butter(2, [900 / (SR / 2), 5000 / (SR / 2)], btype="band")


def ride(rng, vel):
    n = int(0.35 * SR)
    t = np.arange(n) / SR
    noise = lfilter(*_hp, rng.standard_normal(n))
    return noise * np.exp(-9 * t) * vel


def brush(rng, vel):
    n = int(0.12 * SR)
    t = np.arange(n) / SR
    return lfilter(*_bp, rng.standard_normal(n)) * np.exp(-25 * t) * vel


def kick(vel):
    n = int(0.18 * SR)
    t = np.arange(n) / SR
    return np.sin(2 * np.pi * (55 + 40 * np.exp(-30 * t)) * t) * np.exp(-18 * t) * vel


def reverb(sig, rng, seconds=1.8, mix=0.28):
    n = int(seconds * SR)
    t = np.arange(n) / SR
    ir = lfilter(*butter(1, 5000 / (SR / 2)), rng.standard_normal(n)) * np.exp(-3.2 * t)
    wet = fftconvolve(sig, ir)[: len(sig)]
    wet /= np.max(np.abs(wet)) + 1e-9
    return sig * (1 - mix) + wet * np.max(np.abs(sig)) * mix


def fold(pc_note, lo, hi):
    while pc_note < lo:
        pc_note += 12
    while pc_note >= hi:
        pc_note -= 12
    return pc_note


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--bpm", type=float, default=92)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--transpose", type=int, default=0, help="semitones, -3..3 keeps bass in range")
    a = ap.parse_args()
    global TRANSPOSE
    TRANSPOSE = a.transpose
    rng = np.random.default_rng(a.seed)
    beat = 60.0 / a.bpm
    swing = 2 / 3  # position of the off-beat eighth inside a beat
    bars = [c for _ in range(CHORUSES) for c in FORM]
    total = len(bars) * 4 * beat + 3.0
    n = int(total * SR)
    comp, bass, drums, mel = (np.zeros(n) for _ in range(4))

    prev_note = 72
    for bi, name in enumerate(bars):
        root, voic, tones, scale = CHORDS[name]
        nxt = CHORDS[bars[(bi + 1) % len(bars)]][0]
        t0 = bi * 4 * beat

        # comping: charleston-ish, 2 hits per bar with variation
        hits = [(0.0, 1.5), (2 + swing, 1.0)] if rng.random() < 0.6 else [(1.0, 1.2), (2.0, 1.5)]
        for off, ln in hits:
            for k, m in enumerate(voic):
                add(comp, t0 + off * beat + k * 0.012, tone_epiano(m, ln * beat, 0.16))

        # walking bass: root, scale step, chord tone, chromatic approach
        pcs = [fold(root, 36, 52)]
        pcs.append(fold(root + int(rng.choice([4, 7, 3, 2])), 36, 52))
        pcs.append(fold(root + int(rng.choice([7, 4, 9])), 36, 52))
        approach = fold(nxt + int(rng.choice([-1, 1])), 36, 52)
        pcs.append(approach)
        for i, m in enumerate(pcs):
            add(bass, t0 + i * beat, tone_bass(m, beat * 0.95, 0.5))

        # drums: ride + swung skip, feathered kick, brush on 2 & 4
        for i in range(4):
            add(drums, t0 + i * beat, ride(rng, 0.12))
            add(drums, t0 + i * beat, kick(0.12))
            if i in (1, 3):
                add(drums, t0 + (i + swing) * beat, ride(rng, 0.07))
                add(drums, t0 + i * beat, brush(rng, 0.16))

        # melody: phrases of 2-3 bars then rest
        if bi % 4 < 3 and rng.random() < 0.85:
            cur = prev_note
            pos = 0.0
            while pos < 4.0:
                on_beat = abs(pos - round(pos)) < 1e-6
                step = 1.0 if (on_beat and rng.random() < 0.35) else (swing if not on_beat else 1 - swing)
                if on_beat and rng.random() < 0.18:
                    pos += 1.0  # rest
                    continue
                if on_beat and rng.random() < 0.6:
                    cur = min(tones, key=lambda m: abs(m - cur) + rng.random() * 3)
                else:
                    cands = [m for m in range(64, 85) if m % 12 in scale]
                    near = [m for m in cands if 0 < abs(m - cur) <= 4]
                    cur = int(rng.choice(near)) if near else cur
                add(mel, t0 + pos * beat, tone_vibes(cur, max(step, 0.5) * beat * 1.4, 0.22))
                prev_note = cur
                pos += step if not on_beat else (swing if rng.random() < 0.55 else 1.0)

    # vinyl crackle (very subtle)
    crackle = np.zeros(n)
    for _ in range(int(total * 6)):
        i = int(rng.random() * (n - 200))
        crackle[i : i + 80] += rng.standard_normal(80) * np.exp(-np.arange(80) / 12) * 0.02

    mix = reverb(comp + mel, rng) + bass * 0.9 + drums + crackle
    mix = lfilter(*butter(2, 9500 / (SR / 2)), mix)
    fade = int(2 * SR)
    mix[:fade] *= np.linspace(0, 1, fade)
    mix[-fade:] *= np.linspace(1, 0, fade)
    mix = mix / np.max(np.abs(mix)) * 0.85

    pcm = (mix * 32767).astype("<i2")
    with wave.open(a.out, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    print(f"wrote {a.out}: {total:.1f}s, {len(bars)} bars @ {a.bpm} bpm")


if __name__ == "__main__":
    main()
