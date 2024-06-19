import argparse
import asyncio
import json
import logging
import os
import ssl
import uuid

import datetime as dt
import cv2
from aiohttp import web
from aiortc import MediaStreamTrack, RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.media import MediaBlackhole, MediaPlayer, MediaRecorder, MediaRelay
from av import VideoFrame

import openrtist_transformer

times = {}

class VideoTransformTrack(MediaStreamTrack):
    """
    A video stream track that transforms frames from an another track.
    """

    kind = "video"

    def __init__(self, track, transform):
        super().__init__()  # don't forget this!
        self.track = track
        self.transform = transform
        self.model = None
        self.times = {}
        self.processed_frames = 0

    def reset_times(self):
        self.times["decode"] = []
        self.times["pre_process"] = []
        self.times["inference"] = []
        self.times["post_process"] = []
        self.times["encode"] = []
        self.processed_frames = 0

    def print_times(self):
        decode = [t.seconds*1e6+t.microseconds for t in self.times["decode"]] 
        inference = [t.seconds*1e6+t.microseconds for t in self.times["inference"]] 
        encode = [t.seconds*1e6+t.microseconds for t in self.times["encode"]] 

        print("DECODE:", sum(decode) / self.processed_frames, "us")
        print("INFERENCE:", sum(inference) / self.processed_frames, "us")
        print("ENCODE:", sum(encode) / self.processed_frames, "us")
    async def recv(self):
        frame = await self.track.recv()

        if self.transform == "edges":
            # perform edge detection
            img = frame.to_ndarray(format="bgr24")
            img = cv2.cvtColor(cv2.Canny(img, 100, 200), cv2.COLOR_GRAY2BGR)

            # rebuild a VideoFrame, preserving timing information
            new_frame = VideoFrame.from_ndarray(img, format="bgr24")
            new_frame.pts = frame.pts
            new_frame.time_base = frame.time_base
            return new_frame
        elif self.transform == "rotate":
            # rotate image
            img = frame.to_ndarray(format="bgr24")
            rows, cols, _ = img.shape
            M = cv2.getRotationMatrix2D((cols / 2, rows / 2), frame.time * 45, 1)
            img = cv2.warpAffine(img, M, (cols, rows))

            # rebuild a VideoFrame, preserving timing information
            new_frame = VideoFrame.from_ndarray(img, format="bgr24")
            new_frame.pts = frame.pts
            new_frame.time_base = frame.time_base
            return new_frame

        elif self.transform in ["mosaic", "cafe_gogh", "sunday_afternoon", "empty_torch"]:
            if not self.model:
                self.model = openrtist_transformer.create_model(self.transform)
                self.reset_times()

            t1 = dt.datetime.now()
            img = frame.to_ndarray(format="bgr24")
            t2 = dt.datetime.now()
            self.times["decode"].append(t2-t1)
            t1 = dt.datetime.now()
            img = self.model(img)
            t2 = dt.datetime.now()
            self.times["inference"].append(t2-t1)
            t1 = dt.datetime.now()
            new_frame= VideoFrame.from_ndarray(img, format="bgr24")
            t2 = dt.datetime.now()
            self.times["encode"].append(t2-t1)
            new_frame.pts = frame.pts
            new_frame.time_base = frame.time_base

            self.processed_frames+=1
            if self.processed_frames > 300 :
                self.print_times()
                self.reset_times()

            return new_frame
        else:
            return frame

