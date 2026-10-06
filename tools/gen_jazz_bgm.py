#!/usr/bin/env python3
"""Synthesize a jazzy instrumental BGM track (no external AI needed). v2

Usage: python3 tools/gen_jazz_bgm.py OUT.wav [--bpm 92] [--seed 7] [--transpose 0]

Each seed picks a chord form and an arrangement:
  intro -> head (motif melody) -> vibes solo -> piano solo -> head out -> ending chord
Layers (stereo): piano/e-piano comping, walking or two-feel bass, ride/hat/brush drums
with fills, vibraphone lead, light vinyl crackle.
"""
import argparse
import wave

import numpy as np
from scipy.signal import butter, fftconvolve, lfilter

SR = 44100
TRANSPOSE = 0

# chord quality -> (rootless voicing intervals, chord tones, scale)
QUALITY = {
    "maj9": ([4, 7, 11, 14], [0, 4, 7, 11], [0, 2, 4, 5, 7, 9, 11]),
    "6/9": ([4, 9, 14, 19], [0, 4, 7, 9], [0, 2, 4, 7, 9]),
    "m9": ([3, 7, 10, 14], [0, 3, 7, 10], [0, 2, 3, 5, 7, 9, 10]),
    "m6": ([3, 7, 9, 14], [0, 3, 7, 9], [0, 2, 3, 5, 7, 9, 11]),
    "13": ([4, 10, 14, 21], [0, 4, 7, 10], [0, 2, 4, 5, 7, 9, 10]),
    "9": ([4, 7, 10, 14], [0, 4, 7, 10], [0, 2, 4, 5, 7, 9, 10]),
    "7alt": ([4, 8, 10, 15], [0, 4, 8, 10], [0, 1, 3, 4, 6, 8, 10]),
    "m7b5": ([3, 6, 10, 12], [0, 3, 6, 10], [0, 1, 3, 5, 6, 8, 10]),
}
PC = {"C": 0, "Db": 1, "D": 2, "Eb": 3, "E": 4, "F": 5, "Gb": 6, "F#": 6,
      "G": 7, "Ab": 8, "A": 9, "Bb": 10, "B": 11}

# each bar is one chord, or two chords (2 beats each) separated by a space
FORMS = {
    "two-five-one": ["D m9", "G 13", "C maj9", "A 7alt", "F maj9", "F m6", "E m9", "A 7alt",
                     "D m9", "G 13", "C 6/9", "D m9|G 13"],
    "minor-bossa": ["A m9", "A m9", "D m9", "D m9", "B m7b5", "E 7alt", "A m9", "E 7alt",
                    "F maj9", "B m7b5|E 7alt", "A m6", "B m7b5|E 7alt"],
    "jazz-blues": ["F 13", "Bb 13", "F 13", "C m9|F 13", "Bb 13", "Bb 13", "F 13", "D 7alt",
                   "G m9", "C 13", "F 6/9|D 7alt", "G m9|C 13"],
    "rhythm": ["C maj9|A 7alt", "D m9|G 13", "E m9|A 7alt", "D m9|G 13",
               "C 13", "F maj9|F m6", "E m9|A 7alt", "D m9|G 13"],
}


def parse_bar(bar):
    out = []
    for c in bar.split("|"):
        root, q = c.split()
        out.append((PC[root], q))
    return out


def hz(m):
    return 440.0 * 2 ** ((m + TRANSPOSE - 69) / 12)


def fold(n, lo, hi):
    while n < lo:
        n += 12
    while n >= hi:
        n -= 12
    return n


# ---------- instruments ----------
def env_adsr(t, dur, a, decay):
    e = np.exp(-decay * t) * np.minimum(1, t / a)
    return e * np.clip((dur - t) / 0.06, 0, 1)


def piano(m, dur, vel):
    t = np.arange(int((dur + 0.4) * SR)) / SR
    f = hz(m)
    s = np.zeros_like(t)
    for k, amp in enumerate([1.0, 0.55, 0.3, 0.18, 0.1, 0.06], 1):
        fk = f * k * np.sqrt(1 + 0.0004 * k * k)  # slight inharmonicity
        s += amp * np.sin(2 * np.pi * fk * t) * np.exp(-(1.2 + 0.7 * k) * t)
    s += 0.004 * np.random.standard_normal(len(t)) * np.exp(-80 * t)  # hammer
    return s * env_adsr(t, dur + 0.4, 0.003, 0.9) * vel


