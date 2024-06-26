ffmpeg -i ~/scratchpad/BigBuckBunny.mp4 -vf fps=30 ./inputs/bbb-%d.png
ffmpeg -ss 10 -i ~/scratchpad/BigBuckBunny.mp4 -c copy -t 10 ./inputs/bbb-720p.mp4
ffmpeg -ss 10 -i ~/scratchpad/BigBuckBunny.mp4 -c copy -t 10 -filter:v scale=480:-1 ./inputs/bbb-480p.mp4
