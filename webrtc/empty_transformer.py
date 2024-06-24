class EmptyTransformer():
    def __init__(self, device = "cpu"):
        if device != "cpu":
            print("EdgeTransformer: ignoring device", device)
        pass
    def __call__(self, img):
        return img
