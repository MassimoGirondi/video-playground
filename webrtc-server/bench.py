import argparse
import asyncio
import json
import logging
import os
import ssl
import uuid

import datetime as dt
import av
import cv2
from aiohttp import web
from aiortc import MediaStreamTrack, RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.media import MediaBlackhole, MediaPlayer, MediaRecorder, MediaRelay
from av import VideoFrame

import openrtist_transformer
import edge_transformer
import superresolution_transformer
import video_transformer

import time_tracker 
tt = time_tracker.get()




test_input = av.open("../inputs/bbb-720p.mp4")
test_output =av.open('bench-output.mp4', 'w')

in_stream = test_input.streams.video[0]
#transformer = openrtist_transformer.OpenrtistTransformer("mosaic", track = in_stream)


codec_name = in_stream.codec_context.name  # Get the codec name from the input video stream.
fps = in_stream.codec_context.rate  # Get the framerate from the input video stream.
out_stream = test_output.add_stream(codec_name, str(fps))
out_stream.width = in_stream.codec_context.width  # Set frame width to be the same as the width of the input stream
out_stream.height = in_stream.codec_context.height  # Set frame height to be the same as the height of the input stream
out_stream.pix_fmt = in_stream.codec_context.pix_fmt


for frame in in_stream.decode():
    print(frame)
    img = frame.to_ndarray(format="bgr24")
    new_frame = VideoFrame.from_ndarray(img, format="bgr24")
    new_frame.pts = frame.pts
    new_frame.time_base = frame.time_base
    test_output.mux(new_frame)

test_output.close()
