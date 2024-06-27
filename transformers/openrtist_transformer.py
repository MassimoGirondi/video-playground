# This is just a convenience wrapper to the openrtist torch implementation

import os
import sys
import inspect
import datetime as dt
import numpy as np
import empty_transformer

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


class OpenrtistTransformer(empty_transformer.EmptyTransformer):
    def __init__(self, model_name = "mosaic", models_path="../openrtist/models", device = "cpu"):


        # We import elements here so we don't fail if there is 
        # no torch support (e.g. minimal local development copy)


        if device == "cuda":
            torch.cuda.init()
            device = torch.device("cuda", 0)

        self.device = device
        print("Using device", self.device)
        self.model = utils.load_model(model_name, models_path="../openrtist/models").to(torch.float16)
        self.model.eval()
        self.totensor=transforms.ToTensor()


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
        f = self.preprocessing(frame)
        tt.step("oa_pre")
        f = self.model(f)
        tt.step("oa_model")
        f = self.postprocessing(f)
        tt.step("oa_post")
        return f