def epiano(m, dur, vel):
    t = np.arange(int((dur + 0.3) * SR)) / SR
    f = hz(m)
    s = np.sin(2 * np.pi * f * t + 1.4 * np.exp(-5 * t) * np.sin(2 * np.pi * f * t))
    s += 0.2 * np.sin(2 * np.pi * f * 4 * t) * np.exp(-14 * t)
    return s * env_adsr(t, dur + 0.3, 0.004, 1.8) * vel * (1 + 0.07 * np.sin(2 * np.pi * 4.6 * t))


def bass(m, dur, vel):
    t = np.arange(int(dur * SR)) / SR
    f = hz(m)
    s = np.sin(2 * np.pi * f * t) + 0.45 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-6 * t)
    s += 0.2 * np.sin(2 * np.pi * 3 * f * t) * np.exp(-10 * t)
    s += 0.05 * np.random.standard_normal(len(t)) * np.exp(-200 * t)  # finger pluck
    return np.tanh(1.3 * s) * env_adsr(t, dur, 0.004, 2.6) * vel


def vibes(m, dur, vel):
    t = np.arange(int((dur + 0.5) * SR)) / SR
    f = hz(m)
    s = np.sin(2 * np.pi * f * t) + 0.25 * np.sin(2 * np.pi * 4 * f * t) * np.exp(-9 * t)
    s += 0.08 * np.sin(2 * np.pi * 10 * f * t) * np.exp(-30 * t)
    return s * env_adsr(t, dur + 0.5, 0.002, 1.4) * vel * (1 + 0.18 * np.sin(2 * np.pi * 5.2 * t))


_hp = butter(2, 6500 / (SR / 2), btype="high")
_hp2 = butter(2, 8000 / (SR / 2), btype="high")
_bp = butter(2, [800 / (SR / 2), 5000 / (SR / 2)], btype="band")
_sn = butter(2, [180 / (SR / 2), 7000 / (SR / 2)], btype="band")


def noise_hit(rng, length, filt, decay, vel):
    n = int(length * SR)
    t = np.arange(n) / SR
    return lfilter(*filt, rng.standard_normal(n)) * np.exp(-decay * t) * vel


def kick(vel):
    t = np.arange(int(0.2 * SR)) / SR
    return np.sin(2 * np.pi * (52 + 45 * np.exp(-30 * t)) * t) * np.exp(-16 * t) * vel


def snare(rng, vel):
    t = np.arange(int(0.18 * SR)) / SR
    body = np.sin(2 * np.pi * 190 * t) * np.exp(-30 * t) * 0.5
    return (body + noise_hit(rng, 0.18, _sn, 22, 1.0)) * vel


# ---------- stereo bus ----------
class Bus:
    def __init__(self, n):
        self.l = np.zeros(n)
        self.r = np.zeros(n)

    def add(self, start, sig, pan=0.0):
        i = int(max(start, 0) * SR)
        if i >= len(self.l):
            return
        k = min(len(sig), len(self.l) - i)
        gl, gr = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
        self.l[i : i + k] += sig[:k] * gl
        self.r[i : i + k] += sig[:k] * gr


def reverb(bus, rng, seconds=2.2, mix=0.3):
    n = int(seconds * SR)
    t = np.arange(n) / SR
    lp = butter(1, 4500 / (SR / 2))
    out = []
    for ch in (bus.l, bus.r):
        ir = lfilter(*lp, rng.standard_normal(n)) * np.exp(-3.0 * t)
        ir[: int(0.02 * SR)] = 0  # pre-delay
        wet = fftconvolve(ch, ir)[: len(ch)]
        wet *= (np.std(ch) + 1e-9) / (np.std(wet) + 1e-9)
        out.append(ch * (1 - mix) + wet * mix)
    return out


# ---------- composition ----------
def voicing(root, q, prev):
    iv = QUALITY[q][0]
    base = [fold(48 + root, 50, 62) + i for i in iv]
    cands = []
    for rot in range(len(base)):
        v = sorted(base[rot:] + [x + 12 for x in base[:rot]])
        for shift in (-12, 0, 12):
            w = [x + shift for x in v]
            if 50 <= w[0] <= 62 and w[-1] <= 79:
                cands.append(w)
    if not cands:
        return base
    if prev is None:
        return min(cands, key=lambda w: abs(np.mean(w) - 60))
    return min(cands, key=lambda w: sum(abs(a - b) for a, b in zip(w, prev)))


def snap(note, root, q, strong):
    pcs = QUALITY[q][1] if strong else QUALITY[q][2]
    pcs = [(root + p) % 12 for p in pcs]
    for d in (0, 1, -1, 2, -2, 3, -3):
        if (note + d) % 12 in pcs:
            return note + d
    return note


