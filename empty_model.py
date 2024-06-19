import torch
class EmptyModel(torch.nn.Module):
    def __init__(self):
        super(EmptyModel, self).__init__()
        self.identity1 = torch.nn.Identity()
        self.identity2 = torch.nn.Identity()
        self.identity3 = torch.nn.Identity()
    def forward(self, x):
        x = self.identity1(x)
        x = self.identity2(x)
        x = self.identity3(x)
        return x


if __name__ == "__main__":
    torch.cuda.init() 
    gpu = torch.device('cuda')
    i = torch.tensor([[2,3,4,5,6],[1,2,3,4,5]])
    model = EmptyModel()
    model.eval()
    o = model(i)
    print(i)
    print(o)
