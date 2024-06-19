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
from dataset import *
import empty_model
torch.cuda.init() 
gpu = torch.device('cuda')

MODEL="mosaic"
RUNS=10
SAMPLES=32
PREVIEW=3

dprint("Loading input frames")
#frames = load_images(n=SAMPLES, randomize=True)
frames = FrameDataset(name="bbb", n=SAMPLES, device = gpu)
dprint("Loading model")
#model = load_model("mosaic")
model = empty_model.EmptyModel()

model.eval()


# We first run a sample with 
fig = plt.figure(figsize=(16, 9), dpi=400)
types = [torch.double, torch.float, torch.float16, torch.bfloat16]

for j, dtype in enumerate(types):
    try:
        m = model.to(dtype)
        gf = [f.to(dtype) for f in frames[:PREVIEW]]
        times, out = bench(m, gf, 1, True)
        dprint("Average inference time:", (sum(times) / (RUNS*PREVIEW)), "ms for", dtype)

        if dtype in [torch.bfloat16]:
            out_np = [postprocessing(o,precast=True) for o in out[0]]
        else:
            out_np = [postprocessing(o) for o in out[0]]
        for i, o in enumerate(out_np):
            fig.add_subplot(len(types), PREVIEW, (i+1)+(j*PREVIEW))
            plt.axis("off")
            plt.title(dtype)
            plt.imshow(PIL.Image.fromarray(o))
    except:
        traceback.print_exc()

plt.tight_layout()
plt.savefig("dtypes-preview.png")

dprint("Benchmark time!")


types = [torch.double, torch.float, torch.float16, torch.bfloat16]
all_times = {}
for j, dtype in enumerate(types):
    try:
        m = model.to(dtype)
        gf = [f.to(dtype) for f in frames]
        times = bench(m, gf, RUNS, False)
        all_times[dtype] = [(t/SAMPLES) for t in times]
        dprint("Average inference time:", (sum(times) / (RUNS*SAMPLES)), "ms for", dtype)
    except:
        traceback.print_exc()



fig = plt.figure(figsize=(16, 9), dpi=100) 
plt.violinplot(all_times.values())
plt.xticks(np.arange(1, len(all_times.keys()) + 1), labels=all_times.keys())

plt.tight_layout()
plt.xlabel("type")
plt.ylabel("time (ms)")
plt.savefig("dtypes-times.pdf")
