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

torch.cuda.init() 
gpu = torch.device('cuda')


MODEL="mosaic"
RUNS=10
SAMPLES=64
SAMPLES2=8
BATCHES=[1,4,8,16,32,64]
DTYPE=torch.float16



frames = FrameDataset(name="bbb", n=118, device = gpu)
loader = torch.utils.data.DataLoader(frames, batch_size=1, shuffle=False, num_workers=0)
model = load_model("mosaic")
m = model.to(DTYPE)
model.eval()

for b in tqdm(loader):
    bb = b.to(DTYPE)
    outputs = model(bb)


# dprint("Loading input frames")
# frames = load_images(n=SAMPLES, randomize=True)
# dprint("Loading model")

# # Put every frame on the GPU already as we expect them, so we can clock only the inference
# dprint("Pre-load frames")
# gpu_frames = [preprocessing(f).to(DTYPE) for f in frames]
# dprint("Sampling time!")

# all_times = {}
# for b in BATCHES:
#     try:
#         gf = [gpu_frames[:b] for i in range(SAMPLES2)]
#         times = bench(m, gf, RUNS, False)
#         all_times[b] = [(t/b) for t in times]
#         dprint("Average inference time:", (sum(times) / (RUNS*b)), "ms for batch size", b)
#     except:
#         traceback.print_exc()



# fig = plt.figure(figsize=(16, 9), dpi=100) 
# plt.violinplot(all_times.values())
# plt.xticks(np.arange(1, len(all_times.keys()) + 1), labels=all_times.keys())

# plt.tight_layout()
# plt.xlabel("type")
# plt.ylabel("time (ms)")
# plt.savefig("dtypes-times.pdf")
