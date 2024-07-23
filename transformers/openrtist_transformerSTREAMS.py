# This is just a convenience wrapper to the openrtist torch implementation

import os
import sys
import inspect
import datetime as dt
import numpy as np
import empty_transformer
from collections import deque

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import utils
import time_tracker
tt = time_tracker.get()

if not "NO_TORCH" in os.environ:
    import torch
    from torchvision import transforms
    from torch import nn


class OpenrtistTransformerSTREAMS(empty_transformer.EmptyTransformer):
    def __init__(self, model_name = "mosaic", models_path="../openrtist/models", device = "cpu", streams = 3, events=1024):


        if device == "cuda":
            torch.cuda.init()
            device = torch.device("cuda", 0)

        self.device = device
        print("Using device", self.device)
        self.model = utils.load_model(model_name, models_path="../openrtist/models").to(torch.float16)
        self.model.eval()
        self.totensor=transforms.ToTensor()
        self.copy_input_stream = torch.cuda.Stream()
        self.model_stream = torch.cuda.Stream()
        self.copy_output_stream = torch.cuda.Stream()
        self.events = deque([torch.cuda.Event(enable_timing=False) for i in range(events)])
        tt.times["sm_usage"] = []
        tt.times["mem_usage"] = []


    def preprocessing(self, frame):
        f = self.totensor(frame).unsqueeze(0).to(self.device).to(torch.float16)
        return f

    def postprocessing(self, frame):
        # TODO: Do we nee all of these?
        img = torch.squeeze(frame)
        img = img.permute(1, 2, 0)
        img = img.clamp(0, 255)
        img = img.detach().cpu()
        return img.numpy().astype(np.uint8)

    def __call__(self, frame):
        copy_input_event = self.events.popleft()
        model_event = self.events.popleft()
        copy_output_event = self.events.popleft()


        with torch.cuda.stream(self.copy_input_stream): 
            f = self.preprocessing(frame)
            copy_input_event.record(self.copy_input_stream)
        with torch.cuda.stream(self.model_stream):
            copy_input_event.wait(self.model_stream)
            f = self.model(f)
            model_event.record(self.model_stream)
        with torch.cuda.stream(self.copy_output_stream):
            model_event.wait(self.model_stream)
            f = self.postprocessing(f)

        self.events.append(copy_input_event)
        self.events.append(copy_output_event)
        self.events.append(model_event)
        sm_usage, mem_usage = utils.gpu_usage()
        tt.times["sm_usage"].append(sm_usage)
        tt.times["mem_usage"].append(mem_usage)
        return f



