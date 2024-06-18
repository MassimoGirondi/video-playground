from utils import *
import logging
from tqdm import tqdm
import datetime as dt
from pprint import pprint
import gc
import torch_tensorrt
from torchinfo import summary

MODEL="mosaic"
RUNS=1
SAMPLES=50

dprint("Loading input frames")
frames = load_images(n=SAMPLES, randomize=True)
dprint("Loading model")
model = load_model("mosaic")
model.eval()
#summary(model)

# Run a bunch of inferences as warm-up
dprint("Warm-up")
out_frames = [process_image(f, model) for f in tqdm(frames[:10])]
dprint("Warm-up: done")


# Put every frame on the GPU already as we expect them, so we can clock only the inference
dprint("Pre-load frames")
gpu_frames = [preprocessing(f) for f in frames]
dprint("Benchmark time!")

times = bench(model, gpu_frames, RUNS)
dprint("Average inference time:", (sum(times) / (RUNS*SAMPLES)), "ms")


with torch.cuda.amp.autocast(cache_enabled=False): # autocast initialized
    times = bench(model, gpu_frames, RUNS)
    dprint("Average inference time with AMP:", (sum(times) / (RUNS*SAMPLES)), "ms")


with torch.cuda.amp.autocast(cache_enabled=True): # autocast initialized
    times = bench(model, gpu_frames, RUNS)
    dprint("Average inference time with AMP+cache:", (sum(times) / (RUNS*SAMPLES)), "ms")


# torch.backends.cudnn.benchmark = True
# torch.backends.cuda.matmul.allow_tf32 = True
# torch.backends.cudnn.allow_tf32 = True

# dprint("Compiling with TensorRT")
# trt_model = torch_tensorrt.compile(model, 
#     inputs= [torch_tensorrt.Input(frames[0].shape)],
#     enabled_precisions= { torch_tensorrt.dtype.half} # Run with FP16
# )

# with torch.cuda.amp.autocast(cache_enabled=True): # autocast initialized
#     times = bench(model, gpu_frames, RUNS)
#     dprint("Average inference time with AMP+cache:", (sum(times) / (RUNS*SAMPLES)), "ms")


# print("Compile with TensorRT")
# torch.backends.cudnn.benchmark = True
# torch.backends.cuda.matmul.allow_tf32 = True
# torch.backends.cudnn.allow_tf32 = True
# trt_model = torch.compile(model, backend="tensorrt", dynamic=False)
# times = bench(trt_model, gpu_frames, RUNS)
# print("Average inference time:", (sum(times) / (RUNS*SAMPLES)), "ms")
