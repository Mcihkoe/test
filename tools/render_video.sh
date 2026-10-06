#!/usr/bin/env bash
# Usage: tools/render_video.sh IMAGE AUDIO OUT.mp4 [TARGET_SECONDS]
# Slow zoom-in over a still image. If TARGET_SECONDS is longer than the audio, the audio is looped.
set -euo pipefail
IMG=$1; AUD=$2; OUT=$3; TARGET=${4:-}
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$AUD")
DUR=${TARGET:-$DUR}
FPS=25
FRAMES=$(python3 -c "print(int(float('$DUR')*$FPS))")
TMP=$(mktemp -d)
python3 -c "
from PIL import Image
Image.open('$IMG').convert('RGB').resize((3840,2160), Image.LANCZOS).save('$TMP/big.png')"
ffmpeg -y -loglevel error -stream_loop -1 -i "$AUD" -loop 1 -framerate $FPS -i "$TMP/big.png" \
  -vf "zoompan=z='1+0.05*on/$FRAMES':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1920x1080:fps=$FPS,format=yuv420p" \
  -t "$DUR" -c:v libx264 -preset veryfast -crf 20 -c:a aac -b:a 192k \
  -af "afade=t=out:st=$(python3 -c "print(max(0,float('$DUR')-2))"):d=2" -shortest -movflags +faststart "$OUT"
rm -rf "$TMP"
echo "wrote $OUT (${DUR}s)"
