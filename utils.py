import torch
import numpy as np
import glob
from torch.autograd import Variable
from pathlib import Path
import datetime as dt
import random
from tqdm import tqdm

from torchvision import transforms
import PIL
import re

from torchvision.transforms import v2
from multiprocessing import Process
from transformer_net import TransformerNet   
content_transform = transforms.Compose([transforms.ToTensor()])

def preprocessing(img):
    content_image = content_transform(img)
    content_image = content_image.cuda()
    content_image = content_image.unsqueeze(0)
    #return Variable(content_image)
    return content_image

def postprocessing(img, precast=False):
    img = torch.squeeze(img)
    img = img.permute(1, 2, 0)
    img = img.clamp(0, 255)
    if precast:
        img = img.detach().cpu().float()
    else:
        img = img.detach().cpu()
    return img.numpy().astype(np.uint8)
    
def showarray(a, fmt='png'):
    a = np.uint8(a)
    f = StringIO()
    PIL.Image.fromarray(a).save(f, fmt)
    IPython.display.display(IPython.display.Image(data=f.getvalue()))

def load_image(image_path):
    image = PIL.Image.open(image_path).convert('RGB')
    image_np = np.asarray(image)
    image_np = image_np.astype(np.uint8)
    return image_np

def process_image(image, model):
    img = preprocessing(image)
    out_img = model(img)
    out_img = postprocessing(out_img)
    return out_img

def load_images(path="./inputs/*.png", n=0, randomize=False):
    filenames = list(glob.glob(path))
    # Order them, even if they miss leading 0s...
    filenames.sort(key=lambda x: int(re.sub(r'[^0-9]*', "", x)))
    if n > 0:
        if randomize:
            random.shuffle(filenames)
        filenames = filenames[:n]
    return [load_image(f) for f in filenames]

def load_model(name="mosaic",models_path="./openrtist/models", cuda=True):
    model_path = Path(models_path)/ (name+".model")
    model = TransformerNet()
    model.load_state_dict(torch.load(model_path))
    if cuda:
        model = model.cuda()
    return model

def dprint(*args, **kw):
    # print("[%s]" % (dt.datetime.now()),*args, **kw)
    print("[%s]" % (dt.datetime.now().strftime("%H:%M:%S.%f")[:-3]),*args, **kw)


last_print = dt.datetime.utcfromtimestamp(0)
def tprint(*args, **kw):
    global last_print
    threshold=30
    now = dt.datetime.now()
    elapsed = now-last_print
    if elapsed.seconds >  threshold:
        #print("[%s]" % (dt.datetime.now()),*args, **kw)
        print("[%s]" % (dt.datetime.now().strftime("%H:%M:%S")),*args, **kw)
    else:
        print("[ %+d ]" % (elapsed.seconds + elapsed.microseconds/1e6),*args, **kw)
    last_print = now


def bench(model, samples, runs, keep_outputs=False):
    # Just in case we have something being run
    torch.cuda.synchronize()

    # Use CUDA event to measure "only the inferences"
    start = torch.cuda.Event(enable_timing=True)
    end = torch.cuda.Event(enable_timing=True)
    times = []
    outputs = []

    for i in tqdm(range(runs)):
        start.record()
        # Don't save intermediate values
        with  torch.no_grad():
            out_frames = [model(img) for img in tqdm(samples)]
        end.record()
        torch.cuda.synchronize()
        times.append(start.elapsed_time(end))
        if keep_outputs:
            outputs.append(out_frames)

    if keep_outputs:
        return times, outputs
    else:
        return times


def parallel_for(task, args, max_processes):
    processes = [Process(target=task, args=a) for a in args]
    for i in range(0, len(args), max_processes):
        this_p = processes[i:min(len(args),max_processes+i)]
        for process in this_p:
            process.start()
        for process in this_p:
            process.join()
