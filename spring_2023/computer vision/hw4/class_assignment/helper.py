import time
import torch
import torch.nn as nn
import torchvision
import numpy as np
import matplotlib.pyplot as plt
from torchvision import transforms
from tqdm.notebook import trange, tqdm
import torch.optim as optim
from CNN import *
from AverageMeter import *

# %matplotlib widget
print_frequency = 100

def accuracy(output, target, topk=(1,)):
    """Computes the precision@k for the specified values of k"""
    maxk = max(topk)
    batch_size = target.size(0)

    _, pred = output.topk(maxk, 1, True, True)
    pred = pred.t()
    correct = pred.eq(target.view(1, -1).expand_as(pred))

    res = []
    for k in topk:
        correct_k = correct[:k].view(-1).float().sum(0)
        res.append(correct_k.mul_(100.0 / batch_size))
    return res

# def train(model, loader, criterion, optimizer, epoch):
#     batch_time = AverageMeter()
#     data_time = AverageMeter()
#     losses = AverageMeter()
#     top1 = AverageMeter()

#     # switch to train mode
#     model.train()

#     end = time.time()
#     for i, (input, target) in enumerate(loader):
#         # measure data loading time
#         data_time.update(time.time() - end)

#         if torch.cuda.is_available():
#             input = input.cuda()
#             target = target.cuda()

#         # compute output
#         output = model(input)
#         loss = criterion(output, target)

#         # measure accuracy and record loss
#         prec1 = accuracy(output, target)[0]
#         losses.update(loss.item(), input.size(0))
#         top1.update(prec1.item(), input.size(0))

#         # compute gradient and do SGD step
#         optimizer.zero_grad()
#         loss.backward()
#         optimizer.step()

#         # measure elapsed time
#         batch_time.update(time.time() - end)
#         end = time.time()

#         if i % print_frequency == 0:
#             print('Epoch: [{0}][{1}/{2}]\t'
#                   'Time {batch_time.val:.3f} ({batch_time.avg:.3f})\t'
#                   'Data {data_time.val:.3f} ({data_time.avg:.3f})\t'
#                   'Loss {loss.val:.4f} ({loss.avg:.4f})\t'
#                   'Prec@1 {top1.val:.3f} ({top1.avg:.3f})'.format(
#                    epoch, i, len(loader), batch_time=batch_time,
#                    data_time=data_time, loss=losses, top1=top1))

def train(model, loader, criterion, optimizer, epoch):
    batch_time = AverageMeter()
    data_time = AverageMeter()
    losses = AverageMeter()
    top1 = AverageMeter()

    model.train()

    end = time.time()
    pbar = tqdm(enumerate(loader), total=len(loader))
    for i, (input, target) in pbar:
        
        # input = input.cuda()
        # target = target.cuda()

        data_time.update(time.time() - end)

        output = model(input)
        loss = criterion(output, target)

        # Update Step
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        output = output.float()
        loss = loss.float()

        prec = accuracy(output.data, target)[0]
        losses.update(loss.item(), input.shape[0])
        top1.update(prec.item(), input.shape[0])

        batch_time.update(time.time() - end)
        end = time.time()

        if i % print_frequency == 0:
            pbar.set_description("Epoch [%d]\t Loss %.2f\t Prec@1 %.3f (%.3f)" % (epoch, losses.avg, top1.val, top1.avg))


def test(model, loader, criterion):
    batch_time = AverageMeter()
    data_time = AverageMeter()
    losses = AverageMeter()
    top1 = AverageMeter()

    model.eval()

    end = time.time()
    pbar = tqdm(enumerate(loader), total=len(loader))
    for i, (input, target) in pbar:
        
        # input = input.cuda()
        # target = target.cuda()

        data_time.update(time.time() - end)

        output = model(input)
        loss = criterion(output, target)

        output = output.float()
        loss = loss.float()

        prec = accuracy(output.data, target)[0]
        losses.update(loss.item(), input.shape[0])
        top1.update(prec.item(), input.shape[0])

        batch_time.update(time.time() - end)
        end = time.time()

        if i % print_frequency == 0:
            pbar.set_description("Loss %.2f\t Prec@1 %.3f (%.3f)" % (losses.avg, top1.val, top1.avg))