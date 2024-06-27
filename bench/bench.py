import argparse
import logging

import os 
import inspect
import sys
from pathlib import Path
from aiortc.contrib.media import MediaBlackhole, MediaPlayer, MediaRecorder, MediaRelay
import asyncio
import time
import datetime as dt
import pandas as pd

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
sys.path.insert(0, str(Path(parentdir) / "webrtc-server"))
sys.path.insert(0, str(Path(parentdir) / "transformers"))
import config
import signal
from video_transformer import VideoTransformTrack
import time_tracker

async def run(args):

    player = MediaPlayer(args.source)
    # if args.record:
    #     recorder = MediaRecorder(args.record)
    # else:
    #     recorder = MediaBlackhole()


    #relay = MediaRelay()
    #relay.subscribe(player.video),
    transform = VideoTransformTrack( player.video, args.transform, timestamp=True)
    #recorder.addTrack(transform)
    #recorder.addTrack(player.video)
    #await recorder.start()
    start = dt.datetime.now()
    processed = 0
    last_fps = 0
    last_avg = start
    stats = []
    while True:
        #frame = await player.video.recv()
        this_start = dt.datetime.now()
        frame = await transform.recv()
        now = dt.datetime.now()
        processed+=1

        # Remember how much it took to process one single frame
        t = now-this_start

        # # Every 100 frames (aprox. 4 seconds at 25 fps) calculate and record the fps
        # if processed % 100 == 0:
        #     t2 = now-last_avg
        #     fps = processed / (t2.seconds + t2.microseconds/1e6)
        #     if last_fps == 0:
        #         last_fps = fps
        #     last_fps = last_fps*0.7 + fps * 0.3
        #     processed = 0
        #     last_avg = now
        #     print("FPS:", fps, "TIME AVG:", last_fps)
        t2 = now - start
        fps = processed / (t2.seconds + t2.microseconds/1e6)
        stats.append((now.timestamp(), (t.seconds + t.microseconds/1e6) , fps))
        if processed%100 == 0:
            print("FPS:", fps, "TIME:", (t.seconds + t.microseconds/1e6))

        if args.time>0 and (now - start).seconds > int(args.time):
            print("Timeout!")

            break
    print("Saving", len(stats), "records")
    df = pd.DataFrame(stats)
    df.columns=["ts", "t", "fps"]
    df.to_csv(args.output)
    time_tracker.dump(args.output_times)





# async def tasker(args):
#     task = asyncio.create_task(run(args))
#     await asyncio.gather(task)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Benchmark harness for backend service(s)"
    )
    parser.add_argument("--transform", help="The transform to apply", choices = config.models.keys(), default = "mosaic")
    parser.add_argument("--source", help="Source media for the benchmark", default = "../inputs/bbb.mp4")
    #parser.add_argument("--record", help="Whether to record (or not, if empty) the resulting stream")
    parser.add_argument("--loop", help="Loop the file untile the end of the world", action="store_true")
    parser.add_argument("--time", help="How many seconds to run. 0 for infinite", default=30, type=int)
    parser.add_argument("--output", help="Where to save stats", default="output.csv")
    parser.add_argument("--output-times", help="Where to save time stats", default="output-times.csv")

    parser.add_argument("--verbose", "-v", action="count")
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    # THis is prone to fail at the end, but in general works :)
    asyncio.run(run(args))

    # loop = asyncio.get_event_loop()
    # loop.close()
    #asyncio.run(tasker(args))
    #asyncio.set_event_loop(asyncio.ProactorEventLoop())
    # loop.run_until_complete(run(args))

