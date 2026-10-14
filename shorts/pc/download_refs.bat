@echo off
REM 레퍼런스 영상 한 번에 받기 (Windows)
REM 1) 처음 한 번만: winget install yt-dlp.yt-dlp  그리고  winget install Gyan.FFmpeg
REM 2) 이 파일과 refs.txt를 같은 폴더에 두고 더블클릭
yt-dlp -U
yt-dlp -a refs.txt -f "bv*[height<=1080]+ba/b" --merge-output-format mp4 -o "%%(id)s.%%(ext)s" --sleep-interval 3
echo.
echo 끝났습니다. 생긴 mp4 파일들을 Claude 대화창에 첨부해 주세요.
pause
