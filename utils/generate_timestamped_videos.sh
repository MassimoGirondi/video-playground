ffmpeg -i ../inputs/bbb.mp4 \
  -filter_complex "drawtext=fontfile=/usr/share/fonts/truetype/freefont/FreeSerif.ttf: text='frame %{n}\\: %{pict_type}\\: pts=%{pts \\: hms}': x=100: y=50: fontsize=30: fontcolor=yellow: box=1: boxcolor=blue: boxborderw=8" \
  -c:a copy -c:v libx264 -preset veryfast -crf 16 -x264-params keyint=60 -map 0 ../inputs/bbb-ts.mp4

