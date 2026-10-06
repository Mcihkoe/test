#!/usr/bin/env python3
"""Synthesize a jazzy instrumental BGM track (no external AI needed). v3

Usage: python3 tools/gen_jazz_bgm.py OUT.wav [--bpm 92] [--seed 7] [--transpose 0] [--comp piano|rhodes]

Each seed picks a chord form and an arrangement:
  intro -> head (motif melody) -> vibes solo -> piano solo -> head out -> ending chord
Instruments are real sampled sounds (FluidR3_GM SoundFont via FluidSynth):
Yamaha grand piano comping (or Rhodes with --comp rhodes), acoustic bass, vibraphone lead, brush drum kit.
Requires: apt install fluidsynth fluid-soundfont-gm && pip install mido
"""
import argparse
import wave

import numpy as np

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


# ---------- instruments (rendered from real sampled instruments via SoundFont) ----------
SF2 = "/usr/share/sounds/sf2/FluidR3_GM.sf2"
# name -> (GM program, MIDI velocity scale for the amplitude-style vel values below)
PROGRAMS = {"piano": (0, 380), "epiano": (4, 420), "bass": (32, 180), "vibes": (11, 350)}
CHANNEL_VOLUME = {"piano": 127, "epiano": 120, "bass": 90, "vibes": 120, "drum": 105}  # CC7 mix balance
DRUM = {"kick": 36, "tap": 38, "swirl": 40, "pedal_hat": 44, "ride": 51}


def piano(m, dur, vel):
    return ("piano", m, dur, vel)


def epiano(m, dur, vel):
    return ("epiano", m, dur, vel)


def bass(m, dur, vel):
    return ("bass", m, dur, vel)


def vibes(m, dur, vel):
    return ("vibes", m, dur, vel)


def drum(name, vel, dur=0.25):
    return ("drum", DRUM[name], dur, vel)


class Bus:
    """Collects note events; one MIDI channel per (bus, instrument)."""

    def __init__(self, name, events):
        self.name = name
        self.events = events

    def add(self, start, note, pan=0.0):
        self.events.append((self.name, max(start, 0.0), note, pan))


def write_midi(events, path, total):
    import mido

    tpq, tempo = 480, 500000  # 120 bpm grid; we place events in seconds
    def tick(sec):
        return int(round(sec * 1e6 / tempo * tpq))

    mid = mido.MidiFile(ticks_per_beat=tpq)
    track = mido.MidiTrack()
    mid.tracks.append(track)
    msgs = [(0, 0, mido.MetaMessage("set_tempo", tempo=tempo))]
    chans, nxt = {}, 0
    for bus, start, (inst, m, dur, vel), pan in events:
        key = "drum" if inst == "drum" else (bus, inst)
        if key not in chans:
            if key == "drum":
                ch = 9
                msgs.append((0, 1, mido.Message("program_change", channel=9, program=40)))  # Brush kit
                send = 30
            else:
                ch = nxt
                nxt += 1 + (nxt + 1 == 9)
                msgs.append((0, 1, mido.Message("program_change", channel=ch, program=PROGRAMS[inst][0])))
                send = {"bass": 25}.get(inst, 55)
            msgs.append((0, 1, mido.Message("control_change", channel=ch, control=10, value=int(64 + pan * 63))))
            msgs.append((0, 1, mido.Message("control_change", channel=ch, control=91, value=send)))
            msgs.append((0, 1, mido.Message("control_change", channel=ch, control=93, value=0)))
            msgs.append((0, 1, mido.Message("control_change", channel=ch, control=7, value=CHANNEL_VOLUME[inst])))
            chans[key] = ch
        ch = chans[key]
        if inst == "drum":
            v, note = int(vel), m
        else:
            v, note = int(vel * PROGRAMS[inst][1]), m + TRANSPOSE
        v = max(1, min(127, v))
        on, off = tick(start), tick(start + dur)
        msgs.append((on, 3, mido.Message("note_on", channel=ch, note=note, velocity=v)))
        msgs.append((max(off, on + 1), 2, mido.Message("note_off", channel=ch, note=note, velocity=0)))
    msgs.append((tick(total), 4, mido.MetaMessage("end_of_track")))
    msgs.sort(key=lambda x: (x[0], x[1]))
    last = 0
    for t, _, msg in msgs:
        track.append(msg.copy(time=t - last))
        last = t
    mid.save(path)


