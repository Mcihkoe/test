#!/usr/bin/env bash
# Usage: tools/render_long_video.sh IMAGE MIX.mp3 OUT.mp4
# Renders a seamless 60s zoom in/out loop once, then repeats it (no re-encode) over the full mix.
set -euo pipefail
IMG=$1; AUD=$2; OUT=$3
LOOP=60; FPS=25; N=$((LOOP*FPS))
TMP=$(mktemp -d)
python3 -c "
from PIL import Image
Image.open('$IMG').convert('RGB').resize((3840,2160), Image.LANCZOS).save('$TMP/big.png')"
ffmpeg -y -loglevel error -loop 1 -framerate $FPS -i "$TMP/big.png" \
  -vf "zoompan=z='1.03+0.03*(0.5-0.5*cos(2*PI*on/$N))':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1920x1080:fps=$FPS,format=yuv420p" \
  -frames:v $N -c:v libx264 -preset veryfast -crf 20 "$TMP/loop.mp4"
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$AUD")
ffmpeg -y -loglevel error -stream_loop -1 -i "$TMP/loop.mp4" -i "$AUD" -t "$DUR" \
  -c:v copy -c:a aac -b:a 192k -movflags +faststart "$OUT"
rm -rf "$TMP"
echo "wrote $OUT (${DUR}s)"
