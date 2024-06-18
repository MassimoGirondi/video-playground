from utils import *
import logging
from tqdm import tqdm
import datetime as dt
from pytorch_benchmark import benchmark
from pprint import pprint
import gc

dprint("Loading input frames")
frames = load_images(n=20, randomize=True)
dprint("Loading model")
model = load_model("mosaic")

# Run a bunch of inferences as warm-up
dprint("Warm-up")
out_frames = [process_image(f, model) for f in tqdm(frames[:10])]
dprint("Warm-up: done")


# Put every frame on the GPU already as we expect them, so we can clock only the inference
dprint("Pre-load frames")
gpu_frames = [preprocessing(f) for f in frames]
dprint("Benchmark time!")

results = benchmark(model, gpu_frames[0], num_runs=100)
pprint(results)
# start = dt.datetime.now()
# for i in tqdm(range(1)):
#     out_frames = [model(img) for img in tqdm(gpu_frames)]
#     del out_frames
#     gc.collect()
# stop = dt.datetime.now()

# print("Done in ", stop-start)




