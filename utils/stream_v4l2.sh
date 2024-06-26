#!/bin/bash
sudo modprobe v4l2loopback video_nr=9 card_label=Video-Loopback exclusive_caps=1

ffmpeg -stream_loop -1 -re -i ../inputs/bbb-ts.mp4  -f v4l2 /dev/video9

