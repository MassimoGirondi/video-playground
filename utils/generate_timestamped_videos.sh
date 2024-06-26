ffmpeg -i ./inputs/bbb.mp4 \
  -filter_complex "drawtext=fontfile=/usr/share/fonts/truetype/freefont/FreeSerif.ttf: text='frame %{n}\\: %{pict_type}\\: pts=%{pts \\: hms}': x=100: y=50: fontsize=24: fontcolor=yellow@0.8: box=1: boxcolor=blue@0.9" \
  -c:a copy -c:v libx264 -preset veryfast -crf 16 -x264-params keyint=60 -map 0 inputs/bbb-ts.mp4

