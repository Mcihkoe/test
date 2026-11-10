#!/usr/bin/env bash
# VetG Sialic Vital 25초 광고 합본 스크립트 (16:9, 1920x1080, 30fps)
#
# 준비물
#   clips/s01.mp4 … s07.mp4   장면별 생성 영상 (길이는 넉넉하게; 앞에서부터 아래 길이만큼 잘라 씀)
#   audio/narration.wav       (선택) 한국어 내레이션 — cue 시점은 BRIEF.md 참고
#   audio/bgm.wav             (선택) 피아노·현악 배경음악 25초 이상
# 결과: out/vetg_sialic_vital_25s.mp4
set -euo pipefail
cd "$(dirname "$0")"

DUR=(3 3 4 4 4 3 4)   # s01..s07 → 합계 25초
END_AT=21.2            # 엔딩 오버레이 시작 시각
mkdir -p out build

# 1) 장면별 정규화: 길이 자르기, 1920x1080 채움 크롭, 30fps, 원본 앰비언스 유지(없으면 무음)
for i in $(seq 1 7); do
  n=$(printf "s%02d" "$i"); d=${DUR[$((i-1))]}
  src="clips/$n.mp4"; [ -f "$src" ] || { echo "missing $src"; exit 1; }
  if ffprobe -v error -select_streams a -show_entries stream=index -of csv=p=0 "$src" | grep -q .; then
    ain=(-i "$src"); amap="0:a"
  else
    ain=(-f lavfi -t "$d" -i anullsrc=r=48000:cl=stereo); amap="1:a"
  fi
  ffmpeg -loglevel error -y -i "$src" "${ain[@]}" -t "$d" \
    -filter_complex "[0:v]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,fps=30,setsar=1,format=yuv420p[v];[$amap]aresample=48000,aformat=channel_layouts=stereo,apad[a]" \
    -map "[v]" -map "[a]" -t "$d" -c:v libx264 -crf 16 -preset medium -c:a aac -b:a 192k "build/$n.mp4"
done

# 2) 이어 붙이기 — 장면 사이 0.25초 디졸브 대신 컷 편집(절제된 편집). 필요하면 xfade로 교체.
: > build/list.txt; for i in $(seq 1 7); do printf "file '%s'\n" "s0$i.mp4" >> build/list.txt; done
ffmpeg -loglevel error -y -f concat -safe 0 -i build/list.txt -c copy build/joined.mp4

# 3) 오디오 믹스: 현장음 -10dB, BGM -16dB(내레이션 구간 사이드체인 덕킹), 내레이션 0dB
inputs=(-i build/joined.mp4 -loop 1 -t 25 -i endcard/endcard_overlay.png)
amix="[0:a]volume=-10dB[amb]"; parts="[amb]"; k=2
if [ -f audio/bgm.wav ]; then inputs+=(-i audio/bgm.wav); amix+=";[$k:a]atrim=0:25,afade=t=out:st=23:d=2,volume=-16dB[bgm]"; bgm=$k; k=$((k+1)); fi
if [ -f audio/narration.wav ]; then inputs+=(-i audio/narration.wav); amix+=";[$k:a]asplit[nar][sc]"; nar=1; fi
if [ -n "${bgm:-}" ] && [ -n "${nar:-}" ]; then amix+=";[bgm][sc]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=400[bgmd]"; parts+="[bgmd][nar]"
elif [ -n "${bgm:-}" ]; then parts+="[bgm]"
elif [ -n "${nar:-}" ]; then amix+=";[sc]anullsink"; parts+="[nar]"; fi
cnt=$(grep -o '\[' <<<"$parts" | wc -l)
amix+=";${parts}amix=inputs=$cnt:normalize=0,alimiter=limit=0.89,atrim=0:25[aout]"

# 4) 자막(Pretendard) + 21.2초부터 엔딩 오버레이 페이드 인
vf="[0:v]subtitles=subtitles.ass:fontsdir=fonts[sv];[1:v]format=rgba,fade=t=in:st=$END_AT:d=0.8:alpha=1[ov];[sv][ov]overlay=0:0:shortest=1,fade=t=out:st=24.4:d=0.6[vout]"
ffmpeg -loglevel error -y "${inputs[@]}" -filter_complex "$vf;$amix" \
  -map "[vout]" -map "[aout]" -t 25 -c:v libx264 -crf 17 -preset slow -pix_fmt yuv420p \
  -c:a aac -b:a 192k -movflags +faststart out/vetg_sialic_vital_25s.mp4
echo "done → out/vetg_sialic_vital_25s.mp4"
