import argparse
import asyncio
import logging
import math

import cv2
import numpy
from aiortc import (
    RTCIceCandidate,
    RTCPeerConnection,
    RTCSessionDescription,
    VideoStreamTrack,
)
from aiortc.contrib.media import MediaBlackhole, MediaPlayer, MediaRecorder
from aiortc.contrib.signaling import BYE, add_signaling_arguments, create_signaling
from aiortc.contrib.signaling import TcpSocketSignaling
from av import VideoFrame
from webrtc_client import WebRTCClient

class TimeCodeTrack(VideoStreamTrack):
    pass




# async def run(pc, player, recorder, signaling):
#     def add_tracks():
#         pc.addTrack(TimeCodeTrack())

#     @pc.on("track")
#     def on_track(track):
#         print("Receiving %s" % track.kind)
#         recorder.addTrack(track)

#     # connect signaling
#     await signaling.connect()

#     add_tracks()
#     await pc.setLocalDescription(await pc.createOffer())
#     await signaling.send(pc.localDescription)

#     # consume signaling
#     while True:
#         obj = await signaling.receive()
#         print("TEST")

#         if isinstance(obj, RTCSessionDescription):
#             await pc.setRemoteDescription(obj)
#             await recorder.start()

#             if obj.type == "offer":
#                 # send answer
#                 add_tracks()
#                 await pc.setLocalDescription(await pc.createAnswer())
#                 await signaling.send(pc.localDescription)
#         elif isinstance(obj, RTCIceCandidate):
#             await pc.addIceCandidate(obj)
#         elif obj is BYE:
#             print("Exiting")
#             break


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Video stream from the command line")
    #parser.add_argument("--play-from", help="Read the media from a file and sent it.")
    #parser.add_argument("--record-to", help="Write received media to a file.")
    parser.add_argument("--verbose", "-v", action="count")
    parser.add_argument("--url", help="The WebRTC endpoint to contact", default = "https://localhost:8080")
    parser.add_argument("--transform", help="What model to run on the server", default = "passthrough")
    add_signaling_arguments(parser)
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    ## create signaling and peer connection
    #signaling = create_signaling(args)
    # signaling = TcpSocketSignaling("127.0.0.1", 8080)
    client = WebRTCClient(args)
    # signaling = WebRTCSignaling(args)
    pc = RTCPeerConnection()

    # run event loop
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            client.run()
        )
    except KeyboardInterrupt:
        pass
    finally:
        # cleanup
        #loop.run_until_complete(recorder.stop())
        loop.run_until_complete(client.signaling.close())
        loop.run_until_complete(client.pc.close())


    # # create media source
    # if args.play_from:
    #     player = MediaPlayer(args.play_from)
    # else:
    #     player = None
