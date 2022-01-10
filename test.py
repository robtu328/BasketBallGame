import config as cfg
import torchvision.models as models
import torch.nn as nn
import torchvision.models as models


from loader.data_loaders import *
from loader.mnist import *

def train(train_loader, model, criterion, optimizer, epoch, args):
    model.train()
    
    for i, (images, target) in enumerate(train_loader):
        output = model(images)
        

def validate(val_loader, model, criterion, args):
    model.eval()



if __name__ == '__main__':
    

    print ("Hello world")


    model = models.__dict__[cfg.arch]()
    criterion = nn.CrossEntropyLoss().cuda(cfg.gpu)

    optimizer = torch.optim.SGD(model.parameters(), cfg.lr,
                                momentum=cfg.momentum,
                                weight_decay=cfg.weight_decay)
    #optimizer = torch.optim.Adam(capsnet.parameters(), lr=opts.learning_rate)
    train_loader, valid_loader, test_loader=load_mnist(cfg.train_batch_size, valid_size=0.1)
    
    
    
    print ("Hello world2")

