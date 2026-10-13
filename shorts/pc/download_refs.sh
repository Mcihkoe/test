#!/bin/bash
# 레퍼런스 영상 한 번에 받기 (Mac/Linux)
# 처음 한 번만: brew install yt-dlp ffmpeg
cd "$(dirname "$0")"
yt-dlp -a refs.txt -f "bv*[height<=1080]+ba/b" --merge-output-format mp4 -o "%(id)s.%(ext)s" --sleep-interval 3
echo "끝났습니다. 생긴 mp4 파일들을 Claude 대화창에 첨부해 주세요."
