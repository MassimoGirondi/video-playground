import cv2
from av import VideoFrame

import time_tracker
tt = time_tracker.get()


class EdgeTransformer():
    def __init__(self, device = "cpu"):
        if device != "cpu":
            print("EdgeTransformer: ignoring device", device)
        pass
    def __call__(self, img):
        img = cv2.cvtColor(cv2.Canny(img, 100, 200), cv2.COLOR_GRAY2BGR)

        return img