def make_motif(rng, swing):
    """2-bar rhythmic motif: list of (beat_position, step_offset, length_beats)."""
    pos, out, step = 0.0, [], 0
    while pos < 7.0:
        on_beat = abs(pos - round(pos)) < 1e-6
        if on_beat and rng.random() < 0.2:
            pos += 1.0
            continue
        ln = rng.choice([swing, 1.0, 1.5]) if on_beat else 1 - swing
        step += int(rng.choice([-2, -1, 1, 2, 3, -3]))
        out.append((pos, step, ln))
        pos += ln
    return out


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
    np.random.seed(a.seed)

    form_name = list(FORMS)[a.seed % len(FORMS)]
    form = [parse_bar(b) for b in FORMS[form_name]]
    beat = 60.0 / a.bpm
    swing = 0.62 + 0.06 * rng.random()
    comp_inst = piano if rng.random() < 0.5 else epiano

    # arrangement: intro(2 bars) + sections, each one chorus of the form
    target_bars = int(150 / (4 * beat))  # aim ~2.5 min
    n_ch = max(3, round(target_bars / len(form)))
    sections = ["head"] + ["vibes", "piano", "vibes"][: n_ch - 2] + ["head"]
    bars = [("intro", form[-2])] + [("intro", form[-1])]
    for s in sections:
        bars += [(s, b) for b in form]
    total = (len(bars) * 4 + 4) * beat + 4.0
    n = int(total * SR)

    rhythm, lead, low, kit = Bus(n), Bus(n), Bus(n), Bus(n)

    def jit():
        return rng.normal(0, 0.006)

    motif = make_motif(rng, swing)
    prev_voic, prev_note = None, 72
    for bi, (sec, chords) in enumerate(bars):
        t0 = (bi * 4) * beat
        nxt_root = bars[(bi + 1) % len(bars)][1][0][0]
        last_bar_of_4 = bi % 4 == 3
        per = 4 // len(chords)

        for ci, (root, q) in enumerate(chords):
            c0 = t0 + ci * per * beat
            v = voicing(root, q, prev_voic)
            prev_voic = v
            # comping: sparse in head, busier in solos
            pats = [[(0.0, 1.4)], [(1 + swing, 0.6), (3.0, 0.8)], [(0.0, 0.9), (2 + swing, 1.0)],
                    [(1.0, 0.8)], [(swing, 0.6), (2.0, 1.2)]]
            pat = pats[int(rng.integers(len(pats)))]
            for off, ln in pat:
                if off >= per:
                    continue
                vel = 0.10 if sec == "piano" else 0.13
                if sec == "piano":
                    ln *= 0.7
                for k, m in enumerate(v):
                    rhythm.add(c0 + off * beat + k * 0.01 + jit(), comp_inst(m, ln * beat, vel * rng.uniform(0.8, 1.1)), -0.35)

            # bass: two-feel in intro/head, walking in solos
            r = fold(36 + root, 36, 48)
            nr = fold(36 + (chords[ci + 1][0] if ci + 1 < len(chords) else nxt_root), 36, 48)
            if sec in ("intro", "head") and per == 4:
                notes = [(0, r, 2), (2, fold(r + 7, 36, 50), 2)]
            else:
                tones = QUALITY[q][1]
                line = [r]
                for _ in range(per - 2):
                    line.append(fold(r + int(rng.choice(tones[1:] + [2, 5])), 36, 50))
                line.append(nr + int(rng.choice([-1, 1])))
                notes = [(i, m, 1) for i, m in enumerate(line[:per])]
            for b, m, ln in notes:
                low.add(c0 + b * beat + jit(), bass(m, ln * beat * 0.95, 0.45 * rng.uniform(0.9, 1.05)), 0.0)

        # drums
        brushes = sec in ("intro", "head")
        for i in range(4):
            bt = t0 + i * beat
            kit.add(bt + jit(), kick(0.10), 0.0)
            if brushes:
                kit.add(bt, noise_hit(rng, beat * 0.9, _bp, 3.5, 0.035), -0.2)  # brush swish
            kit.add(bt + jit(), noise_hit(rng, 0.4, _hp, 8, 0.11 if not brushes else 0.07), 0.45)  # ride
            if i in (1, 3):
                kit.add(bt + swing * beat + jit(), noise_hit(rng, 0.25, _hp, 12, 0.06), 0.45)
                kit.add(bt + jit(), noise_hit(rng, 0.06, _hp2, 60, 0.08), -0.5)  # hat chick
                if brushes:
                    kit.add(bt + jit(), noise_hit(rng, 0.12, _bp, 25, 0.12), -0.1)
            if not brushes and rng.random() < 0.12:
                kit.add(bt + swing * beat, snare(rng, 0.05), -0.1)  # ghost note
        if last_bar_of_4 and bi % 8 == 7:
            for k in range(3):
                kit.add(t0 + (3 + k / 3) * beat, snare(rng, 0.10 + 0.03 * k), -0.1)

        # melody
        root, q = chords[0]
        if sec == "head":
            phrase_bar = bi % 4
            if phrase_bar in (0, 2):
                base = snap(72 + int(rng.choice([-2, 0, 2])), root, q, True)
                for pos, step, ln in motif:
                    bar_off = int(pos // 4)
                    croot, cq = bars[min(bi + bar_off, len(bars) - 1)][1][0]
                    m = snap(base + step, croot, cq, abs(pos - round(pos)) < 1e-6)
                    m = fold(m, 64, 86)
                    lead.add(t0 + pos * beat + jit(), vibes(m, ln * beat * 1.2, 0.2 * rng.uniform(0.85, 1.1)), 0.35)
        elif sec in ("vibes", "piano") and bi % 4 != 3:
            inst, pan, vel = (vibes, 0.35, 0.18) if sec == "vibes" else (piano, -0.15, 0.2)
            cur = prev_note
            pos = 0.0
            while pos < 4.0:
                ci = min(int(pos // per), len(chords) - 1)
                croot, cq = chords[ci]
                on_beat = abs(pos - round(pos)) < 1e-6
                if on_beat and rng.random() < 0.15:
                    pos += 1.0
                    continue
                cur = snap(cur + int(rng.choice([-2, -1, 1, 2, -3, 3, 4])), croot, cq, on_beat)
                cur = fold(cur, 62, 86)
                ln = (swing if rng.random() < 0.7 else 1.0) if on_beat else 1 - swing
                lead.add(t0 + pos * beat + jit(), inst(cur, ln * beat * 1.1, vel * (1.15 if on_beat else 0.85)), pan)
                pos += ln
            prev_note = cur

    # ending: tonic chord + bass + vibes ring out
    tend = len(bars) * 4 * beat
    root, q = form[0][0] if form_name != "rhythm" else (0, "6/9")
    for k, m in enumerate(voicing(root, "6/9" if q in ("maj9", "13", "6/9") else q, prev_voic)):
        rhythm.add(tend + k * 0.05, piano(m, 3.0, 0.14), -0.35)
    low.add(tend, bass(fold(36 + root, 36, 48), 3.0, 0.45), 0.0)
    lead.add(tend + 0.2, vibes(fold(72 + root + 7, 70, 84), 3.0, 0.15), 0.35)
    kit.add(tend, noise_hit(rng, 2.5, _hp, 1.5, 0.12), 0.45)

    # mix
    melodic = Bus(n)
    melodic.l = rhythm.l + lead.l
    melodic.r = rhythm.r + lead.r
    ml, mr = reverb(melodic, rng, mix=0.32)
    kl, kr = reverb(kit, rng, seconds=1.2, mix=0.15)
    L = ml + kl + low.l * 1.0
    R = mr + kr + low.r * 1.0
    crack = np.zeros(n)
    for _ in range(int(total * 5)):
        i = int(rng.random() * (n - 100))
        crack[i : i + 60] += rng.standard_normal(60) * np.exp(-np.arange(60) / 10) * 0.015
    L, R = L + crack, R + crack * 0.8

    stereo = np.stack([L, R])
    stereo = lfilter(*butter(2, 11000 / (SR / 2)), stereo, axis=1)
    stereo /= np.max(np.abs(stereo)) + 1e-9
    stereo = np.tanh(1.6 * stereo) / np.tanh(1.6)  # warm saturation / glue
    fade_in = int(0.5 * SR)
    stereo[:, :fade_in] *= np.linspace(0, 1, fade_in)
    fade_out = int(2.5 * SR)
    stereo[:, -fade_out:] *= np.linspace(1, 0, fade_out)
    stereo *= 0.89

    pcm = (stereo.T * 32767).astype("<i2")
    with wave.open(a.out, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    print(f"wrote {a.out}: {total:.1f}s form={form_name} sections={sections} bpm={a.bpm} comp={comp_inst.__name__}")


if __name__ == "__main__":
    main()
