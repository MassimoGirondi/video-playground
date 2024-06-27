import cv2
from av import VideoFrame
from torchvision import transforms
import torch
import numpy as np

import time_tracker
tt = time_tracker.get()


class DummyTransformer():
    def __init__(self, device = "cpu", do_nothing=False):
        if device == "cuda":
            torch.cuda.init()
            device = torch.device("cuda", 0)

        self.device = device
        self.totensor=transforms.ToTensor()
        self.do_nothing = do_nothing
        print("Using device", self.device)

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


    def __call__(self, img):
        # Here we simulate the wrapping that would happen
        # Around a standard pytorch/model call


        if not self.do_nothing:
            img = self.preprocessing(img)
            img = self.postprocessing(img)
        return img