def render(midi_path, wav_path):
    import subprocess

    subprocess.run(
        ["fluidsynth", "-ni", "-q", "-g", "0.45", "-r", str(SR), "-O", "s16",
         "-o", "synth.reverb.active=1", "-o", "synth.reverb.room-size=0.55",
         "-o", "synth.reverb.damp=0.4", "-o", "synth.reverb.width=0.8", "-o", "synth.reverb.level=0.7",
         "-o", "synth.chorus.active=0", "-F", wav_path, SF2, midi_path],
        check=True,
    )


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
    ap.add_argument("--comp", choices=["piano", "rhodes"], default="piano", help="comping instrument")
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
    comp_inst = epiano if a.comp == "rhodes" else piano

    # arrangement: intro(2 bars) + sections, each one chorus of the form
    target_bars = int(150 / (4 * beat))  # aim ~2.5 min
    n_ch = max(3, round(target_bars / len(form)))
    sections = ["head"] + ["vibes", "piano", "vibes"][: n_ch - 2] + ["head"]
    bars = [("intro", form[-2])] + [("intro", form[-1])]
    for s in sections:
        bars += [(s, b) for b in form]
    total = (len(bars) * 4 + 4) * beat + 4.0
    n = int(total * SR)

    events = []
    rhythm, lead, low, kit = (Bus(k, events) for k in ("rhythm", "lead", "low", "kit"))

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
            kit.add(bt + jit(), drum("kick", rng.integers(28, 40)), 0.0)
            if brushes:
                kit.add(bt, drum("swirl", rng.integers(35, 50), beat * 0.9), -0.2)  # brush swish
            kit.add(bt + jit(), drum("ride", rng.integers(62, 76) if not brushes else rng.integers(45, 58)), 0.45)  # ride
            if i in (1, 3):
                kit.add(bt + swing * beat + jit(), drum("ride", rng.integers(38, 52)), 0.45)
                kit.add(bt + jit(), drum("pedal_hat", rng.integers(50, 65)), -0.5)  # hat chick
                if brushes:
                    kit.add(bt + jit(), drum("tap", rng.integers(45, 60)), -0.1)
            if not brushes and rng.random() < 0.12:
                kit.add(bt + swing * beat, drum("tap", rng.integers(22, 34)), -0.1)  # ghost note
        if last_bar_of_4 and bi % 8 == 7:
            for k in range(3):
                kit.add(t0 + (3 + k / 3) * beat, drum("tap", 55 + 10 * k), -0.1)

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
    kit.add(tend, drum("ride", 70, 3.0), 0.45)

    # render real instruments, then master
    import os
    import tempfile

    tmpd = tempfile.mkdtemp()
    mid_path, raw_path = os.path.join(tmpd, "song.mid"), os.path.join(tmpd, "raw.wav")
    write_midi(events, mid_path, total)
    render(mid_path, raw_path)
    with wave.open(raw_path, "rb") as w:
        raw = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(np.float64) / 32768
    os.remove(mid_path)
    os.remove(raw_path)
    os.rmdir(tmpd)
    stereo = raw.reshape(-1, 2).T[:, :n]
    if stereo.shape[1] < n:
        stereo = np.pad(stereo, ((0, 0), (0, n - stereo.shape[1])))

    crack = np.zeros(n)
    for _ in range(int(total * 4)):
        i = int(rng.random() * (n - 100))
        crack[i : i + 60] += rng.standard_normal(60) * np.exp(-np.arange(60) / 10) * 0.004
    stereo = stereo + np.stack([crack, crack * 0.8])

    stereo /= np.max(np.abs(stereo)) + 1e-9
    stereo = np.tanh(1.15 * stereo) / np.tanh(1.15)  # gentle glue
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
