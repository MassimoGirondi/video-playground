import torch
from utils import *
from torch.utils.data import Dataset, DataLoader
import random



class FrameDataset(Dataset):
    def load_frame(self,file):
        img = PIL.Image.open(file).convert("RGB")
        img_np = np.asarray(img)
        return self.totensor(img_np).unsqueeze(0)

    def __init__(self,
                 folder="inputs/",
                 name="bbb",
                 n=0,
                 randomize=False,
                 transform=None,
                 device=None,
                 num_workers=0):


        self.transform = transform
        self.totensor = transforms.ToTensor()
        self.full_path = f"{folder}/{name}-*"
        self.all_files = filenames = list(glob.glob(self.full_path))  
        if randomize:
            random.shuffle(self.all_files)   
        else:
            self.all_files.sort(key=lambda x: int(re.sub(r'[^0-9]*','',x)))

        if n > 0 and n < len(self.all_files):
            self.files = self.all_files[:n]
        else:
            self.files = self.all_files

        self.frames = [self.load_frame(f) for f in self.files]
        if self.transform:
            self.frames = [self.transform(f) for f in self.frames]

        if device:
            self.frames = [f.to(device) for f in self.frames]


    def __len__(self):
        return len(self.frames)

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()

        frames = self.frames[idx]
        return frames



# class FramePreProcess():
#     def __init__(self):
#         pass
#     def __call__(self, f):
#         return f.unsqueeze(0)



