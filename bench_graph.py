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
DTYPE=torch.float16

dprint("Loading input frames")
#frames = load_images(n=SAMPLES, randomize=True)
frames = FrameDataset(name="bbb", n=SAMPLES, device = gpu)
dprint("Loading model")
#model = load_model("mosaic")
model = empty_model.EmptyModel()
model.eval()

m = model.to(dtype)
gf = [f.to(dtype) for f in frames[:PREVIEW]]
times, out = bench(m, gf, 1, True)
dprint("Average inference time:", (sum(times) / (RUNS*PREVIEW)), "ms for", dtype)
