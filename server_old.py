import torch
import torchvision
from pathlib import Path
from torchvision import transforms
import numpy as np
import os
from transformer_net import TransformerNet   
from torchinfo import summary
from torch.autograd import Variable
from PIL import Image

models_path = "./openrtist/models/"
model_name = "david_vaughan"
content_transform = transforms.Compose([transforms.ToTensor()]) 
model_path = Path(models_path)/ (model_name+".model")

model = TransformerNet()
model.load_state_dict(torch.load(model_path))
model = model.cuda()
summary(model)


def preprocessing(img):
    content_image = content_transform(img)
    content_image = content_image.cuda()
    content_image = content_image.unsqueeze(0)
    print("PRE:",img.shape)
    return Variable(content_image)

def postprocessing(img):
    print("POST1:", img.shape)
    #img = img.data[0].clamp(0, 255).cpu().numpy()
    img = img.cpu().numpy()
    print("POST:",img.shape)
    return img.transpose(1, 2, 0)

images_path = Path("./inputs")
image_name =  "bbb-161.png"
image_path = images_path / image_name
image = Image.open(image_path).convert('RGB')

image_np = np.asarray(image)
image_np = image_np.astype(np.uint8)
# img = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
# img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


img = preprocessing(image_np)
out_img = model(img).data[0]
out_img = postprocessing(out_img)


#img = postprocessing(img)

# image = Image.fromarray(image_np)
# image.save(images_path / (".".join((image_name).split(".")[:-1]) + "-processes.png"))



