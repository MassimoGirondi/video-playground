from utils import *
import logging
from tqdm import tqdm
import datetime as dt
from pprint import pprint
import gc
#import torch_tensorrt
from torchinfo import summary
from PIL import Image
import traceback
import matplotlib.pyplot as plt

MODEL="mosaic"
RUNS=10
SAMPLES=32
PREVIEW=3

dprint("Loading input frames")
frames = load_images(n=SAMPLES, randomize=True)
dprint("Loading model")
model = load_model("mosaic")
model.eval()

# Put every frame on the GPU already as we expect them, so we can clock only the inference
dprint("Pre-load frames")
gpu_frames = [preprocessing(f) for f in frames]
dprint("Sampling time!")


# m = torch.ao.quantization.quantize_dynamic(
#     model,  # the original model
#     {torch.nn.Linear},  # a set of layers to dynamically quantize
#     dtype=torch.qint8)  # the target dtype for quantized weights
model.qconfig = torch.ao.quantization.get_default_qconfig('x86')
#model_fp32_fused = torch.ao.quantization.fuse_modules(model, [['deconv1', 'relu']])
model_fp32_fused = model
model_fp32_prepared = torch.ao.quantization.prepare(model_fp32_fused)
model_fp32_prepared(gpu_frames[0])
model_int8 = torch.ao.quantization.convert(model_fp32_prepared).eval()



#gf = [f.to(torch.quint8) for f in gpu_frames]
gf = gpu_frames
times = bench(model_int8, gf, RUNS, False)
dprint("Average inference time:", (sum(times) / (RUNS*SAMPLES)), "ms")
