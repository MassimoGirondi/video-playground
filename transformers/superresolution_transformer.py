import os
import sys
import inspect
import torch
from torchvision import transforms
from torch import nn
import datetime as dt
import numpy as np
import torchsr
import PIL
from torchvision.transforms.functional import to_pil_image, to_tensor

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import utils
import torchinfo
import time_tracker
tt = time_tracker.get()

class SuperresolutionTransformer():
    def __init__(self,  model_name= "ninasr_b0", device = "cpu", dtype = torch.float16):

        if device == "cuda":
            torch.cuda.init()
            device = torch.device("cuda", 0)

        self.device = device
        self.dtype = dtype
        print("Using device", self.device)
        # self.model = utils.load_model(model_name, models_path="../openrtist/models").to(torch.float16)
        if model_name == "ninasr_b0":
            self.model = torchsr.models.ninasr_b0(scale=1)
        else:
            raise "Not supported"

        self.model.eval()
        torchinfo.summary(self.model)
        self.model = self.model.to(device=device, dtype = self.dtype)
        self.totensor=transforms.ToTensor()

        self.test_frame = to_tensor(PIL.Image.open("../inputs/bbb-1002.png"))

    def preprocessing(self, frame):
        frame = self.totensor(frame)
        frame = frame.unsqueeze(0).to(device=self.device, dtype=self.dtype)
        return frame

    def postprocessing(self, frame):
        frame = frame.squeeze(0)
        frame = frame.permute(1, 2, 0)
        framet = frame.clamp(0, 255)
        frame = frame.to("cpu")
        frame = frame.numpy().astype(np.uint8)
        return frame

    def __call__(self, frame):

        f = self.test_frame
        f = self.preprocessing(frame)

        tt.step("oa_pre")
        with torch.no_grad():
            f = self.model(f)
        tt.step("oa_model")
        f = self.postprocessing(f)
        tt.step("oa_post")
        return f
