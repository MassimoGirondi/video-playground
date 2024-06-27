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
import torch_enhance

torch.cuda.init() 
gpu = torch.device('cuda')

SAMPLES=4
DTYPE=torch.float16

MODEL="SRResNet"
dprint("Loading input frames")
#frames = load_images(n=SAMPLES, randomize=True)
frames = FrameDataset(name="bbb", n=SAMPLES, device = gpu, randomize=True)
dprint("Loading model")
#model = load_model(MODEL)
model = torch_enhance.models.SRResNet(scale_factor=2, channels=3)
model = model.to(DTYPE)
model = model.to(gpu)
model.eval()

print(model)
summary(model)


fig = plt.figure(figsize=(16, 9), dpi=400)
try:
    gf = [f.to(DTYPE) for f in frames]
    times, out = bench(model, gf, 1, True)
    out = out[0]
    dprint("Average inference time:", (sum(times) / len(times)))
    out

    #out_np = [postprocessing(o) for o in out]

    for i, o in enumerate(out_np):
        fig.add_subplot(2, SAMPLES, (i+1))
        plt.imshow(PIL.Image.open(frames.all_files[i])) # Just to be sure on what we read
        plt.axis("off")
        fig.add_subplot(2, SAMPLES, (i+1+SAMPLES))
        plt.axis("off")
        plt.imshow(PIL.Image.fromarray(o))
except:
    traceback.print_exc()

plt.tight_layout()
fig.suptitle(f"{MODEL} on {torch.cuda.get_device_properties(gpu.index).name} with {DTYPE}")
plt.savefig(f"enhance.png")

