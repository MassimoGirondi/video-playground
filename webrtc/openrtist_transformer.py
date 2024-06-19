# This is just a convenience wrapper to the openrtist torch implementation


import os
import sys
import inspect
import torch
from torchvision import transforms
from torch import nn
import datetime as dt

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import utils
import empty_model

times = {}
processed_frames = 0

def create_model(model_name="mosaic"):
    torch.cuda.init() 
    gpu = torch.device('cuda')

    if model_name == "empty_torch":
        model = empty_model.EmptyModel().to(torch.float16)

    else:
        model = utils.load_model(model_name, models_path="../openrtist/models").to(torch.float16)

    model.eval()
    model = model.to(gpu)
    totensor  = transforms.ToTensor()

    def reset_times():
        global times, processed_frames
        times["preprocessing"] = []
        times["model"] = []
        times["postprocessing"] = []
        processed_frames = 0

    def print_times():
        global times, processed_frames
        pre = [t.seconds*1e6+t.microseconds for t in times["preprocessing"]] 
        model= [t.seconds*1e6+t.microseconds for t in times["model"]] 
        post= [t.seconds*1e6+t.microseconds for t in times["postprocessing"]] 

        print("  PRE:", sum(pre) / processed_frames, "us")
        print("  MODEL:", sum(model) / processed_frames, "us")
        print("  POST:", sum(post) / processed_frames, "us")

    reset_times()

    def call(frame):
        global times, processed_frames

        t1 = dt.datetime.now()
        f = totensor(frame).unsqueeze(0).to(gpu).to(torch.float16)
        t2 = dt.datetime.now()
        times["preprocessing"].append(t2-t1)
        t1 = dt.datetime.now()
        f = model(f)
        t2 = dt.datetime.now()
        times["model"].append(t2-t1)
        f = utils.postprocessing(f) 
        torch.cuda.synchronize()
        t2 = dt.datetime.now()
        times["postprocessing"].append(t2-t1)
        t1 = dt.datetime.now()


        processed_frames+=1
        if processed_frames > 300 :
            print_times()
            reset_times()



        return f

    return call
