#!/usr/bin/env bash
# Downloads Salamander Grand Piano V3 samples (CC BY 3.0, Alexander Holm) from npm into
# ~/.cache/jazz-bgm/salamander (override with PIANO_SAMPLES). Used by gen_jazz_bgm.py.
set -euo pipefail
DEST=${PIANO_SAMPLES:-$HOME/.cache/jazz-bgm/salamander}
mkdir -p "$DEST"
TMP=$(mktemp -d)
cd "$TMP"
for v in 2 4 6 8 10 12 14 16; do npm pack "@audio-samples/piano-velocity$v@1.0.5" --silent >/dev/null; done
npm pack "@audio-samples/piano-release@1.0.5" --silent >/dev/null
for t in *.tgz; do tar xzf "$t" --wildcards 'package/audio/*.ogg' && mv package/audio/*.ogg "$DEST"/ && rm -rf package; done
rm -rf "$TMP"
echo "samples in $DEST: $(ls "$DEST" | wc -l) files, $(du -sh "$DEST" | cut -f1)"
