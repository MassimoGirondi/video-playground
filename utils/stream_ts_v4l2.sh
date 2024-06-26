#!/bin/bash

sudo modprobe v4l2loopback video_nr=9 card_label=Video-Loopback exclusive_caps=0

SOURCE=/dev/video0
DEST=/dev/video9

# if [ ! -f SOURCE ]; then
#         echo "No source $SOURCE"
#         exit 1
# fi
# if [ ! -f $DEST ]; then
#         echo "No device $DEST"
#         exit 2
# fi

ffmpeg -re  -f v4l2 -framerate 30 -video_size 1920x1080 -input_format mjpeg  -i $SOURCE \
  -filter_complex "drawtext=fontfile=/usr/share/fonts/truetype/freefont/FreeSerif.ttf: text='frame %{n}\\: %{pict_type}\\: pts=%{pts \\: hms}': x=100: y=50: fontsize=34: fontcolor=white: box=1: boxcolor=blue:boxborderw=8" \
  -pix_fmt yuv420p \
-f v4l2 $DEST
  #-f v4l2 -vcodec rawvideo -pix_fmt yuv420p $DEST


  #-filter_complex "drawtext=fontfile=/usr/share/fonts/truetype/freefont/FreeSerif.ttf: text='frame %{n}\\: %{pict_type}\\: pts=%{pts \\: hms}': x=100: y=50: fontsize=24: fontcolor=yellow@0.8: box=1: boxcolor=blue@0.9" \
