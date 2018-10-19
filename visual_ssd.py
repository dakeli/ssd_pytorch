from __future__ import print_function
from visualize import make_dot
from data import *
from data import VOC_ROOT, VOCAnnotationTransform, VOCDetection, BaseTransform
from data import VOC_CLASSES as labelmap
from utils.augmentations import SSDAugmentation
from layers.modules import MultiBoxLoss
from ssd import build_ssd
import os
import sys
import time
import torch
from torch.autograd import Variable
import torch.nn as nn
import torch.optim as optim
import torch.backends.cudnn as cudnn
import torch.nn.init as init
import torch.utils.data as data
import numpy as np
import argparse
import visdom
import os


def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")


parser = argparse.ArgumentParser(description='Single Shot MultiBox Detector Evaluation')
parser.add_argument('--trained_model',default='weights/VOC.pth', type=str,help='Trained state_dict file path to open')
parser.add_argument('--save_folder', default='eval/', type=str, help='File path to save results')
parser.add_argument('--confidence_threshold', default=0.01, type=float, help='Detection confidence threshold')
parser.add_argument('--top_k', default=5, type=int, help='Further restrict the number of predictions to parse')
parser.add_argument('--cuda', default=False, type=str2bool,help='Use cuda to train model')
parser.add_argument('--voc_root', default=VOC_ROOT,help='Location of VOC root directory')
parser.add_argument('--cleanup', default=True, type=str2bool,help='Cleanup and remove results files following eval')
parser.add_argument('--show_results', default=True, type=str2bool,help='show image detection results after detection')
args = parser.parse_args()

if not os.path.exists(args.save_folder):
    os.mkdir(args.save_folder)

if torch.cuda.is_available():
    if args.cuda:
        torch.set_default_tensor_type('torch.cuda.FloatTensor')
    if not args.cuda:
        print("WARNING: It looks like you have a CUDA device, but aren't using \
              CUDA.  Run with --cuda for optimal eval speed.")
        torch.set_default_tensor_type('torch.FloatTensor')
else:
    torch.set_default_tensor_type('torch.FloatTensor')

annopath = os.path.join(args.voc_root, 'VOC2007', 'Annotations', '%s.xml')
imgpath = os.path.join(args.voc_root, 'VOC2007', 'JPEGImages', '%s.png')
imgsetpath = os.path.join(args.voc_root, 'VOC2007', 'ImageSets',
                          'Main', '{:s}.txt')
YEAR = '2007'
devkit_path = args.voc_root + 'VOC' + YEAR
dataset_mean = (104, 117, 123)
set_type = 'test'

# load net
num_classes = len(labelmap) + 1  # +1 for background
net = build_ssd('test', 300, num_classes)  # initialize SSD
net.load_state_dict(torch.load(args.trained_model))
net.eval()
print('Finished loading model!')
# load data
dataset = VOCDetection(args.voc_root, [('2007', set_type)],BaseTransform(300, dataset_mean),VOCAnnotationTransform())
if args.cuda:
    net = net.cuda()
    cudnn.benchmark = True

im, gt, h, w, img_id = dataset.pull_item(0)
x = Variable(im.unsqueeze(0))
if args.cuda:
    x = x.cuda()
y = net(x)
g = make_dot(y)

# g.view()
g.render('network_train', view=False)


#############权值的结构##########
params = list(net.parameters())
k = 0
for i in params:
    l = 1
    print("**该层的结构**：" + str(list(i.size())))
    for j in i.size():
        l *= j
    print("该层参数和：" + str(l))
    k = k + l
print("####总参数数量和####：" + str(k))