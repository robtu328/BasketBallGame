import argparse
import config as cfg
import torch.nn as nn
import torchvision.models as models


from loader.data_loaders import *
from loader.mnist import *

class AverageMeter(object):
    """Computes and stores the average and current value"""
    def __init__(self, name, fmt=':f'):
        self.name = name
        self.fmt = fmt
        self.reset()

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count

    def __str__(self):
        fmtstr = '{name} {val' + self.fmt + '} ({avg' + self.fmt + '})'
        return fmtstr.format(**self.__dict__)

def accuracy(output, target, topk=(1,)):
    """Computes the accuracy over the k top predictions for the specified values of k"""
    with torch.no_grad():
        maxk = max(topk)
        batch_size = target.size(0)

        _, pred = output.topk(maxk, 1, True, True)
        pred = pred.t()
        correct = pred.eq(target.view(1, -1).expand_as(pred))

        res = []
        for k in topk:
            correct_k = correct[:k].reshape(-1).float().sum(0, keepdim=True)
            res.append(correct_k.mul_(100.0 / batch_size))
        return res




def train(train_loader, model, criterion, optimizer, epoch, args):
    top1 = AverageMeter('Acc@1', ':6.2f')
    top5 = AverageMeter('Acc@5', ':6.2f')
    losses = AverageMeter('Loss', ':.4e')

    model.train()
    
    for i, (images, target) in enumerate(train_loader):
        if cfg.gpu is not None:
            images = images.cuda(cfg.gpu, non_blocking=True)
        if torch.cuda.is_available():
            target = target.cuda(cfg.gpu, non_blocking=True)  
            
        #Forward propgration
        images=images.expand(64, 3, 28,28)
        output = model(images)
        loss = criterion(output, target)
        acc1, acc5 = accuracy(output, target, topk=(1, 5))
        losses.update(loss.item(), images.size(0))
        top1.update(acc1[0], images.size(0))
        top5.update(acc5[0], images.size(0))

        #backward propgration 
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        

def validate(val_loader, model, criterion, args):
    top1 = AverageMeter('Acc@1', ':6.2f')
    top5 = AverageMeter('Acc@5', ':6.2f')
    losses = AverageMeter('Loss', ':.4e')

    model.eval()
    with torch.no_grad():     #No grad calculation
        
        for i, (images, target) in enumerate(val_loader):
            if cfg.gpu is not None:
                images = images.cuda(cfg.gpu, non_blocking=True)
            if torch.cuda.is_available():
                target = target.cuda(cfg.gpu, non_blocking=True)  
            
            #Forward propgration
            output = model(images)
            loss = criterion(output, target)
            acc1, acc5 = accuracy(output, target, topk=(1, 5))
            losses.update(loss.item(), images.size(0))
            top1.update(acc1[0], images.size(0))
            top5.update(acc5[0], images.size(0))


            print(' * Acc@1 {top1.avg:.3f} Acc@5 {top5.avg:.3f}'
              .format(top1=top1, top5=top5))


    return top1.avg, top5.avg


if __name__ == '__main__':
    

    print ("Hello world")
    #parameters set up
    model_names = sorted(name for name in models.__dict__
                         if name.islower() and not name.startswith("__")
                         and callable(models.__dict__[name]))
    
    parser = argparse.ArgumentParser(description='PyTorch Simple Training')
    parser.add_argument('-a', '--arch', metavar='ARCH', default='resnet18',
                    choices=model_names,
                    help='model architecture: ' +
                        ' | '.join(model_names) +
                        ' (default: resnet18)')
    
    args = parser.parse_args()
    
    
    #Objects initialization
    model = models.__dict__[cfg.arch]()
    
    if cfg.gpu is not None:
        torch.cuda.set_device(cfg.gpu)
        model.cuda(cfg.gpu)
    
    
    criterion = nn.CrossEntropyLoss().cuda(cfg.gpu)

    optimizer = torch.optim.SGD(model.parameters(), cfg.lr,
                                momentum=cfg.momentum,
                                weight_decay=cfg.weight_decay)
    #optimizer = torch.optim.Adam(capsnet.parameters(), lr=opts.learning_rate)
    #Load dataset
    train_loader, valid_loader, test_loader=load_mnist(cfg.train_batch_size, valid_size=0.1)

    
    for epoch in range(0, cfg.epoch):
    
       #Forward propgration
       train(train_loader, model, criterion, optimizer, epoch, args)
     
       # evaluate on validation set
       acc1, acc5 = validate(val_loader, model, criterion, args)   

    
    print ("Hello world2")

