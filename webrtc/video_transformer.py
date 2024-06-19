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
import edge_transformer

import time_tracker 
tt = time_tracker.get()

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
        self.processed_frames = 0
        if transform == "edges":
            self.transformer = edge_transformer.EdgeTransformer()
        elif transform in ["mosaic", "cafe_gogh", "sunday_afternoon"]:
            self.transformer = openrtist.OpenrtistTransformer(model)
        else:
            self.transformer = None

    async def recv(self):
        tt.start()
        frame = await self.track.recv()
        tt.step("recv")
        img = frame.to_ndarray(format="bgr24")
        tt.step("decode")
        if self.transformer:
            img = self.transformer(img)
        new_frame = VideoFrame.from_ndarray(img, format="bgr24")
        tt.step("encode")
        new_frame.pts = frame.pts
        new_frame.time_base = frame.time_base

        self.processed_frames+=1
        if self.processed_frames > 100:
            print(tt)
            tt.reset()
            self.processed_frames = 0

        return new_frame

